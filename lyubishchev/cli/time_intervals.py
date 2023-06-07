from arrow import Arrow

from lyubishchev.clockify_fetcher import ClockifyConfig, ClockifyFetcher
from lyubishchev.data_model import (
    EVENT_TYPE,
    TYPE_WAKEUP,
    Event,
    TimeInterval,
    date_str_from_timestamp,
    day_start_timestamp_early_bound,
    find_first_match,
)


def fetch_time_intervals_events_since_wakeup(
    timestamp: Arrow,
) -> tuple[list[TimeInterval], list[Event]]:
    time_intervals: list[TimeInterval]
    events: list[Event]

    clockify_fetcher: ClockifyFetcher = ClockifyFetcher(ClockifyConfig())
    today_date_str = date_str_from_timestamp(timestamp)
    today_early_bound_timestamp = day_start_timestamp_early_bound(
        start_date=today_date_str
    )

    time_intervals, events = clockify_fetcher.fetch_time_intervals_events(
        start_timestamp=today_early_bound_timestamp,
        end_timestamp=timestamp,
    )

    wakeup_event_index = find_first_match(
        sequence=events,
        search_start_timestamp=timestamp,
        label={
            EVENT_TYPE: TYPE_WAKEUP,
        },
        reverse=True,
    )

    today_first_time_interval_index = find_first_match(
        sequence=time_intervals,
        search_start_timestamp=events[wakeup_event_index].timestamp,
    )

    return time_intervals[today_first_time_interval_index:], events[wakeup_event_index:]
