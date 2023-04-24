from typing import Any, Dict, List

import plotly.graph_objs as go
from arrow import Arrow

from .nb_helper_util import remove_year_add_weekday


def draw_bars_chart(
    dates: List[str], day_timestamps: list[Arrow], bar_list: Dict[str, Dict[str, Any]]
) -> None:
    """
    Draw bar chart: X specify dates; Y specify time span in minutes
    dates: list of dates, e.g., 2023-04-13
    bar_list = {
        "label1": {
            "color": "red",
            "time_span_minutes": [1, 2, 3, 4, 5, 6, 7]
        },
        "label2": {
            "color": "blue",
            "time_span_minutes": [1, 2, 3, 4, 5, 6, 7]
        },
    }
    """
    dates = remove_year_add_weekday(
        dates=dates,
        day_timestamps=day_timestamps,
    )
    fig = go.Figure()

    for label, data in bar_list.items():
        fig.add_trace(
            go.Bar(
                x=dates,
                y=data["time_span_minutes"],
                name=label,
                marker_color=data["color"],
            )
        )

    fig.update_layout(
        title="Bar Chart",
        xaxis_title="Dates",
        yaxis_title="Time Span in Minutes",
        barmode="group",
    )

    fig.show()


def draw_bars_effective_output(
    dates: list[str],
    day_timestamps: list[Arrow],
    self_improving_minutes: list[int],
    work_minutes: list[int],
) -> None:

    draw_bars_chart(
        dates=dates,
        day_timestamps=day_timestamps,
        bar_list={
            "self_improving": {
                "color": "green",
                "time_span_minutes": self_improving_minutes,
            },
            "work": {
                "color": "blue",
                "time_span_minutes": work_minutes,
            },
        },
    )
