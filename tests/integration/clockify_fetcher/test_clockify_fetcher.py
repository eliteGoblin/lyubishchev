import json
import os

from lyubishchev.clockify_fetcher import ClockifyConfig, ClockifyFetcher
from lyubishchev.data_model import date_range_to_timestamp_range

config: ClockifyConfig = ClockifyConfig(
    host="api.clockify.me",
    workspace_id="5e86fab7183a8475e0c7a757",
    user_id="5e86fab6183a8475e0c7a755",
    api_key=os.getenv("CLOCKIFY_API_KEY", "fake_clockify_key"),
)


# Testing data in sample_data.py


def test_fetch_single_day() -> None:

    fetcher: ClockifyFetcher = ClockifyFetcher(config)
    res = fetcher.fetch_raw_time_series(
        *date_range_to_timestamp_range(
            "2022-07-02", "2022-07-03"
        )  # get [7.2, 7.3), 1 day
    )
    for time_series in res:
        print(json.dumps(time_series, sort_keys=True, indent=4))
    assert len(res) == 30


def test_fetch_3_days() -> None:
    fetcher: ClockifyFetcher = ClockifyFetcher(config)
    res = fetcher.fetch_raw_time_series(
        *date_range_to_timestamp_range("2022-07-02", "2022-07-05")
    )
    print(len(res))
    assert len(res) == 75
