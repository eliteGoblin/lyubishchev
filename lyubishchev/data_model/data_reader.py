from abc import ABC, abstractmethod

from arrow import Arrow

from lyubishchev.data_model.day import DayRecord
from lyubishchev.data_model.event import Event
from lyubishchev.data_model.time_interval import TimeInterval


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
        Possible cache layer to accelerate query, created when init (specify date range)

    Features:
        date-string, day unit interface
        query, filter by label, tag
    """

    @abstractmethod
    def get_day_records(self, start_date: str, end_date: str) -> list[DayRecord]:
        """
        Get day records
        date format must by YYYY-MM-DD, [start, end), excluding end;

        when implement, could use date_range_to_timestamp_range to get timestamp from date str
        """

    @abstractmethod
    def fetch_last_time_interval(
        self, timestamp: Arrow, typ: str, tag: str = ""
    ) -> TimeInterval:
        """
        Get when was the last event which matches criteria
        """

    @abstractmethod
    def fetch_last_event(self, timestamp: Arrow, typ: str, tag: str = "") -> Event:
        """
        Get when was the last event which matches criteria
        """
