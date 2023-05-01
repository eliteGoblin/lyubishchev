from typing import Any

import plotly.graph_objects as go

from lyubishchev.report import (
    DayRangeReport,
    get_match_dict,
    time_spans_by_day_matching_label_minutes,
)
from lyubishchev.search import Match

from .nb_helper_time_interval_metrics import draw_bars_chart
from .nb_helper_util import dict_tree_to_parent_tree


def draw_bars_effective_output(report: DayRangeReport) -> None:

    draw_bars_chart(
        report=report,
        bar_list={
            "self_improving": {
                "color": "green",
                "time_span_minutes": report.get_interval_metrics()["effective_output"][
                    "self_improving"
                ],
            },
            "work": {
                "color": "blue",
                "time_span_minutes": report.get_interval_metrics()["effective_output"][
                    "work"
                ],
            },
        },
    )


def get_effective_output_dict_tree(report: DayRangeReport) -> dict[str, Any]:
    """
    Hierarchy of effective_output:
    {
        "effective_output": {
            "self_improving": {
                "tech": {
                    "lyubishchev": 3,
                    "oj": 4,
                    "software": 5,
                },
                "non_tech": {
                    "bibliotherapy": 1,
                    "linkedin": 2,
                    "audible": 6,
                }
            }
            "work": 10,
        }
    }
    """
    self_improving_tech_key = "self_improving_tech"
    self_improving_tech_match_dict = get_match_dict(self_improving_tech_key)
    # self_improving_tech = {
    #   "linkedin": None,
    #    "lyubishchev": None,
    #    "oj": None,
    #    "software": None,
    # }
    self_improving_tech_res = {}
    # generate tree dict from match dict, e.g
    # {
    #     "linkedin": 1,
    #     "lyubishchev": 2,
    #     "oj": 3,
    #     "software": 4,
    # }
    for key in self_improving_tech_match_dict:
        self_improving_tech_res[key] = sum(
            time_spans_by_day_matching_label_minutes(
                day_records=report.day_records,
                match=Match.from_dict({key: None}),
            )
        )

    self_improving_non_tech_key = "self_improving_non_tech"
    self_improving_non_tech_match_dict = get_match_dict(self_improving_non_tech_key)
    self_improving_non_tech_res = {}
    for key in self_improving_non_tech_match_dict:
        self_improving_non_tech_res[key] = sum(
            time_spans_by_day_matching_label_minutes(
                day_records=report.day_records,
                match=Match.from_dict({key: None}),
            )
        )

    res = {
        "effective_output": {
            "self_improving": {
                "tech": self_improving_tech_res,
                "non_tech": self_improving_non_tech_res,
            },
            "work": sum(
                time_spans_by_day_matching_label_minutes(
                    day_records=report.day_records,
                    match=Match.from_dict({"work": None}),
                )
            ),
        }
    }

    return res


def sunburst_effective_output(report: DayRangeReport) -> None:
    """
    piechart contain:
        night_sleep
        other
        work
        self_improving
    """
    effective_output_dict_tree = get_effective_output_dict_tree(report)
    labels, parents, values = dict_tree_to_parent_tree(effective_output_dict_tree)
    f_values = [round(value / 60, 2) for value in values]  # change minutes to hours

    fig = go.Figure(
        go.Sunburst(
            labels=labels,
            parents=parents,
            values=f_values,
            textinfo="label+percent entry",
        )
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.show()
