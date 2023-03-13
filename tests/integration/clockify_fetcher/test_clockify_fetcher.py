from lyubishchev.clockify_fetcher import ClockifyConfig, ClockifyFetcher
from lyubishchev.data_model import date_range_to_timestamp_range

config: ClockifyConfig = ClockifyConfig()


def test_fetch_raw_time_series_single_day() -> None:
    fetcher: ClockifyFetcher = ClockifyFetcher(config)
    res = fetcher.fetch_raw_time_series(
        *date_range_to_timestamp_range(
            "2022-07-02", "2022-07-03"
        )  # get [7.2, 7.3), 1 day
    )
    assert len(res) == 30


def test_fetch_raw_time_series_3_days() -> None:
    fetcher: ClockifyFetcher = ClockifyFetcher(config)
    res = fetcher.fetch_raw_time_series(
        *date_range_to_timestamp_range("2022-07-02", "2022-07-05")
    )
    assert len(res) == 75
