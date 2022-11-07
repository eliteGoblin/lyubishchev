from arrow import Arrow

from lyubishchev.data_model import DataReader, DayRecord, Event, TimeInterval


class CachedDayDataReader(DataReader):
    """
    CachedDayDataReader provide day query interface
    Input:
        day_records: store day records, should with buffer
            at least one day for fetch sleep time day before first day
    """

    day_records: list[DayRecord]

    def __init__(self, day_records: list[DayRecord]):
        self.day_records: list[DayRecord] = day_records

    def get_day_records(self, start_date: str, end_date: str) -> list[DayRecord]:
        """
        Get day records
        date format must by YYYY-MM-DD, [start, end), excluding end;

        when implement, could use date_range_to_timestamp_range to get timestamp from date str
        """
        return []

    def fetch_last_time_interval(
        self, timestamp: Arrow, typ: str, tag: str = ""
    ) -> TimeInterval:
        """
        Get when was the last event which matches criteria
        """
        return TimeInterval()

    def fetch_last_event(self, timestamp: Arrow, typ: str, tag: str = "") -> Event:
        """
        Get when was the last event which matches criteria
        """
        return Event()
