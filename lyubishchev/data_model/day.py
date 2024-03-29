from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Callable, List

import arrow
from arrow import Arrow

from lyubishchev import config
from lyubishchev.data_model.date_time_utils import date_str_from_timestamp
from lyubishchev.data_model.event import Event
from lyubishchev.data_model.event_data import (
    EVENT_TYPE,
    TYPE_BED,
    TYPE_GETUP,
    TYPE_WAKEUP,
)
from lyubishchev.data_model.time_interval import TimeInterval

from .core_data_structure import TimeSeriesNotFound
from .search_time_series import find_first_match


class DayEvents:
    """DayEvents represent events in a day"""

    current_day_events: list[Event]

    def __init__(self, single_day_events: list[Event]) -> None:
        self.current_day_events = single_day_events

    def __len__(self) -> int:
        return len(self.current_day_events)

    def __getitem__(self, index: int) -> Event:
        return self.current_day_events[index]

    def get_previous_day_bed_event(self) -> Event:
        return self.current_day_events[0]

    def get_wakeup_event(self) -> Event:
        wakeup_event_index: int = find_first_match(
            sequence=self.current_day_events,
            search_start_timestamp=self.get_previous_day_bed_event().timestamp,
            label={
                EVENT_TYPE: TYPE_WAKEUP,
            },
        )
        return self.current_day_events[wakeup_event_index]

    def get_getup_event(self) -> Event:
        wakeup_event: Event = self.get_wakeup_event()
        getup_event_index: int
        try:
            getup_event_index = find_first_match(
                sequence=self.current_day_events,
                search_start_timestamp=wakeup_event.timestamp,
                label={
                    EVENT_TYPE: TYPE_GETUP,
                },
            )
        except TimeSeriesNotFound:
            return wakeup_event  # no getup, means no time spent on bed before getup, after wake up
        return self.current_day_events[getup_event_index]

    def get_bed_event(self) -> Event:
        bed_event_index: int = find_first_match(
            sequence=self.current_day_events,
            search_start_timestamp=self.get_wakeup_event().timestamp,
            label={
                EVENT_TYPE: TYPE_BED,
            },
        )
        return self.current_day_events[bed_event_index]


class InvalidDayRecord(Exception):
    """
    Exception raised indicating DayRecord is invalid
    """


@dataclass
class DayRecord:
    """
    DayRecord object is for tracking day key data, time intervals, and events
    DayRecord range between wakeup event and bed event,
        not necessarily within [0:00-23:59]
        wakeup time's date is same with date of Day
    events: without wakeup, getup, bed events, they'll become part of DayRecord
    """

    timezone_name: str
    wakeup_timestamp: Arrow
    getup_timestamp: Arrow
    bed_timestamp: Arrow
    last_night_sleep_minutes: int
    time_intervals: List[TimeInterval]
    events: List[Event]

    def __init__(self, **kwargs: Any) -> None:
        valid_keys: List[str] = [
            "timezone_name",
            "wakeup_timestamp",
            "getup_timestamp",
            "bed_timestamp",
            "last_night_sleep_minutes",
            "time_intervals",
            "events",
        ]
        # let kwargs overwrite default values
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
        # default as global timezone
        if self.timezone_name is None:
            self.timezone_name = config.get_iana_timezone_name()

    def __repr__(self) -> str:
        return f"""
        DayRecord(
            timezone_name={self.timezone_name},
            day_str={self.date_str()},
            wakeup_timestamp={self.wakeup_timestamp},
            getup_timestamp={self.getup_timestamp},
            bed_timestamp={self.bed_timestamp},
            last_night_sleep_minutes={self.last_night_sleep_minutes},
            time_intervals={self.time_intervals},
            events={self.events},
        )
        """

    def date_str(self) -> str:
        """
        local date matters: what's the local date when time recorded
        """
        if self.wakeup_timestamp is None:
            raise ValueError(f"{self} should contain wakeup_timestamp")
        return date_str_from_timestamp(
            timezone_name=config.get_iana_timezone_name(),
            timestamp=self.wakeup_timestamp,
        )

    @property
    def day_length_minutes(self) -> int:
        return int((self.bed_timestamp - self.wakeup_timestamp).seconds / 60)

    @property
    def recorded_minutes(self) -> int:
        """
        recorded_minutes = Sum of duration of TimeIntervals
        """
        return sum(interval.duration_minutes for interval in self.time_intervals)


def validate_required_fields(day_record: DayRecord) -> None:
    """
    throw InvalidDayRecord if missing required fields
    """
    required_fields: List[str] = [
        "wakeup_timestamp",
        "getup_timestamp",
        "bed_timestamp",
        "last_night_sleep_minutes",
        "time_intervals",
    ]
    for key in required_fields:
        if getattr(day_record, key) is None:
            raise InvalidDayRecord(
                f"day record {day_record.date_str()} missing required field {key}"
            )


