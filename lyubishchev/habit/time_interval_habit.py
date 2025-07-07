import pandas as pd

from lyubishchev.report.report import DayRangeReport

from .habit_protocol import Habit


class TimeIntervalHabit(Habit):
    """
    TimeIntervalHabit computes the total duration (in minutes) per day for time intervals
    whose label contains the specified key. Returns a pandas Series with a DatetimeIndex.
    """

    def __init__(self, report: DayRangeReport, key: str) -> None:
        self.report = report
        self.key = key

    def data(self) -> "pd.Series[int]":
        dates: list[str] = []
        values: list[int] = []
        for day in self.report.day_records:
            total = 0
            for interval in day.time_intervals:
                if self.key in interval.metadata.label:
                    total += interval.duration_minutes
            dates.append(day.date_str())
            values.append(total)
        # Ensure DatetimeIndex for calplot compatibility
        return pd.Series(values, index=pd.to_datetime(dates))  # type: ignore[attr-defined]
