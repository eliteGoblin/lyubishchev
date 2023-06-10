import arrow
import typer

from lyubishchev import config
from lyubishchev.data_model import (
    get_day_range_from_relative_days,
    get_day_range_from_relative_months,
    get_day_range_from_relative_weeks,
)
from lyubishchev.report import DayRangeReport

from .report import get_report

# from icecream import ic  # type: ignore


report_app = typer.Typer(
    name="report",
)


@report_app.command()
def dayrange(start_date: str, end_date: str) -> DayRangeReport:
    """
    specify day range [start_date, end_date) to generate report
    """
    report = get_report(
        start_date=start_date,
        end_date=end_date,
    )

    return report


@report_app.command()
def last(last_days: int) -> DayRangeReport:
    """
    specify last N days to generate report, e.g last_days=3 means [today-3, today)
    """
    # get today's date string as 2023-03-18, using Arrow, timezone is "Australia/Sydney"
    today_str = arrow.now(config.get_iana_timezone_name()).format("YYYY-MM-DD")

    start_date, end_date = get_day_range_from_relative_days(
        start_date=today_str,
        days_delta=-last_days,
        lower_bound_applied=True,
    )
    report = get_report(
        start_date=start_date,
        end_date=end_date,
    )

    return report


@report_app.command()
def relative_week(week_offset: int) -> DayRangeReport:
    """
    get DayRangeReport from last Sunday to yesterday
    """
    today_str = arrow.now(config.get_iana_timezone_name()).format("YYYY-MM-DD")

    start_date, end_date = get_day_range_from_relative_weeks(
        start_date_str=today_str, week_offset=week_offset
    )

    report = get_report(
        start_date=start_date,
        end_date=end_date,
    )

    return report


@report_app.command()
def relative_month(month_offset: int) -> DayRangeReport:
    """
    get DayRangeReport based on month offset
    """
    today_str = arrow.now(config.get_iana_timezone_name()).format("YYYY-MM-DD")

    start_date, end_date = get_day_range_from_relative_months(
        start_date_str=today_str, month_offset=month_offset
    )

    report = get_report(
        start_date=start_date,
        end_date=end_date,
    )

    return report


if __name__ == "__main__":
    report_app()
