import re
from datetime import timedelta
from typing import cast

import pandas as pd
from arrow import Arrow

from lyubishchev.report.report import DayRangeReport

from .habit_protocol import Habit

# Use builtins.int to avoid mypy false positive and module indexing error


class GetupHabit(Habit):
    """
    GetupHabit computes the difference in minutes between a target getup time (in "HH:MM" 24hr format)
    and the actual getup time for each day in a DayRangeReport.
    The score is (target - actual) in minutes, positive if earlier than target, negative if later.
    Returns a pandas Series with a DatetimeIndex.
    """

    def __init__(self, report: DayRangeReport, target_time: str) -> None:
        """
        Args:
            report: DayRangeReport containing day records.
            target_time: Target getup time in "HH:MM" 24hr format (e.g., "07:00").
        Raises:
            ValueError: If target_time is not in valid 24hr 'HH:MM' format.
        """
        self.report = report
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", target_time):
            raise ValueError(
                f"target_time '{target_time}' is not in valid 24hr 'HH:MM' format"
            )
        self.target_time = target_time

    def data(self) -> "pd.Series[int]":
        """
        Returns:
            pd.Series: Index is date string, value is (target - actual getup) in minutes (signed).
        """
        dates: list[str] = []
        values: list[int] = []
        target_hour, target_minute = map(int, self.target_time.split(":"))

        for day in self.report.day_records:
            getup: Arrow = day.getup_timestamp
            # Construct target time on the same day as getup
            target_today = getup.replace(
                hour=target_hour, minute=target_minute, second=0, microsecond=0
            )
            delta: timedelta = cast(timedelta, target_today - getup)
            diff = int(delta.total_seconds() // 60)

            dates.append(day.date_str())
            values.append(diff)
        # Ensure DatetimeIndex for calplot compatibility
        return pd.Series(values, index=pd.to_datetime(dates))  # type: ignore[attr-defined]
