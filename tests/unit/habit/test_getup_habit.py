import pytest

from lyubishchev.habit import BedHabit, GetupHabit
from lyubishchev.report.report import DayRangeReport


def test_getup_habit_on_time(sample_dayrangereport: DayRangeReport) -> None:
    habit = GetupHabit(sample_dayrangereport, "07:00")
    result_series = habit.data()
    # All getup at 7:00, so diff should be 0
    assert list(result_series) == [0, 0, 0, 0, 0]


def test_getup_habit_early(sample_dayrangereport: DayRangeReport) -> None:
    # Simulate getup at 6:30 for first day
    day_record = sample_dayrangereport.day_records[0]
    day_record.getup_timestamp = day_record.getup_timestamp.replace(hour=6, minute=30)
    habit = GetupHabit(sample_dayrangereport, "07:00")
    result_series = habit.data()
    assert result_series.iloc[0] == 30  # 7:00 - 6:30 = 30 min early


def test_getup_habit_late(sample_dayrangereport: DayRangeReport) -> None:
    # Simulate getup at 7:30 for last day
    day_record = sample_dayrangereport.day_records[-1]
    day_record.getup_timestamp = day_record.getup_timestamp.replace(hour=7, minute=30)
    habit = GetupHabit(sample_dayrangereport, "07:00")
    result_series = habit.data()
    assert result_series.iloc[-1] == -30  # 7:00 - 7:30 = -30 min late


@pytest.mark.parametrize("bad_time", ["7:00", "24:00", "07:60", "ab:cd"])
def test_getup_habit_invalid_time(
    bad_time: str, sample_dayrangereport: DayRangeReport
) -> None:
    with pytest.raises(ValueError):
        GetupHabit(sample_dayrangereport, bad_time)


def test_bed_habit_on_time(sample_dayrangereport: DayRangeReport) -> None:
    # Assuming all bed_timestamp at 23:00 by default (from conftest.py)
    habit = BedHabit(sample_dayrangereport, "23:00")
    result_series = habit.data()
    # All bed at 23:00, so diff should be 0
    assert list(result_series) == [0, 0, 0, 0, 0]


def test_bed_habit_early(sample_dayrangereport: DayRangeReport) -> None:
    # Simulate bed at 20:30 for first day (earlier than 21:00 target = good)
    day_record = sample_dayrangereport.day_records[0]
    day_record.bed_timestamp = day_record.bed_timestamp.replace(hour=20, minute=30)
    habit = BedHabit(sample_dayrangereport, "21:00")
    result_series = habit.data()
    # Earlier bed = positive score (good habit)
    assert result_series.iloc[0] == 30  # 30 min early = +30


def test_bed_habit_late(sample_dayrangereport: DayRangeReport) -> None:
    # Simulate bed at 21:30 for last day (later than 21:00 target = bad)
    day_record = sample_dayrangereport.day_records[-1]
    day_record.bed_timestamp = day_record.bed_timestamp.replace(hour=21, minute=30)
    habit = BedHabit(sample_dayrangereport, "21:00")
    result_series = habit.data()
    # Later bed = negative score (bad habit)
    assert result_series.iloc[-1] == -30  # 30 min late = -30


@pytest.mark.parametrize("bad_time", ["9:00", "24:00", "21:60", "ab:cd"])
def test_bed_habit_invalid_time(
    bad_time: str, sample_dayrangereport: DayRangeReport
) -> None:
    with pytest.raises(ValueError):
        BedHabit(sample_dayrangereport, bad_time)
