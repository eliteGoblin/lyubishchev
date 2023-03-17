from lyubishchev.clockify_fetcher import ClockifyConfig, ClockifyFetcher
from lyubishchev.data_model import (
    Event,
    TimeInterval,
    date_range_to_timestamp_range,
    parse_and_generate_day_records,
)
from lyubishchev.report import DayRangeReport


def get_report(start_date: str, end_date: str) -> DayRangeReport:
    """
    generate report for a given day range
    """
    time_intervals: list[TimeInterval]
    events: list[Event]

    clockify_fetcher: ClockifyFetcher = ClockifyFetcher(ClockifyConfig())
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

    return report
