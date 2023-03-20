import arrow
import typer
from icecream import ic  # type: ignore

from lyubishchev import config
from lyubishchev.data_model import get_day_range_from_relative_days
from lyubishchev.report import get_highlights

from .report import get_report

report_app = typer.Typer(
    name="report",
)


@report_app.command()
def dayrange(start_date: str, end_date: str) -> None:
    """
    specify day range [start_date, end_date) to generate report
    """
    report = get_report(
        start_date=start_date,
        end_date=end_date,
    )
    ic(report.get_time_stats())
    ic(report.get_interval_metrics())
    ic(report.get_event_metrics())

    ic(get_highlights(report))


@report_app.command()
def last(last_days: int) -> None:
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
    ic(report.get_time_stats())
    ic(report.get_interval_metrics())
    ic(report.get_event_metrics())

    ic(get_highlights(report))


if __name__ == "__main__":
    report_app()
