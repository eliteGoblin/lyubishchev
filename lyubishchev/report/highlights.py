from .report import DayRangeReport

def get_self_improving_highlights(day_range_report: DayRangeReport) -> str:
    """
    SE average is measured against every day, i.e there's no strict NON-SE days
    """
    interval_metrics = day_range_report.get_interval_metrics()

    total_time: float = sum(interval_metrics["effective_output"]["self_improving"]) / 60.0

    average_time: float = total_time / len(day_range_report)

    return f"Total time: {total_time}h, average: {average_time}h"

def get_work_highlights(day_range_report: DayRangeReport) -> str:
    """
    Work average, is only measured against days of working day(literally need to work days, no leave, no public holiday, etc); 
    If overtime on weekend, work days for that week is still 5
    """
    interval_metrics = day_range_report.get_interval_metrics()

    total_time: float = sum(interval_metrics["effective_output"]["work"]) / 60.0
    # SE average is measured against every day, i.e there's no strict NON-SE days
    average_time: float = total_time / len(day_range_report)

    return f"Total time: {total_time}h, average: {average_time}h"

def get_sex_highlights(day_range_report: DayRangeReport) -> str:
    sex_times: int = 0
    ejaculate_times: int = 0
    sex_total_hours: float = 0.0

    return f"sex {sex_times} times, ejaculate count/avg {ejaculate_times}/{avg_ejaculate_times}, total {sex_total_hours}h"

def get_sleep_highlights(day_range_report: DayRangeReport) -> str:

    average_nightly_sleep_hours: float = 0.0
    average_daily_nap_hours: float = 0.0
    average_daily_nap_count:float = 0.0

    return f"average nightly sleep {nightly_sleep_hours}h, average daily nap {average_daily_nap_hours}h, average daily nap {average_daily_nap_count} times"

def get_highlights(day_range_report: DayRangeReport) -> dict[str, str]:
        """
        get_highlights returns a dict of highlights
        """
        # effective output
        self_improving = get_self_improving_highlights(day_range_report)
        work = get_work_highlights(day_range_report)
        # supporting
        sex = get_sex_highlights(day_range_report)
        sleep = get_sleep_highlights(day_range_report)
        meditation = get_meditation_highlights(day_range_report)
        exercise = get_exercise_highlights(day_range_report)

        return {
            "self_improving": self_improving,
            "work": work,
            "sex": sex,
            "sleep": sleep,
            "meditation": meditation,
            "exercise": exercise,
        }
