import pandas as pd

from lyubishchev.report.report import DayRangeReport

from .habit_protocol import Habit


class TimeIntervalCounterHabit(Habit):
    """
    TimeIntervalCounterHabit counts the number of time intervals per day whose label contains
    the specified key. Returns a pandas Series with a DatetimeIndex.
    """

    def __init__(self, report: DayRangeReport, key: str) -> None:
        """
        Args:
            report: DayRangeReport containing day records.
            key: The label key to match in each time interval.
        """
        self.report = report
        self.key = key

    def data(self) -> "pd.Series[int]":
        """
        Returns:
            pd.Series: Index is DatetimeIndex (one per day), value is the count of matching intervals.
        """
        dates: list[str] = []
        counts: list[int] = []
        for day in self.report.day_records:
            count = 0
            for interval in day.time_intervals:
                if self.key in interval.metadata.label:
                    count += 1
            dates.append(day.date_str())
            counts.append(count)
        return pd.Series(counts, index=pd.to_datetime(dates))  # type: ignore[attr-defined]
