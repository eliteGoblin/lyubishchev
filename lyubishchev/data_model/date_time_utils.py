import re
from datetime import datetime

import arrow
from arrow import Arrow

from lyubishchev import config

date_str_fmt: str = "YYYY-MM-DD"


def must_yyyy_mm_dd(date_str: str) -> None:

    date_pattern: str = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    if re.search(date_pattern, date_str) is None:
        raise ValueError("date string should follow YYYY-MM-DD strictly")


def time_diff_minutes(start: Arrow, end: Arrow) -> int:
    return int((end - start).seconds / 60)


def day_start_timestamp_early_bound(timezone_name: str, start_date: str) -> Arrow:
    """
    Return earliest timestamp for a particular day's start(wakeup event)
        i.e search for wakeup after this timestamp, for that day
        i.e that day's wakeup will never early than return timestamp
    """
    return arrow.get(
        datetime.fromisoformat(start_date + " 00:00"),
        timezone_name,
    )


def day_end_timestamp_late_bound(timezone_name: str, end_date: str) -> Arrow:
    """
    Return latest bound timestamp for last day(one day before end day)'s end(sleep event),
        last means inclusive, while end means exclusive
        i.e search for last day's bed event before end day's 18:00 (possible to happen,
            but should getup before it event I stay-up all the night)
    """
    return arrow.get(
        datetime.fromisoformat(end_date + " 18:00"),
        timezone_name,
    )


def date_str_from_timestamp(
    timezone_name: str, timestamp: Arrow, date_fmt: str = date_str_fmt
) -> str:
    return timestamp.to(timezone_name).format(date_fmt)


def timestamp_from_date_str(timezone_name: str, date_str: str) -> Arrow:
    must_yyyy_mm_dd(date_str)
    return arrow.get(date_str, date_str_fmt, tzinfo=timezone_name)


def next_day(timezone_name: str, date_str: str) -> str:
    must_yyyy_mm_dd(date_str)
    return date_str_from_timestamp(
        timezone_name=timezone_name,
        timestamp=timestamp_from_date_str(
            timezone_name=timezone_name,
            date_str=date_str,
        ).shift(days=1),
    )


def previous_day(timezone_name: str, date_str: str) -> str:
    must_yyyy_mm_dd(date_str)
    return date_str_from_timestamp(
        timezone_name=timezone_name,
        timestamp=timestamp_from_date_str(
            timezone_name=timezone_name,
            date_str=date_str,
        ).shift(days=-1),
    )


def date_range_to_timestamp_range(
    start_date: str, end_date: str, buffer_days: int = 0
) -> tuple[Arrow, Arrow]:
    """
    Allow user to provide date in strictly string format: YYYY-MM-DD, e.g
    [2022-07-02, 2022-07-03), to get a data within a day or days
    end_date should be at least one day later than start date
    Parameters:
        start_date: start day
        end_date: end day, one day past last day interested, i.e not including in range
        buffer_days: non-negative, extra days will be added to both start_date and end_date, e.g
            [7.1, 7.2) buffer 2 days will be [6.29, 7.4)
    Return timestamp for string date, in config's timezone
        Start timestamp: start date 00:00, to include start day's wakeup
        End timestamp:   end date 18:00, ensure we include last day(the day before end)'s bedtime,
        but exclude end date's bedtime
    Throws: ValueError
    """
    # Explicitly format checking , instead of relying on datetime parse
    must_yyyy_mm_dd(start_date)
    must_yyyy_mm_dd(end_date)
    if buffer_days < 0:
        raise ValueError(f"buffer_days should be non-negative, got {buffer_days}")

    timezone_name: str = config.get_iana_timezone_name()
    start_timestamp: Arrow = day_start_timestamp_early_bound(timezone_name, start_date)
    end_timestamp: Arrow = day_end_timestamp_late_bound(timezone_name, end_date)

    if start_date >= end_date:  # strictly follow YYYY-MM-DD, string compare is enough
        raise ValueError(f"start date: {start_date} should before end date: {end_date}")
    # add buffer to both start and end, if any
    return start_timestamp.shift(days=-1 * buffer_days), end_timestamp.shift(
        days=buffer_days
    )