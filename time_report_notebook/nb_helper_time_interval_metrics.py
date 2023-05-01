from typing import Any, Dict

import plotly.graph_objs as go

from lyubishchev.report import DayRangeReport


def m2h(minutes: list[int]) -> list[float]:
    return [round(m / 60, 2) for m in minutes]


def draw_bars_chart(
    report: DayRangeReport,
    bar_list: Dict[str, Dict[str, Any]],
    title: str = "",
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
    dates = report.dates(is_remove_year=True, is_add_weekday=True)
    fig = go.Figure()

    for label, data in bar_list.items():
        fig.add_trace(
            go.Bar(
                x=dates,
                y=m2h(data["time_span_minutes"]),
                name=label,
                marker_color=data["color"],
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="Dates",
        yaxis_title="Time Span in Hours",
        barmode="group",
        width=800,  # Set the chart width
        height=500,  # Set the chart height
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        autosize=True,
    )

    fig.show()
