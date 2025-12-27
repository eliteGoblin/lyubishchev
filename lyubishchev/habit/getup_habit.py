import re
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import cast

import pandas as pd
from arrow import Arrow

from lyubishchev.data_model.day import DayRecord
from lyubishchev.report.report import DayRangeReport

from .habit_protocol import Habit


class TimeHabit(ABC, Habit):
    """
    Base class for time-based habits (GetupHabit, BedHabit).
    Computes the difference in minutes between a target time and actual time.
    Implements Habit protocol while providing shared logic for
    time-based habits.
    """

    def __init__(self, report: DayRangeReport, target_time: str) -> None:
        """
        Args:
            report: DayRangeReport containing day records.
            target_time: Target time in "HH:MM" 24hr format (e.g., "07:00").
        Raises:
            ValueError: If target_time is not in valid 24hr 'HH:MM' format.
        """
        self.report = report
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", target_time):
            raise ValueError(
                f"target_time '{target_time}' is not in valid 24hr " f"'HH:MM' format"
            )
        self.target_time = target_time
        self.target_hour, self.target_minute = map(int, target_time.split(":"))

    @abstractmethod
    def get_timestamp(self, day: DayRecord) -> Arrow:
        """Get the relevant timestamp from the day record."""

    @abstractmethod
    def calculate_score(self, target: Arrow, actual: Arrow) -> int:
        """Calculate the habit score. Higher score = better habit."""

    def get_target_reference_timestamp(self, day: DayRecord) -> Arrow:
        """
        Get the reference timestamp for constructing target time.
        Subclasses can override to use a different reference.
        Default: use the actual timestamp (from get_timestamp).
        """
        return self.get_timestamp(day)

    def data(self) -> "pd.Series[int]":
        """
        Returns:
            pd.Series: Index is date string, value is habit score in minutes.
        """
        dates: list[str] = []
        values: list[int] = []

        for day in self.report.day_records:
            actual_time: Arrow = self.get_timestamp(day)
            # Construct target time based on reference timestamp
            reference = self.get_target_reference_timestamp(day)
            target_today = reference.replace(
                hour=self.target_hour,
                minute=self.target_minute,
                second=0,
                microsecond=0,
            )
            score = self.calculate_score(target_today, actual_time)
            dates.append(day.date_str())
            values.append(score)
        # Ensure DatetimeIndex for calplot compatibility
        return pd.Series(values, index=pd.to_datetime(dates))  # type: ignore[attr-defined]


class GetupHabit(TimeHabit):
    """
    GetupHabit computes the difference in minutes between a target getup time
    and actual getup time. Score = (target - actual) in minutes,
    positive if earlier than target (good habit).
    """

    def get_timestamp(self, day: DayRecord) -> Arrow:
        """Get the getup timestamp from the day record."""
        return day.getup_timestamp

    def calculate_score(self, target: Arrow, actual: Arrow) -> int:
        """Earlier getup (actual < target) gives positive score."""
        delta: timedelta = cast(timedelta, target - actual)
        return int(delta.total_seconds() // 60)


class BedHabit(TimeHabit):
    """
    BedHabit computes the difference in minutes between actual bed time and
    target bed time. Score = (actual - target) in minutes,
    positive if earlier than target (good habit).
    """

    def get_timestamp(self, day: DayRecord) -> Arrow:
        """Get the bed timestamp from the day record."""
        return day.bed_timestamp

    def get_target_reference_timestamp(self, day: DayRecord) -> Arrow:
        """
        Use wakeup_timestamp for target reference since bed_timestamp may be
        past midnight (next calendar day) but still belongs to the same logical day.
        """
        return day.wakeup_timestamp

    def calculate_score(self, target: Arrow, actual: Arrow) -> int:
        """Earlier bed time (actual < target) gives positive score."""
        delta: timedelta = cast(timedelta, actual - target)
        # Invert: earlier bed time (actual < target) = positive score
        return -int(delta.total_seconds() // 60)
