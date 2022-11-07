from datetime import datetime
from typing import Sequence, Union

import arrow
from arrow import Arrow

from lyubishchev import config

from .date_time_utils import day_end_timestamp_late_bound, previous_day
from .event import Event
from .time_interval import TimeInterval


def must_time_order(entries: Sequence[Union[Event, TimeInterval]]) -> None:
    """
    throw ValueError if:
        order error of entries
        overlap larger than threshold between entries
    """
    last_timestamp: Arrow = arrow.get(
        datetime(
            1970,
            1,
            1,
        )
    )
    for entry in entries:
        if entry.timestamp <= last_timestamp:
            raise ValueError(
                f"entry at {entry.timestamp} earlier than previous entry: {last_timestamp}, from {entries}"
            )
        last_timestamp = entry.timestamp


def must_events_cover_date_range(
    events: list[Event], start_date: str, end_date: str
) -> None:
    """
    check input events match [start_date, end_date), might not need?
    """

    if len(events) < 2:
        raise ValueError(
            f"events {events} needs min size 2 to cover start and end for given date range"
        )

    timezone_name: str = config.get_iana_timezone_name()
    if events[0].timestamp > day_end_timestamp_late_bound(timezone_name, start_date):
        # [7.2, 7.3), start event(say wakeup) could be 7.2 05:30, or 7.2 10:30,
        #   or earlier so shouldn't be later than 7.2 18:00(late bound), since might contain buffer
        raise ValueError(
            f"first event timestamp {events[0].timestamp} should <= {start_date} 18:00"
        )

    end_date_timestamp_lower_bound: Arrow = day_end_timestamp_late_bound(
        timezone_name, previous_day(timezone_name, end_date)
    )

    if events[-1].timestamp <= end_date_timestamp_lower_bound:
        # [7.1, 7.3), end event(say, bed) could be 7.2 23:59, also 7.3 03:30, but shouldn't be
        #   earlier than 7.2 18:00, which miss the 7.2 bed event
        raise ValueError(
            f"last event timestamp {events[-1].timestamp} should > {end_date} - 1's 00:00"
        )


def must_time_intervals_within_events(
    events: list[Event], time_intervals: list[TimeInterval]
) -> None:
    """
    time_intervals records must happen between [events[0], events[-1]]
    might not needed?
    Raises:
        ValueError if violate
    """
    if time_intervals[0].timestamp < events[0].timestamp:
        raise ValueError(
            f"first time interval timestamp {time_intervals[0]} should >= first events {events[0]}"
        )
    if time_intervals[-1].timestamp > events[-1].timestamp:
        raise ValueError(
            f"last time interval timestamp {time_intervals[-1]} should <= last events {events[-1]}"
        )


def must_single_day_events(single_day_events: list[Event]) -> None:
    """
    Validate events for a single day
    Parameters:
        single_day_events: events of that day, rules:
            MUST contain 1 wakeup, 2 bed, 0 or 1 getup
            MUST contain events in following order:
                First is last day's bed event
                Wakeup event
                Optional getup event
                Last is day's bed event
            8 < Bed - wakeup < 24
    raise:
        ValueError if key time series missing
    """
    raise NotImplementedError


def must_single_day_time_intervals(
    single_day_events: list[Event], single_day_time_intervals: list[TimeInterval]
) -> None:
    """
    Validate TimeIntervals for a single day
    Parameters:
        single_day_events: events of same day as TimeIntervals, used to validate TimeIntervals
        single_day_time_intervals: TimeIntervals of that day, rules:
            First TimeInterval starts >= wakeup event
            Last TimeInterval ends <= bed event
    raise:
        ValueError if key time series missing
    """
    raise NotImplementedError
