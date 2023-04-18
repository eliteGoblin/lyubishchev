from typing import Sequence, Union

from arrow import Arrow

from lyubishchev import config

from .date_time_utils import day_end_timestamp_late_bound, previous_day
from .event import Event
from .event_data import EVENT_TYPE, TYPE_BED, TYPE_WAKEUP
from .time_interval import TimeInterval


def must_time_order(entries: Sequence[Union[Event, TimeInterval]]) -> None:
    """
    throw ValueError if:
        order error of entries
        overlap larger than threshold between entries
    """
    for i in range(1, len(entries)):
        if entries[i].timestamp <= entries[i - 1].timestamp:
            raise ValueError(
                f"entry {entries[i]} earlier than previous entry: {entries[i-1]}"
            )


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
        ValueError
    """

    if len(single_day_events) < 3:
        raise ValueError(
            f"single day events {single_day_events} needs min size 3 to cover 1 wakeup, 2 bed"
        )
    if single_day_events[0].metadata.label[EVENT_TYPE] != TYPE_BED:
        raise ValueError(
            f"single day events {single_day_events} should start with last day's bed event, got {single_day_events[0]}"
        )
    if single_day_events[1].metadata.label[EVENT_TYPE] != TYPE_WAKEUP:
        raise ValueError(
            f"single day events index 1 should be wakeup event, got {single_day_events[1]}"
        )
    if single_day_events[-1].metadata.label[EVENT_TYPE] != TYPE_BED:
        raise ValueError(
            f"single day events last index should be bed event, got {single_day_events[-1]}"
        )

    # bed - wakeup should be 8 hr < x < 24 hr
    diff = single_day_events[-1].timestamp - single_day_events[1].timestamp
    secs: int = diff.total_seconds()  # type: ignore

    assert_message = f"day events {single_day_events} invalid"
    assert 8 * 60 * 60 < secs < 24 * 60 * 60, assert_message

    for i, event in enumerate(single_day_events):
        if i in (0, 1, len(single_day_events) - 1):
            continue
        if (
            event.metadata.label[EVENT_TYPE] == TYPE_WAKEUP
            or event.metadata.label[EVENT_TYPE] == TYPE_BED
        ):
            raise ValueError(
                f"single day events {single_day_events} "
                + f"contain extra wakeup or bed event, violating at pos {i}, {event}"
            )


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
            last timeinterval end timestamp - first time interval start timestamp <= 24 hr
    raise:
        ValueError
    """

    assert single_day_time_intervals[0].timestamp >= single_day_events[1].timestamp
    assert single_day_time_intervals[-1].timestamp <= single_day_events[-1].timestamp
    diff = (
        single_day_time_intervals[-1].timestamp - single_day_time_intervals[0].timestamp
    )
    assert diff.total_seconds() <= 24 * 60 * 60  # type: ignore
    # mypy seems can't infer Arrow - Arrow is a datetime.timedelta
