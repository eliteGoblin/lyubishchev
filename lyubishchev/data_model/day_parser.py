from arrow import Arrow

from lyubishchev import config

from .core_data_structure import TimeSeriesNotFound
from .data_validator import (
    must_single_day_events,
    must_single_day_time_intervals,
    must_time_order,
)
from .date_time_utils import (
    date_str_from_timestamp,
    day_start_timestamp_early_bound,
    must_yyyy_mm_dd,
    next_day,
    time_diff_minutes,
)
from .day import DayEvents, DayRecord
from .event import Event
from .event_data import EVENT_TYPE, TYPE_BED, TYPE_GETUP, TYPE_WAKEUP
from .search_time_series import find_first_match
from .time_interval import TimeInterval


def remove_wakeup_getup_bed_from_day_events(day_events: list[Event]) -> list[Event]:
    """
    strip wakeup, getup, bed events in given events, they'll become part of DayRecord
    Parameters:
        day_events: events belong to a single day, sorted with timestamp ascending
    Returns:
        stripped events, won't contain any bed related events
    Raises:
        ValueError upon invalid input
    """
    final_events: list[Event] = []

    for event in day_events:
        if EVENT_TYPE in event.metadata.label and event.metadata.label[EVENT_TYPE] in (
            TYPE_WAKEUP,
            TYPE_GETUP,
            TYPE_BED,
        ):
            continue

        final_events.append(event)
    return final_events


def get_events_for_single_day(
    date_range_events: list[Event],
    date: str,
) -> list[Event]:
    """
    events MUST be logically in that day:
        wakeup event MUST in that day
        getup event MUST in that day
        bed event MUST in that day or next day(sleep time is after 00:00)
    """

    # searching starts at start_date's 00:00
    timezone_name: str = config.get_iana_timezone_name()
    day_search_start_timestamp: Arrow = day_start_timestamp_early_bound(date)

    # following events are key indicator of time to generate day record
    wakeup_index: int
    last_night_bed_index: int
    bed_index: int

    wakeup_index = find_first_match(
        sequence=date_range_events,
        search_start_timestamp=day_search_start_timestamp,
        label={
            EVENT_TYPE: TYPE_WAKEUP,
        },
    )

    wakeup_date: str = date_str_from_timestamp(
        timezone_name=config.get_iana_timezone_name(),
        timestamp=date_range_events[wakeup_index].timestamp,
    )
    if wakeup_date != date:
        raise ValueError(f"date {date} doesn't match wakeup event's date {wakeup_date}")

    last_night_bed_index = find_first_match(
        sequence=date_range_events,
        search_start_timestamp=date_range_events[wakeup_index].timestamp,
        reverse=True,
        label={
            EVENT_TYPE: TYPE_BED,
        },
    )

    bed_index = find_first_match(
        sequence=date_range_events,
        search_start_timestamp=date_range_events[wakeup_index].timestamp,
        label={
            EVENT_TYPE: TYPE_BED,
        },
    )

    timezone_name = config.get_iana_timezone_name()

    bed_date: str = date_str_from_timestamp(
        timezone_name=timezone_name,
        timestamp=date_range_events[wakeup_index].timestamp,
    )
    if bed_date != date and bed_date != next_day(timezone_name, date):
        raise ValueError(
            f"bed event's date {bed_date} should be same as {date} or it's next day"
        )

    return date_range_events[last_night_bed_index : bed_index + 1]


def get_time_intervals_for_single_day(
    date_range_intervals: list[TimeInterval],
    current_day_events: list[Event],
) -> list[TimeInterval]:
    """
    Note:
        since events ensured in single day, no need to check here
    """
    # use timestamp from key events(wakeup, bed) to cut time intervals for current day
    # skip the time intervals start from today's bed time event, means it's next day's first time interval
    day_events: DayEvents = DayEvents(current_day_events)
    start_interval_index = find_first_match(
        sequence=date_range_intervals,
        search_start_timestamp=day_events.get_wakeup_event().timestamp,
    )
    try:
        end_interval_index = find_first_match(
            # first interval record after bed time of today, means first time interval for next day\
            # (which should include wakeup event).
            sequence=date_range_intervals,
            search_start_timestamp=day_events.get_bed_event().timestamp,
        )
    except TimeSeriesNotFound:
        # if can't find records happen after last day's bed, means last time_interval contain last day's bed event,
        # use it as end
        end_interval_index = len(date_range_intervals)

    return date_range_intervals[start_interval_index:end_interval_index]


