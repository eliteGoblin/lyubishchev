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
    return int((end - start).total_seconds() / 60)


def day_start_timestamp_early_bound(
    start_date: str, timezone_name: str = config.get_iana_timezone_name()
) -> Arrow:
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
    timestamp: Arrow,
    date_fmt: str = date_str_fmt,
    timezone_name: str = config.get_iana_timezone_name(),
) -> str:
    return timestamp.to(timezone_name).format(date_fmt)


def timestamp_from_date_str(
    date_str: str, timezone_name: str = config.get_iana_timezone_name()
) -> Arrow:
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


def get_day_range_from_relative_days(
    start_date: str,
    days_delta: int,
    lower_bound_applied: bool = False,
) -> tuple[str, str]:
    """
    get day range from relative days;
    Args:
        days_delta: means how many days I want to be in rage [start, end) can be both positive and negative
            e.g I want days_delta=-2, I want to see past 2 days (NOT including today)'s data: today - 2d, today - 1d;
            so it should return [today -2d, today)
    Return:
        actual date range, earlier day first
    """
    must_yyyy_mm_dd(start_date)
    calculate_starte = timestamp_from_date_str(
        timezone_name=config.get_iana_timezone_name(),
        date_str=start_date,
    )
    the_other_timestamp = calculate_starte.shift(days=days_delta)
    the_other_date = date_str_from_timestamp(
        timezone_name=config.get_iana_timezone_name(),
        timestamp=the_other_timestamp,
    )

    if days_delta > 0:
        return (
            start_date,
            the_other_date,
        )  # doesn't matter return date that later than today
    if lower_bound_applied and the_other_date < config.get_date_lower_bound():
        the_other_date = config.get_date_lower_bound()
    return the_other_date, start_date


def get_day_range_from_relative_weeks(
    start_date_str: str, week_offset: int
) -> tuple[str, str]:
    """
    0 means show current week(til yesterday: last recorded day)
    -1 means last week, etc
    Return:
        res[0]: start date in YYYY-MM-DD format
        res[1]: end date in YYYY-MM-DD format(exclusive)
    Info:
        arrow treat Monday as first day of week, instead of Sunday
    """
    if week_offset > 0:
        raise ValueError(f"week_offset should be non-positive, got {week_offset}")

    start_date = arrow.get(start_date_str).to(config.get_iana_timezone_name())

    if start_date.format("d") == "7":  # '7' represents Sunday in the 'd' format
        start_of_start_date_week = start_date
    else:
        start_of_start_date_week = start_date.floor("week").shift(days=-1)  # Sunday

    start_of_res_week = start_of_start_date_week.shift(weeks=week_offset)
    end_of_res_week = (
        start_of_res_week.shift(weeks=1) if week_offset != 0 else start_date
    )

    return start_of_res_week.format(date_str_fmt), end_of_res_week.format(date_str_fmt)


def get_day_range_from_relative_months(
    start_date_str: str, month_offset: int
) -> tuple[str, str]:
    """
    0 means show current month(til yesterday: last recorded day)
    -1 means last full month, etc
    e.g For June 10, 2023, month_offset=0, return [2023-06-01, 2023-06-10)
    e.g For June 10, 2023, month_offset=-1, return [2023-05-01, 2023-06-01)
    Return:
        res[0]: start date in YYYY-MM-DD format
        res[1]: end date in YYYY-MM-DD format(exclusive)
    """
    if month_offset > 0:
        raise ValueError(f"month_offset should be non-positive, got {month_offset}")

    start_date = arrow.get(start_date_str).to(config.get_iana_timezone_name())
    if month_offset == 0:
        return (start_date.floor("month").format(date_str_fmt), start_date_str)

    start_of_month = start_date.shift(months=month_offset).floor("month")
    end_of_month = start_of_month.shift(months=1).format(date_str_fmt)
    return (start_of_month.format(date_str_fmt), end_of_month)


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
    Note:
        buffer is to fetch the day before start_date's bed time, to calculate start day's sleep
    """
    # Explicitly format checking , instead of relying on datetime parse
    must_yyyy_mm_dd(start_date)
    must_yyyy_mm_dd(end_date)
    if buffer_days < 0:
        raise ValueError(f"buffer_days should be non-negative, got {buffer_days}")

    timezone_name: str = config.get_iana_timezone_name()
    start_timestamp: Arrow = day_start_timestamp_early_bound(start_date)
    end_timestamp: Arrow = day_end_timestamp_late_bound(timezone_name, end_date)

    if start_date >= end_date:  # strictly follow YYYY-MM-DD, string compare is enough
        raise ValueError(f"start date: {start_date} should before end date: {end_date}")
    # add buffer to both start and end, if any
    return start_timestamp.shift(days=-1 * buffer_days), end_timestamp.shift(
        days=buffer_days
    )
