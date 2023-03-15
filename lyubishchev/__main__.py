import sys

from lyubishchev.clockify_fetcher import ClockifyConfig, ClockifyFetcher
from lyubishchev.data_model import Event, TimeInterval, date_range_to_timestamp_range


def main() -> int:
    config: ClockifyConfig = ClockifyConfig()
    start_date: str = "2022-08-16"
    end_date: str = "2022-08-17"

    time_intervals: list[TimeInterval]
    events: list[Event]

    clockify_fetcher: ClockifyFetcher = ClockifyFetcher(config)
    time_intervals, events = clockify_fetcher.fetch_time_intervals_events(
        *date_range_to_timestamp_range(
            start_date=start_date,
            end_date=end_date,
            buffer_days=1,
        )
    )

    print(time_intervals, events)

    return 0


if __name__ == "__main__":
    sys.exit(main())
