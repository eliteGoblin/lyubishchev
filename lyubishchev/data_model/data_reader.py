import re
from abc import ABC, abstractmethod
from datetime import datetime

import arrow
from arrow import Arrow

from lyubishchev import config
from lyubishchev.data_model.day import DayRecord
from lyubishchev.data_model.event import Event


def must_yyyy_mm_dd(date_str: str) -> None:
    date_pattern: str = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    if re.search(date_pattern, date_str) is None:
        raise ValueError("date string should follow YYYY-MM-DD strictly")


def date_range_to_timestamp_range(
    start_date: str, end_date: str  # pylint: disable=unused-argument
) -> tuple[Arrow, Arrow]:
    """
    Allow user to provide date in strictly string format: YYYY-MM-DD, e.g
    [2022-07-02, 2022-07-03), to get a data within a day or days
    end_date should be at least one day later than start date
    Return timestamp for string date, in config's timezone
        Start timestamp: start date 00:00, to include start day's wakeup
        End timestamp:   end date 18:00, ensure we include start day's bedtime,
        but exclude end date's bedtime
    """
    # Explicitly format checking , instead of relying on datetime parse
    must_yyyy_mm_dd(start_date)
    must_yyyy_mm_dd(end_date)

    start_timestamp: Arrow = arrow.get(
        datetime.fromisoformat(start_date + " 00:00"),
        config.get_iana_timezone_name(),
    )
    end_timestamp: Arrow = arrow.get(
        datetime.fromisoformat(end_date + " 18:00"),
        config.get_iana_timezone_name(),
    )
    if start_date >= end_date:  # strictly follow YYYY-MM-DD, string compare is enough
        raise ValueError(f"start date: {start_date} should before end date: {end_date}")
    return start_timestamp, end_timestamp


class DataReader(ABC):
    """
    For query data which is in a certain date range, i.e unit is a day
    This is a higher level, smarter data reader(compared to lower-level Clockify Fetcher
        which blindly return data within timestamp range)

    DataReader: provide date-string friendly query interface, unit is a day
    ^
    ClockifyFetcher: return TimeIntervals and Events of certain timestamp range
    ^
    ClockifyAPI

    Contain logic:
        Move low level time series into higher level user data, e.g days
        Various possible queries
        Possible cache layer to accelerate query
    """

    @abstractmethod
    def get_day_records(self, start_date: str, end_date: str) -> list[DayRecord]:
        """
        Get day records
        date format must by YYYY-MM-DD, [start, end), excluding end;

        when implement, could use date_range_to_timestamp_range to get timestamp from date str
        """

    @abstractmethod
    def fetch_last_event(self, timestamp: Arrow, typ: str, tag: str = "") -> Event:
        """
        Get when was the last event which matches criteria
        """
