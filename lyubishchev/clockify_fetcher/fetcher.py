import urllib
from dataclasses import dataclass
from typing import Any

import requests
from arrow import Arrow
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from lyubishchev.data_model import Event, TimeInterval, TimeIntervalFetcher


@dataclass
class ClockifyConfig:
    host: str
    api_key: str
    workspace_id: str
    user_id: str


class ClockifyFetcher(TimeIntervalFetcher):
    """
    Find a sample dataset for next step
    """

    config: ClockifyConfig

    def __init__(self, config: ClockifyConfig):
        self.config = config

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

        return [TimeInterval()], [Event()]

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

    def fetch_last_event_within(
        self, timestamp: Arrow, typ: str, tag: str = ""
    ) -> Event:
        """
        Get when was the last event which matches criteria
        """
