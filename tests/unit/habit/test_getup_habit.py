import pytest

from lyubishchev.habit import GetupHabit
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