def validate_value_range(day_record: DayRecord) -> None:
    """
    throw InvalidDayRecord if violating:
    wakeup in range: [03:00, 13:00], same as getup, bed: [19:00, 08:00]
    day length(bedtime - wakeup) in [10h, 19h)
    last_night_sleep_minutes [3h, 13h]
    day length time(sleep - wakeup) [10h, 20h]
    """
    if day_record.wakeup_timestamp.hour < 3 or day_record.wakeup_timestamp.hour > 13:
        raise InvalidDayRecord(
            f"{day_record.date_str()} has invalid wakeup_timestamp {day_record.wakeup_timestamp}"
        )

    if day_record.getup_timestamp.hour < 3 or day_record.getup_timestamp.hour > 13:
        raise InvalidDayRecord(
            f"{day_record.date_str()} has invalid wakeup_timestamp {day_record.wakeup_timestamp}"
        )

    if not (
        19 <= day_record.bed_timestamp.hour <= 23
        or 0 <= day_record.bed_timestamp.hour <= 8
    ):
        raise InvalidDayRecord(
            f"{day_record.date_str()} has invalid bed_timestamp {day_record.bed_timestamp}"
        )

    if not 3 * 60 <= day_record.last_night_sleep_minutes <= 13 * 60:
        raise InvalidDayRecord(
            f"{day_record.date_str()} has invalid bed_timestamp {day_record.bed_timestamp}"
        )

    diff_seconds: int = (day_record.bed_timestamp - day_record.wakeup_timestamp).seconds
    if not 10 * 3600 <= diff_seconds <= 20 * 3600:
        raise InvalidDayRecord(
            f"{day_record.date_str()} has invalid length between {day_record.wakeup_timestamp} "
            f"and {day_record.bed_timestamp}, "
            f"diff {(day_record.bed_timestamp - day_record.wakeup_timestamp).seconds / 3600}"
        )


def validate_time_order(day_record: DayRecord) -> None:
    """
    throw InvalidDayRecord if violating order:
        wakeup <= getup < bed time
    """
    if (
        not day_record.wakeup_timestamp
        <= day_record.getup_timestamp
        < day_record.bed_timestamp
    ):
        raise InvalidDayRecord(f"{day_record.date_str()} timestamp order invalid")


def validate_time_intervals_order(day_record: DayRecord) -> None:
    """
    throw InvalidDayRecord if:
        empty time_intervals
        intervals happen time not in order:
            begin of next time_interval must happens after last interval's finish time
            won't tolerate any human error, should fail fast, also simplify code logic
    """
    if day_record.time_intervals is None or len(day_record.time_intervals) == 0:
        raise InvalidDayRecord(
            f"day record {day_record.date_str()} has empty TimeIntervals"
        )

    unix_epoch: Arrow = arrow.get("1970-01-01T00:00:00+00:00")
    last_timestamp: Arrow = unix_epoch

    for interval in day_record.time_intervals:
        if interval.timestamp < last_timestamp:
            raise InvalidDayRecord(
                f"day record {day_record.date_str()} time interval disorder {interval.timestamp}"
            )
        last_timestamp = interval.timestamp + timedelta(
            minutes=interval.duration_minutes
        )


def validate_events(day_record: DayRecord) -> None:
    """
    throw InvalidDayRecord if violating:
        events NOT contain wakeup, getup, bed.
        intervals happen time in order
    """
    if len(day_record.events) == 0:
        return

    last_timestamp: Arrow = arrow.get("1970-01-01T00:00:00+00:00")
    for event in day_record.events:
        if event.timestamp < last_timestamp:  # allow 5 min human recording error
            raise InvalidDayRecord(
                f"day record {day_record.date_str()} events disorder {event.timestamp}"
            )
        last_timestamp = event.timestamp

        if event.metadata.label[EVENT_TYPE] in [TYPE_WAKEUP, TYPE_GETUP, TYPE_BED]:
            raise InvalidDayRecord(
                f"day record {day_record.date_str()} "
                f"events contains invalid type {event.metadata.label[EVENT_TYPE]}"
            )


def validate_time_intervals_match_events(day_record: DayRecord) -> None:
    """
    throw InvalidDayRecord if violating:
        time_intervals not within [wakeup, getup]
        sum of duration of time_intervals < 0.85 * (bedtime - wakeup)
    """
    if day_record.time_intervals[0].timestamp < day_record.wakeup_timestamp:
        raise InvalidDayRecord(
            f"day record {day_record.date_str()} first interval before "
            f"wakeup {day_record.wakeup_timestamp}"
        )

    if (
        day_record.time_intervals[-1].timestamp
        + timedelta(minutes=day_record.time_intervals[-1].duration_minutes)
        > day_record.bed_timestamp
    ):
        raise InvalidDayRecord(
            f"day record {day_record.date_str()} last interval end after "
            f"bedtime {day_record.bed_timestamp}"
        )

    if day_record.recorded_minutes < 0.85 * day_record.day_length_minutes:
        raise InvalidDayRecord(
            f"day record {day_record.date_str()} recorded minutes {day_record.recorded_minutes} "
            f"less than 0.85 of day length: {day_record.day_length_minutes}"
        )


def validate_day_record(day: DayRecord) -> None:

    verifiers: list[Callable[[DayRecord], None]] = [
        validate_required_fields,
        validate_value_range,
        validate_time_order,
        validate_time_intervals_order,
        validate_events,
        validate_time_intervals_match_events,
    ]
    for verifier in verifiers:
        verifier(day)
