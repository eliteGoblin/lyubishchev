from lyubishchev.habit import TimeIntervalCounterHabit
from lyubishchev.report.report import DayRangeReport


def test_time_interval_counter_habit_work(
    sample_dayrangereport: DayRangeReport,
) -> None:
    """
    Test that TimeIntervalCounterHabit counts the number of 'work' intervals per day.
    """
    habit = TimeIntervalCounterHabit(sample_dayrangereport, "work")
    result_series = habit.data()
    # Each day in the fixture has exactly one 'work' interval
    assert list(result_series) == [1, 1, 1, 1, 1]
    # Index should be DatetimeIndex matching the days
    assert all(
        result_series.index[i].strftime("%Y-%m-%d") == day.date_str()
        for i, day in enumerate(sample_dayrangereport.day_records)
    )


def test_time_interval_counter_habit_exercise(
    sample_dayrangereport: DayRangeReport,
) -> None:
    """
    Test that TimeIntervalCounterHabit counts the number of 'exercise' intervals per day.
    """
    habit = TimeIntervalCounterHabit(sample_dayrangereport, "exercise")
    result_series = habit.data()
    # Each day in the fixture has exactly one 'exercise' interval
    assert list(result_series) == [1, 1, 1, 1, 1]


def test_time_interval_counter_habit_missing(
    sample_dayrangereport: DayRangeReport,
) -> None:
    """
    Test that TimeIntervalCounterHabit returns 0 for days with no matching intervals.
    """
    habit = TimeIntervalCounterHabit(sample_dayrangereport, "nonexistent")
    result_series = habit.data()
    assert list(result_series) == [0, 0, 0, 0, 0]