def parse_and_generate_day_record(
    single_day_events: list[Event],
    single_day_time_intervals: list[TimeInterval],
) -> DayRecord:
    """
    parse and generate single day record, providing events and time_interval EXACTLY for that day
    Parameters:
        single_day_events: events of single day, see must_single_day_events
        single_day_time_intervals: time entries records, MUST include time_interval entry in following order:
            First is wakeup entry, MUST start after wakeup event
            Last is last time interval of day, MUST finish before bed event
    raise:
        TimeSeriesNotFound if key time series missing
    """
    must_single_day_events(single_day_events=single_day_events)
    must_single_day_time_intervals(
        single_day_events=single_day_events,
        single_day_time_intervals=single_day_time_intervals,
    )

    day_events: DayEvents = DayEvents(single_day_events)

    return DayRecord(
        wakeup_timestamp=day_events.get_wakeup_event().timestamp,
        getup_timestamp=day_events.get_getup_event().timestamp,
        bed_timestamp=day_events.get_bed_event().timestamp,
        last_night_sleep_minutes=time_diff_minutes(
            start=day_events.get_previous_day_bed_event().timestamp,
            end=day_events.get_wakeup_event().timestamp,
        ),
        time_intervals=single_day_time_intervals,
        events=remove_wakeup_getup_bed_from_day_events(single_day_events),
    )


def parse_and_generate_day_records(
    start_date: str,
    end_date: str,
    events: list[Event],
    time_intervals: list[TimeInterval],
) -> list[DayRecord]:
    """
    parse_and_generate_day_records:
        favor explicit over implicit, i.e buffered range
        first events much be last night's bed event
    Parameters:
        start_date: first day of return list[DayRecord]
        end_date: day past last day return(DayRecords[-1])
        events:
            list of events containing [start_date, end_date), e.g date range is [2022-10-27, 2022-10-29)
            events is important, use wakeup, bed event to breakup a day
                MUST in time order
                MUST contain the day before start_date's bedtime
                MUST contain last day's bed time
                MUST include wakeup, bed event for each day [start_date, last_day], i.e last event should
                    at least include last day's bed event
        time_intervals: TimeIntervals for a selected date range
            MUST in time order
            MUST NO overlapping for any 2 TimeIntervals
    Return:
        day records generated from input:
            first day must be start_date; last day must be one day before end_date
    Throws:
        ValueError for any data issue
    """
    must_yyyy_mm_dd(start_date)
    must_yyyy_mm_dd(end_date)
    if start_date >= end_date:
        raise ValueError(f"start date {start_date} must before end date {end_date} ")
    must_time_order(time_intervals)
    must_time_order(events)

    day_records: list[DayRecord] = []

    # Split events by marking wakeup, bed event
    # Searching stops when last day complete, i.e last day's bed event reached
    to_parse_date: str = start_date
    while True:
        events_for_current_day: list[Event] = get_events_for_single_day(
            date_range_events=events, date=to_parse_date
        )

        time_intervals_for_current_day: list[TimeInterval] = (
            get_time_intervals_for_single_day(
                date_range_intervals=time_intervals,
                current_day_events=events_for_current_day,
            )
        )

        day_record: DayRecord = parse_and_generate_day_record(
            single_day_events=events_for_current_day,
            single_day_time_intervals=time_intervals_for_current_day,
        )

        day_records.append(day_record)

        # if last day been parsed, stop
        next_day_date: str = next_day(
            timezone_name=config.get_iana_timezone_name(),
            date_str=day_record.date_str(),
        )
        if next_day_date == end_date:
            break
        to_parse_date = next_day_date

    return day_records
