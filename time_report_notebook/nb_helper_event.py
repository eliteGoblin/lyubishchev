import datetime
from typing import Optional

import plotly.graph_objs as go
from arrow import Arrow
from plotly.subplots import make_subplots

from lyubishchev.data_model import day_start_timestamp_early_bound
from lyubishchev.report import DayRangeReport


def timestamp_diff(timestamp: Arrow, base_timestamp: Optional[Arrow] = None) -> float:

    if base_timestamp is None:
        start_of_day = timestamp.floor("day")
    else:
        start_of_day = base_timestamp.floor("day")

    difference: datetime.timedelta = timestamp - start_of_day  # type: ignore
    offset_hours = difference.total_seconds() / 3600.0

    return round(offset_hours, 2)


def draw_wakeup_plot(report: DayRangeReport) -> None:
    wakeup_timestamps = report.get_event_metrics()["wakeup"]
    dates = report.dates(is_remove_year=True, is_add_weekday=True)

    diff_hours = [timestamp_diff(tm) for tm in wakeup_timestamps]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    trace = go.Scatter(
        x=dates, y=diff_hours, mode="markers+lines", name="Wakeup Hour Offset"
    )
    fig.add_trace(trace, secondary_y=False)

    fig.update_xaxes(title_text="Dates of Day")

    fig.update_yaxes(title_text="Wakeup Hour Offset", secondary_y=False)

    # Display the plot
    fig.show()


def draw_bed_plot(report: DayRangeReport) -> None:
    """
    bedtime can be after midnight, so when calculate offset, we can't always the start of sameday,
        we need to calculate the start of previous day
    """
    dates = report.dates(is_remove_year=False, is_add_weekday=False)
    bed_timestamps = report.get_event_metrics()["bed"]
    base_timestamps = [day_start_timestamp_early_bound(date) for date in dates]
    diff_hours = []

    for idx, timestamp in enumerate(bed_timestamps):
        diff_hours.append(timestamp_diff(timestamp, base_timestamps[idx]))

    dates = report.dates(is_remove_year=True, is_add_weekday=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    trace = go.Scatter(
        x=dates, y=diff_hours, mode="markers+lines", name="Bed Hour Offset"
    )
    fig.add_trace(trace, secondary_y=False)

    fig.update_xaxes(title_text="Dates of Day")

    fig.update_yaxes(title_text="Bed Hour Offset", secondary_y=False)

    # Display the plot
    fig.show()
