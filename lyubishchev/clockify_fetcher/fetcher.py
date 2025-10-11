import os
import urllib
from typing import Any, Optional

import arrow
import requests
import urllib3
from arrow import Arrow
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from lyubishchev import config
from lyubishchev.data_model import (
    EVENT_TYPE,
    TYPE_BED,
    VALID_EVENT_LABEL_KEY,
    VALID_EVENT_TAG_KEY,
    Event,
    TimeInterval,
    TimeIntervalFetcher,
    time_diff_minutes,
    validate_event_label_and_tag,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore

TimeSeries = dict[str, Any]


class ClockifyConfig:  # pylint: disable=too-few-public-methods
    host: str
    api_key: str
    workspace_id: str
    user_id: str

    def __init__(self) -> None:
        self.host = "api.clockify.me"
        self.workspace_id = os.getenv(
            "CLOCKIFY_WORKSPACE_ID", "fake_clockify_workspace_id"
        )
        self.user_id = os.getenv("CLOCKIFY_USER_ID", "fake_clockify_id")
        self.api_key = os.getenv("CLOCKIFY_API_KEY", "fake_clockify_key")

    def __repr__(self) -> str:
        return f"""
            ClockifyConfig(
                host={self.host},
                api_key={self.api_key},
                workspace_id={self.workspace_id},
                user_id={self.user_id}
            )
        """


def is_clockify_tag_a_label(tag: str) -> bool:
    """
    label format key=value, tag is string only (no equal sign '=' present)
    """
    return tag.find("=") != -1


def generate_time_interval_from_time_series(
    time_series_entry: TimeSeries,
) -> Optional[TimeInterval]:
    """
    return a TimeInterval from a TimeSeries object, fill
        Metadata: label only, skip annotation for now
        extra_info: from description field, possible for future's annotation parsing
        timestamp:  start of TimeSeries
        duration_in_minutes: end timestamp - start timestamp
    throw: ValueError
    """
    result: TimeInterval = TimeInterval.empty()
    required_keys: list[str] = [
        "timeInterval",
        "tags",
    ]
    for required_key in required_keys:
        if required_key not in time_series_entry:
            raise ValueError(
                f"time_series_entry should contain required key: {required_key}"
            )

    if (
        "end" not in time_series_entry["timeInterval"]
        or time_series_entry["timeInterval"]["end"] is None
    ):
        # no end means currently counting record, return None
        return None

    if "tags" not in time_series_entry:
        raise ValueError(f"time_series_entry should contain tags: {time_series_entry}")
    # fill time fields
    start_timestamp: Arrow = arrow.get(time_series_entry["timeInterval"]["start"]).to(
        config.get_iana_timezone_name()
    )
    end_timestamp: Arrow = arrow.get(time_series_entry["timeInterval"]["end"]).to(
        config.get_iana_timezone_name()
    )
    result.timestamp = start_timestamp
    result.duration_minutes = time_diff_minutes(start_timestamp, end_timestamp)
    # fill metadata
    for tag in time_series_entry["tags"]:
        tag_name: str = tag["name"]
        if is_clockify_tag_a_label(tag_name):
            key, value = tag_name.split("=")
            if key in VALID_EVENT_LABEL_KEY:
                # skip event tag, it will be parsed in generate_event_from_time_series
                continue
            if key in result.metadata.label:  # avoid two type label
                raise ValueError(
                    f"duplicate label key {key}, already exist for entry {start_timestamp}"
                )
            result.metadata.label[key] = value
        else:
            result.metadata.label[tag_name] = ""
    if time_series_entry["project"] is not None:
        result.metadata.label["project"] = time_series_entry["project"]["name"]
    # fill other fields
    result.extra_info = time_series_entry["description"]

    return result


def generate_event_from_time_series(time_series_entry: TimeSeries) -> Optional[Event]:
    # pylint: disable=too-many-branches
    """
    return a event from a TimeSeries object or None if not event contained in TimeSeries
    fill:
        metadata: label only, skip annotation for now
        extra_info: from description field, possible for future's annotation parsing
        timestamp:  start or end of TimeSeries, depends event type
    throw: ValueError, InvalidLabelTag
    """
    result: Optional[Event] = None
    if "tags" not in time_series_entry:
        raise ValueError(f"time_series_entry should contain tags: {time_series_entry}")
    start_timestamp: Arrow = arrow.get(time_series_entry["timeInterval"]["start"]).to(
        config.get_iana_timezone_name()
    )
    for tag in time_series_entry["tags"]:
        tag_name: str = tag["name"]
        if is_clockify_tag_a_label(tag_name):
            key, value = tag_name.split("=")
            valid_label_key_translate_dict: dict[str, str] = {
                "event_type": EVENT_TYPE,
            }
            if key in valid_label_key_translate_dict:
                if result is None:
                    result = Event()
                time_interval_label_key: str = valid_label_key_translate_dict[key]
                if time_interval_label_key in result.metadata.label:
                    raise ValueError(
                        f"time_series_entry at {start_timestamp} contain duplicate event label key"
                    )
                result.metadata.label[time_interval_label_key] = value
        else:
            if tag_name in VALID_EVENT_TAG_KEY:
                if result is None:
                    result = Event()
                result.metadata.label[tag_name] = ""

    if result is None:  # no event type tag means not contain a event
        return None

    if result.metadata.label[EVENT_TYPE] == TYPE_BED:
        result.timestamp = arrow.get(time_series_entry["timeInterval"]["end"]).to(
            config.get_iana_timezone_name()
        )
    else:
        result.timestamp = start_timestamp
    # fill other fields
    result.extra_info = time_series_entry["description"]
    validate_event_label_and_tag(result.metadata.label)
    try:
        validate_event_label_and_tag(result.metadata.label)
    except Exception:
        print(f"unexpected exception when processing time entry: {start_timestamp}")
        raise
    return result


class ClockifyFetcher(TimeIntervalFetcher):
    """
    Find a sample dataset for next step
    """

    config: ClockifyConfig

    def __init__(self, cfg: ClockifyConfig):
        self.config = cfg

    def fetch_time_intervals_events(
        self, start_timestamp: Arrow, end_timestamp: Arrow
    ) -> tuple[list[TimeInterval], list[Event]]:
        """
        Fetch records exactly between: [start_timestamp, end_timestamp]
        """
        if start_timestamp > end_timestamp:
            raise ValueError(
                f"start_timestamp:{start_timestamp} must be early than end_timestamp{end_timestamp}"
            )

        time_series: list[TimeSeries] = self.fetch_raw_time_series(
            start_timestamp, end_timestamp
        )

        time_intervals: list[TimeInterval] = []
        events: list[Event] = []

        # ClockifyAPI returned time entry in order: latest record at first,
        # here we want asc order by timestamp, so need to reverse the result list
        for index, time_series_entry in enumerate(reversed(time_series)):
            time_interval: Optional[TimeInterval] = (
                generate_time_interval_from_time_series(time_series_entry)
            )
            if (
                time_interval is None
            ):  # we reach the record still counting, i.e not stopped
                assert (
                    index == len(time_series) - 1
                ), f"index is {index}, {time_series_entry}, len is {len(time_series)}"
                break

            time_intervals.append(time_interval)

            event: Optional[Event] = generate_event_from_time_series(time_series_entry)
            if event is not None:
                events.append(event)
        return time_intervals, events

    def fetch_raw_time_series(
        self, start_timestamp: Arrow, end_timestamp: Arrow
    ) -> list[dict[str, Any]]:
        """
        return time series in Clockify's object structure(dict[str, Any])
        """
        # timestamp in Clockify must end with Z, even input is local time, bug?
        timestamp_format: str = "%Y-%m-%dT%H:%M:%SZ"
        page_size: int = 50  # Clockify default page size
        retries = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )

        headers = {"X-Api-Key": self.config.api_key}
        query = (
            f"{self.config.host}/api/v1/workspaces/{self.config.workspace_id}"
            f"/user/{self.config.user_id}/time-entries"
        )

        params = {
            "start": start_timestamp.strftime(timestamp_format),
            "end": end_timestamp.strftime(timestamp_format),
            "page-size": str(page_size),
            "hydrated": "true",
        }

        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=retries))
        result_objects: list[dict[str, Any]] = []

        page: int = 1

        while True:
            params["page"] = str(page)
            response = session.get(
                "https://" + urllib.request.pathname2url(query),
                headers=headers,
                params=params,
                verify=False,
            )
            if response.status_code != 200:
                raise ValueError(
                    f"Clockify return non 200: {response.status_code}, content{response.text}"
                )
            resp_json = response.json()
            if len(resp_json) == 0:
                break
            result_objects.extend(resp_json)
            page += 1

        return result_objects
