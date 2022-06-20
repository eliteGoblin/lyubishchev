from typing import List, Tuple

from arrow import Arrow

from .day import DayRecord
from .event import Event
from .time_interval import TimeInterval


def generate_timestamp_from_date_str(
    start_date: str, end_date: str
) -> Tuple[Arrow, Arrow]:
    raise NotImplementedError


def remove_time_intervals_outside_range(
    time_intervals: List[TimeInterval], start_timestamp: Arrow, end_timestamp: Arrow
) -> List[TimeInterval]:
    """
    return records: [first wakeup timestamp, last bed timestamp]
    """
    raise NotImplementedError


def parse_and_generate_day_records(
    time_intervals: List[TimeInterval],
    events: List[Event],
    previous_night_sleep_minutes: int,
) -> List[DayRecord]:
    """
    events must with first records wakeup, last records with bed
    """
    raise NotImplementedError
