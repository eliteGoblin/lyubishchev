import sys

from icecream import ic  # type: ignore

from lyubishchev.clockify_fetcher import ClockifyConfig, ClockifyFetcher
from lyubishchev.data_model import (
    Event,
    TimeInterval,
    date_range_to_timestamp_range,
    parse_and_generate_day_records,
)
from lyubishchev.report import DayRangeReport


def main() -> int:
    config: ClockifyConfig = ClockifyConfig()
    start_date: str = "2023-03-12"
    end_date: str = "2023-03-17"

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
    day_records = parse_and_generate_day_records(
        start_date=start_date,
        end_date=end_date,
        time_intervals=time_intervals,
        events=events,
    )

    report = DayRangeReport(
        day_records=day_records,
    )

    ic(report.get_time_stats())
    ic(report.get_interval_metrics())
    ic(report.get_event_metrics())

    return 0


if __name__ == "__main__":
    sys.exit(main())
