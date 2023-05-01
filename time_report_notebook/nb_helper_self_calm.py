import plotly.graph_objects as go

from lyubishchev.report import (
    DayRangeReport,
    get_match_dict,
    time_spans_by_day_matching_label_minutes,
)
from lyubishchev.search import Match

from .nb_helper_time_interval_metrics import draw_bars_chart, m2h
from .nb_helper_util import dict_tree_to_parent_tree


def bar_calm(report: DayRangeReport) -> None:
    calm_spans = report.get_interval_metrics()["calm"]
    draw_bars_chart(
        report=report,
        bar_list={
            "exercise": {
                "color": "#07731e",
                "time_span_minutes": calm_spans,
            },
        },
        title="Exercise in minutes",
    )


def sunburst_calm(report: DayRangeReport) -> None:
    """
    Get a dict tree frist
    {
        "calm": {
            "meditation": 10,
            "walk": 20,
        }
    }
    Convert to parent tree, then draw sunburst chart
    """
    calm_key = "calm"
    calm_match_dict = get_match_dict(calm_key)
    calm_res = {}

    for key in calm_match_dict:
        calm_res[key] = sum(
            time_spans_by_day_matching_label_minutes(
                day_records=report.day_records,
                match=Match.from_dict({key: None}),
            )
        )

    labels, parents, values = dict_tree_to_parent_tree(calm_res)
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
