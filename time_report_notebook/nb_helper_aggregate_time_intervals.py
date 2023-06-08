import plotly.express as px
import plotly.graph_objs as go

from lyubishchev.data_model import TimeInterval
from lyubishchev.report import DayRangeReport, get_time_interval_aggregation_dict_tree
from time_report_notebook.nb_helper_util import dict_tree_to_parent_tree, m2h


def sunburst_time_intervals(
    total_time_minutes: int, time_intervals: list[TimeInterval]
) -> None:
    aggregation_dict_tree = get_time_interval_aggregation_dict_tree(
        total_time_minutes=total_time_minutes,
        time_intervals=time_intervals,
    )
    labels, parents, values = dict_tree_to_parent_tree(aggregation_dict_tree)
    fig = go.Figure(
        go.Sunburst(
            labels=labels,
            parents=parents,
            values=m2h(values),
            textinfo="label+percent entry",
            # maxdepth=3,
        )
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.show()


def time_intervals_to_gantt_data_frame(
    time_intervals: list[TimeInterval],
) -> list[dict[str, str]]:
    res: list[dict[str, str]] = []

    for time_interval in time_intervals:
        for key, value in time_interval.metadata.label.items():

            value = "" if value is None else value
            value = "_" + value if value else value

            start_time = time_interval.timestamp.format("YYYY-MM-DD HH:mm:ss")
            finish_time = time_interval.timestamp.shift(
                minutes=+time_interval.duration_minutes
            ).format("YYYY-MM-DD HH:mm:ss")

            res.append(dict(Task=key + value, Start=start_time, Finish=finish_time))

    return res


def gantt_time_intervals(
    time_intervals: list[TimeInterval],
) -> None:

    data_frame = time_intervals_to_gantt_data_frame(time_intervals)
    fig = px.timeline(data_frame, x_start="Start", x_end="Finish", y="Task")
    fig.update_yaxes(
        autorange="reversed"
    )  # makes sure that the tasks are displayed from top to bottom in the order they are in the df
    fig.show()


def sunburst_time_intervals_single_day(report: DayRangeReport, day_shift: int) -> None:
    """
    day_shift must be negative, -1 means yesterday, -2 means day before yesterday
    """

    day_record = report.day_records[day_shift]

    time_intervals = day_record.time_intervals
    total_time_minutes_non_sleep = (
        day_record.bed_timestamp - day_record.wakeup_timestamp
    ).total_seconds() // 60  # type: ignore

    sunburst_time_intervals(
        total_time_minutes=total_time_minutes_non_sleep, time_intervals=time_intervals
    )
