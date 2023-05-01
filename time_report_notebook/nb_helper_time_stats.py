from typing import Any

import plotly.graph_objs as go
import plotly.io as pio

from lyubishchev.report import DayRangeReport


def time_intervals_stat_to_pie_chart_data(time_stat: dict[str, Any]) -> dict[str, int]:
    """
    cherry-pick data from timestats, and return a dict for pie chart
    """

    res = {
        "self_improving": sum(time_stat["effective_output"]["self_improving"]),
        "work": sum(time_stat["effective_output"]["work"]),
        "sex": sum(time_stat["sex_all"]["sex"]) + sum(time_stat["sex_all"]["mbate"]),
        "exercise": sum(time_stat["exercise"]),
        "night_sleep": sum(time_stat["sleep_all"]["night_sleep"]),
        "nap": sum(time_stat["sleep_all"]["nap"]),
        "calm": sum(time_stat["calm"]),
        "intangible": sum(time_stat["intangible"]),
        "regret": sum(time_stat["regret"]),
        "routine_all": sum(time_stat["routine_all"]),
        "solitude": sum(time_stat["solitude"]),
    }

    return res


def plot_piechart(chart_name: str, piechart_data: dict[str, float]) -> None:
    labels = list(piechart_data.keys())
    values = list(piechart_data.values())

    pie = go.Pie(labels=labels, values=values)

    layout = go.Layout(title=chart_name)

    fig = go.Figure(data=[pie], layout=layout)

    pio.show(fig)


def show_time_intervals_stat_as_piechart(report: DayRangeReport) -> None:
    time_interval_metrics = report.get_interval_metrics()
    piechart_data = time_intervals_stat_to_pie_chart_data(time_interval_metrics)
    piechart_data["other"] = report.get_total_minutes() - sum(piechart_data.values())
    piechart_data_hours = {k: round(v / 60, 2) for k, v in piechart_data.items()}
    plot_piechart("all time stat in hours", piechart_data_hours)
