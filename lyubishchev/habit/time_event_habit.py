import pandas as pd

from lyubishchev.report.report import DayRangeReport

from .habit_protocol import Habit


class TimeEventHabit(Habit):
    """
    TimeEventHabit counts the number of events per day whose label contains the specified key.
    Returns a pandas Series with a DatetimeIndex.
    """

    def __init__(self, report: DayRangeReport, key: str) -> None:
        self.report = report
        self.key = key

    def data(self) -> "pd.Series[int]":
        dates: list[str] = []
        values: list[int] = []
        for day in self.report.day_records:
            count = 0
            for event in day.events:
                if self.key in event.metadata.label:
                    count += 1
            dates.append(day.date_str())
            values.append(count)
        # Ensure DatetimeIndex for calplot compatibility
        return pd.Series(values, index=pd.to_datetime(dates))  # type: ignore[attr-defined]
