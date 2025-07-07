from lyubishchev.habit import TimeIntervalHabit
from lyubishchev.report.report import DayRangeReport


def test_time_interval_habit_work(sample_dayrangereport: DayRangeReport) -> None:
    habit = TimeIntervalHabit(sample_dayrangereport, "work")
    result_series = habit.data()
    # Should be [60, 70, 80, 90, 100]
    assert list(result_series) == [60, 70, 80, 90, 100]
    # Compare index as strings to match DatetimeIndex with date_str
    assert [ts.strftime("%Y-%m-%d") for ts in result_series.index] == [
        day_record.date_str() for day_record in sample_dayrangereport.day_records
    ]


def test_time_interval_habit_exercise(sample_dayrangereport: DayRangeReport) -> None:
    habit = TimeIntervalHabit(sample_dayrangereport, "exercise")
    result_series = habit.data()
    assert list(result_series) == [30, 30, 30, 30, 30]
