import pandas as pd

from lyubishchev.data_model import timestamp_from_date_str
from lyubishchev.search import Match

from .report import DayRangeReport, get_match_dict, time_spans_matching_label_minutes


def get_duration_highlights(report: DayRangeReport) -> pd.DataFrame:
    """
    Return:
            daily   avg     total
    work
    SE
    night_sleep
    nap
    exercise
    calm
    """
    time_intervals = report.get_time_intervals()
    work = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict(get_match_dict("work_all"))
    )
    total_weekdays: int = 0
    for day in report.day_records:
        day_timestamp = timestamp_from_date_str(date_str=day.date_str())
        if day_timestamp.isoweekday() <= 5:
            total_weekdays += 1

    self_improving = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict(get_match_dict("self_improving"))
    )
    night_sleep = [day.last_night_sleep_minutes for day in report.day_records]
    nap = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict({"nap": None})
    )
    exercise = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict(get_match_dict("exercise"))
    )
    calm = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict(get_match_dict("calm"))
    )

    data = {
        "work": [
            sum(work) / total_weekdays if total_weekdays > 0 else 0,
            sum(work),
        ],  # work is weekday average, instead of everyday average
        "self_improving": [
            sum(self_improving) / len(report.day_records),
            sum(self_improving),
        ],
        "night_sleep": [sum(night_sleep) / len(report.day_records), sum(night_sleep)],
        "nap": [sum(nap) / len(report.day_records), sum(nap)],
        "exercise": [sum(exercise) / len(report.day_records), sum(exercise)],
        "calm": [sum(calm) / len(report.day_records), sum(calm)],
    }
    # convert to hours, round to 2 decimal
    data = {k: [round(e / 60, 2) for e in v] for k, v in data.items()}
    index = ["daily_average", "total_hours"]
    df_duration = pd.DataFrame(data=data, index=index).transpose()  # type: ignore

    return df_duration


def daily_count_to_str(daily_count: float) -> str:
    if daily_count == 0:
        return "no activity found"
    if daily_count < 1:
        return f"every {round(1 / daily_count, 1)} days"
    return f"{round(daily_count, 1)} times per day"


def get_habbits_highlight(report: DayRangeReport) -> pd.DataFrame:
    """
    Return:
             count_per_day activity_avg  daily_avg total
    sex_all
    walk
    meditation
    nap
    exericise
    """
    time_intervals = report.get_time_intervals()
    sex_all = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict(get_match_dict("sex_all"))
    )
    walk = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict({"walk": None})
    )
    meditation = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict({"meditation": None})
    )
    nap = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict({"nap": None})
    )
    exercise = time_spans_matching_label_minutes(
        time_intervals, Match.from_dict(get_match_dict("exercise"))
    )

    list_names = ["sex_all", "walk", "meditation", "nap", "exercise"]
    list_of_lists = [sex_all, walk, meditation, nap, exercise]
    index = [
        "count_per_day",
        "avg_minutes_per_activity",
        "avg_minutes_per_day",
        "total_minutes",
    ]

    data = {}
    for i, name in enumerate(list_names):
        data[name] = [
            len(list_of_lists[i]) / len(report.day_records),
            sum(list_of_lists[i]) / len(list_of_lists[i])
            if len(list_of_lists[i]) > 0
            else 0,
            sum(list_of_lists[i]) / len(report.day_records),
            sum(list_of_lists[i]),
        ]

    df_habbits = pd.DataFrame(data=data, index=index).transpose()  # type: ignore

    df_habbits["frequency"] = df_habbits["count_per_day"].apply(daily_count_to_str)
    df_habbits = df_habbits.drop("count_per_day", axis=1)

    df_habbits["avg_minutes_per_activity"] = (
        df_habbits["avg_minutes_per_activity"] / 60
    ).apply(lambda x: round(x, 2))

    df_habbits["avg_minutes_per_day"] = (df_habbits["avg_minutes_per_day"] / 60).apply(
        lambda x: round(x, 2)
    )

    df_habbits["total_hours"] = (df_habbits["total_minutes"] / 60).apply(
        lambda x: round(x, 2)
    )
    df_habbits = df_habbits.drop("total_minutes", axis=1)

    return df_habbits
