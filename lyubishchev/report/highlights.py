from lyubishchev import config
from lyubishchev.data_model import timestamp_from_date_str

from .report import DayRangeReport


def get_self_improving_highlights(day_range_report: DayRangeReport) -> str:
    """
    SE average is measured against every day, i.e there's no strict NON-SE days
    """
    interval_metrics = day_range_report.get_interval_metrics()

    total_time: float = (
        sum(interval_metrics["effective_output"]["self_improving"]) / 60.0
    )

    average_time: float = total_time / len(day_range_report)

    return f"Total time: {round(total_time, 2)}h, daily self-improving: {round(average_time, 2)}h"


def get_work_highlights(day_range_report: DayRangeReport) -> str:
    """
    Work average, is only measured against weekdays
    """
    interval_metrics = day_range_report.get_interval_metrics()

    total_time: float = sum(interval_metrics["effective_output"]["work"]) / 60.0
    total_weekdays: int = 0

    for day in day_range_report.day_records:
        day_timestamp = timestamp_from_date_str(
            timezone_name=config.get_iana_timezone_name(), date_str=day.date_str()
        )
        if day_timestamp.isoweekday() <= 5:
            total_weekdays += 1

    average_time: float = total_time / total_weekdays

    return f"Total time: {round(total_time, 2)}h, average: {round(average_time, 2)}h"


def get_effective_output_highlights(day_range_report: DayRangeReport) -> str:
    interval_metrics = day_range_report.get_interval_metrics()

    effective_output = [
        work + self_improving
        for work, self_improving in zip(
            interval_metrics["effective_output"]["work"],
            interval_metrics["effective_output"]["self_improving"],
        )
    ]

    total_time: float = sum(effective_output) / 60.0
    average_time: float = total_time / len(day_range_report)

    return (
        f"Total time: {round(total_time, 2)}h, daily average: {round(average_time, 2)}h"
    )


def every(occur_ratio: float) -> str:
    """
    0.33 -> every 3 days
    0.5 -> every 2 days
    1 -> every day
    """
    if occur_ratio < 0.01:
        return "rarely(< 0.01)"
    if occur_ratio >= 1:
        return "every day"
    return f"every {round(1 / occur_ratio, 2)} days"


def get_sex_highlights(day_range_report: DayRangeReport) -> str:
    """
    sex: use daily aggregated data to calculate count: 0 or 1 per day
    """

    interval_metrics = day_range_report.get_interval_metrics()
    sex = interval_metrics["sex"]

    sex_times: int = len([e for e in sex if e > 0])
    sex_total_hours: float = sum(sex) / 60.0

    return (
        f"day has sex: {sex_times}/{len(sex)}, happens {every(len([e for e in sex if e > 0]) / len(sex))}. "
        f"total hour/every time avg {round(sex_total_hours, 2)}/{round(sex_total_hours / sex_times, 2)}h"
    )


def get_sleep_highlights(day_range_report: DayRangeReport) -> str:

    interval_metrics = day_range_report.get_interval_metrics()
    night_sleep = interval_metrics["sleep"]["night_sleep"]
    nap = interval_metrics["sleep"]["nap"]

    average_nightly_sleep_hours: float = sum(night_sleep) / len(night_sleep) / 60.0
    average_daily_nap_hours: float = sum(nap) / len(nap) / 60.0

    nap_days = [e for e in nap if e > 0]

    return (
        f"average nap {round(average_daily_nap_hours, 2)}h, "
        f"day has nap {len(nap_days)}/{len(nap)}, happens {every(len(nap_days) / len(nap))}. "
        f"average nightly sleep {round(average_nightly_sleep_hours, 2)}h, "
        f"average all sleep time {round(average_nightly_sleep_hours + average_daily_nap_hours, 2)}h"
    )


def get_meditation_highlights(day_range_report: DayRangeReport) -> str:
    meditations = day_range_report.get_interval_metrics()["meditation"]
    meditation_daily_aggregate = [e for e in meditations if e > 0]

    daily_average_meditation_hours = sum(meditations) / (60.0 * len(meditations))

    return (
        f"daily meditation: {round(daily_average_meditation_hours, 2)}h "
        f"days with meditation: {len(meditation_daily_aggregate)}/{len(meditations)}, "
        f"happends {every(len(meditation_daily_aggregate) / len(meditations))}"
    )


def get_exercise_highlights(day_range_report: DayRangeReport) -> str:

    exercises = day_range_report.get_interval_metrics()["exercise"]
    exercise_daily_aggregate = [e for e in exercises if e > 0]

    res = {
        "daily_avg": round(sum(exercises) / len(exercises) / 60.0, 2),
        "exercie_every": every(len(exercise_daily_aggregate) / len(exercises)),
    }

    return (
        f"daily exercise: {res['daily_avg']}h, "
        f"days with exercise: {len(exercise_daily_aggregate)}/{len(exercises)}, happens {res['exercie_every']}"
    )


def get_highlights(day_range_report: DayRangeReport) -> dict[str, str]:
    """
    get_highlights returns a dict of highlights
    """
    # effective output
    self_improving = get_self_improving_highlights(day_range_report)
    work = get_work_highlights(day_range_report)
    effective_output = get_effective_output_highlights(day_range_report)
    # supporting
    sex = get_sex_highlights(day_range_report)
    sleep = get_sleep_highlights(day_range_report)
    meditation = get_meditation_highlights(day_range_report)
    exercise = get_exercise_highlights(day_range_report)

    return {
        "self_improving": self_improving,
        "work": work,
        "effective_output": effective_output,
        "sex": sex,
        "sleep": sleep,
        "meditation": meditation,
        "exercise": exercise,
    }
