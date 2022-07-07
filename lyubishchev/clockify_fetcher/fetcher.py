import urllib
from dataclasses import dataclass
from typing import Any, Optional

import arrow
import requests
from arrow import Arrow
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from lyubishchev import config
from lyubishchev.data_model import (
    VALID_TIME_INTERVAL_TAGS,
    Event,
    TimeInterval,
    TimeIntervalFetcher,
)

TimeSeries = dict[str, Any]


@dataclass
class ClockifyConfig:
    host: str
    api_key: str
    workspace_id: str
    user_id: str


def is_clockify_tag_a_label(tag: str) -> bool:
    """
    label format key=value, tag is string only (no equal sign '=' present)
    """
    return tag.find("=") != -1


def time_diff_minutes(start: Arrow, end: Arrow) -> int:
    return int((end - start).seconds / 60)


def generate_time_interval_from_time_series(
    time_series_entry: TimeSeries,
) -> TimeInterval:
    """
    return a TimeInterval from a TimeSeries object, fill
        Metadata: label only, skip annotation for now
        extra_info: from description field, possible for future's annotation parsing
        timestamp:  start of TimeSeries
        duration_in_minutes: end timestamp - start timestamp
    throw: ValueError
    """
    result: TimeInterval = TimeInterval()
    if "tags" not in time_series_entry:
        raise ValueError(f"time_series_entry should contain tags: {time_series_entry}")
    for tag in time_series_entry["tags"]:
        tag_name: str = tag["name"]
        if is_clockify_tag_a_label(tag_name):
            key, value = tag_name.split("=")
            valid_label_key: list[str] = ["type"]
            if key in valid_label_key:
                result.metadata.label[key] = value
        else:
            if tag_name in VALID_TIME_INTERVAL_TAGS:
                result.metadata.label[tag_name] = ""
    if time_series_entry["project"] is not None:
        result.metadata.label["project"] = time_series_entry["project"]["name"]
    # fill time fields
    start_timestamp: Arrow = arrow.get(time_series_entry["timeInterval"]["start"]).to(
        config.get_iana_timezone_name()
    )
    end_timestamp: Arrow = arrow.get(time_series_entry["timeInterval"]["end"]).to(
        config.get_iana_timezone_name()
    )
    result.timestamp = start_timestamp
    result.duration_minutes = time_diff_minutes(start_timestamp, end_timestamp)
    # fill other fields
    result.extra_info = time_series_entry["description"]
    if result.extra_info == "":
        raise ValueError(
            f"time_series_entry at {start_timestamp} should contain description field "
        )

    return result


def generate_event_from_time_series(time_series_entry: TimeSeries) -> Optional[Event]:
    """
    return a event from a TimeSeries object or None if not event contained in TimeSeries
    fill:
        metadata: label only, skip annotation for now
        extra_info: from description field, possible for future's annotation parsing
        timestamp:  start or end of TimeSeries, depends event type
    throw: ValueError
    """
    print(time_series_entry)
    return Event()


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

        for time_series_entry in time_series:
            time_interval: TimeInterval = generate_time_interval_from_time_series(
                time_series_entry
            )
            time_intervals.append(time_interval)
            event: Optional[Event] = generate_event_from_time_series(time_series_entry)
            if event is not None:
                events.append(event)

        return time_intervals, events

    def fetch_raw_time_series(
        self, start_timestamp: Arrow, end_timestamp: Arrow
    ) -> list[dict[str, Any]]:
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
            )
            if response.status_code != 200:
                raise Exception(
                    f"Clockify return non 200: {response.status_code}, content{response.text}"
                )
            resp_json = response.json()
            if len(resp_json) == 0:
                break
            result_objects.extend(resp_json)
            page += 1

        return result_objects
