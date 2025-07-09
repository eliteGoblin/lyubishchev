from lyubishchev.habit import TimeIntervalOneofHabit
from lyubishchev.report.report import DayRangeReport


def test_interval_oneof_habit_work_exercise(
    sample_dayrangereport: DayRangeReport,
) -> None:
    """
    When keys include both 'work' and 'exercise', durations sum per day.
    """
    habit = TimeIntervalOneofHabit(sample_dayrangereport, ["work", "exercise"])
    result = habit.data()
    # work durations: [60,70,80,90,100], exercise: [30,30,30,30,30]
    expected = [90, 100, 110, 120, 130]
    assert list(result) == expected
    # index matches each day_str
    assert [ts.strftime("%Y-%m-%d") for ts in result.index] == [
        dr.date_str() for dr in sample_dayrangereport.day_records
    ]


def test_interval_oneof_habit_work_only(sample_dayrangereport: DayRangeReport) -> None:
    """
    When only 'work' key provided, behaves like TimeIntervalHabit.
    """
    habit = TimeIntervalOneofHabit(sample_dayrangereport, ["work"])
    result = habit.data()
    assert list(result) == [60, 70, 80, 90, 100]


def test_interval_oneof_habit_missing(sample_dayrangereport: DayRangeReport) -> None:
    """
    No matching keys yields zero durations.
    """
    habit = TimeIntervalOneofHabit(sample_dayrangereport, ["nonexistent"])
    result = habit.data()
    assert list(result) == [0, 0, 0, 0, 0]
