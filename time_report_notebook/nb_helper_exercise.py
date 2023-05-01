import plotly.graph_objects as go

from lyubishchev.report import (
    DayRangeReport,
    get_match_dict,
    time_spans_by_day_matching_label_minutes,
)
from lyubishchev.search import Match

from .nb_helper_time_interval_metrics import draw_bars_chart, m2h
from .nb_helper_util import dict_tree_to_parent_tree, stack_bar


def bar_exercise(report: DayRangeReport) -> None:
    exercise_spans = report.get_interval_metrics()["exercise"]
    draw_bars_chart(
        report=report,
        bar_list={
            "exercise": {
                "color": "#07731e",
                "time_span_minutes": exercise_spans,
            },
        },
        title="Exercise in minutes",
    )


def stack_bar_exercise(report: DayRangeReport) -> None:
    stack_bar(report=report, match_dict_key="exercise")


def sunburst_exercise(report: DayRangeReport) -> None:
    """
    Get a dict tree frist
    {
        "exercise": {
            "jog": 10,
            "swim": 20,
            "anaerobic": 30,
        }
    }
    Convert to parent tree, then draw sunburst chart
    """
    exercise_key = "exercise"
    exercise_match_dict = get_match_dict(exercise_key)
    exercise_res = {}

    for key in exercise_match_dict:
        exercise_res[key] = sum(
            time_spans_by_day_matching_label_minutes(
                day_records=report.day_records,
                match=Match.from_dict({key: None}),
            )
        )

    labels, parents, values = dict_tree_to_parent_tree({exercise_key: exercise_res})
    fig = go.Figure(
        go.Sunburst(
            labels=labels,
            parents=parents,
            values=m2h(values),
            textinfo="label+percent entry",
        )
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.show()
