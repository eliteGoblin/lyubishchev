from lyubishchev.habit import TimeEventHabit
from lyubishchev.report.report import DayRangeReport


def test_time_event_habit_unwell(sample_dayrangereport: DayRangeReport) -> None:
    habit = TimeEventHabit(sample_dayrangereport, "unwell")
    result_series = habit.data()
    # Only day 2 and 4 have "unwell" event
    assert list(result_series) == [0, 1, 0, 1, 0]
