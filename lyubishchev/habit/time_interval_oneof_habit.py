import pandas as pd

from lyubishchev.report.report import DayRangeReport

from .habit_protocol import Habit


class TimeIntervalOneofHabit(Habit):
    """
    TimeIntervalOneofHabit computes the total duration (in minutes) per day for any
    time interval whose label matches at least one key in the provided list.
    Returns a pandas Series with a DatetimeIndex.
    """

    def __init__(self, report: DayRangeReport, keys: list[str]) -> None:
        """
        Args:
            report: DayRangeReport containing day records.
            keys: List of label keys; if any appears in an interval's label, that interval is counted.
        """
        self.report = report
        self.keys = keys

    def data(self) -> "pd.Series[int]":
        """
        Returns:
            pd.Series: Index is DatetimeIndex (one per day), value is total duration
                        of intervals matching any of the keys (in minutes).
        """
        dates: list[str] = []
        values: list[int] = []
        for day in self.report.day_records:
            total = 0
            for interval in day.time_intervals:
                # sum duration if any key matches
                if any(key in interval.metadata.label for key in self.keys):
                    total += interval.duration_minutes
            dates.append(day.date_str())
            values.append(total)
        # Ensure DatetimeIndex for compatibility
        return pd.Series(values, index=pd.to_datetime(dates))  # type: ignore[attr-defined]
