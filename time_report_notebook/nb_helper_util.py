from typing import Any, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from arrow import Arrow

from lyubishchev.report import (
    DayRangeReport,
    get_match_dict,
    time_spans_by_day_matching_label_minutes,
)
from lyubishchev.search import Match


def remove_year(dates: list[str]) -> list[str]:
    # remove year, e.g. 2021-03-18 -> 03-18, since it will couse X axis label overlap
    return [date[5:] for date in dates]


def get_weekdays(timestamps: list[Arrow]) -> list[str]:
    return [timestamp.format("ddd") for timestamp in timestamps]


def remove_year_add_weekday(dates: list[str], day_timestamps: list[Arrow]) -> list[str]:
    # zip the dates and weekdays, like 03-18\nMON

    dates = remove_year(dates)
    weekdays = get_weekdays(day_timestamps)
    dates = [f"{date}\n{weekday}" for date, weekday in zip(dates, weekdays)]

    return dates


def dict_tree_to_parent_tree(
    dict_tree: dict[str, Any]
) -> Tuple[list[str], list[str], list[int]]:
    """
    Convert a dict tree to a parent tree

    Args:
    - dict_tree: dictionary representing a nested tree structure

    Returns:
    - nodes_name: list of node names in the parent tree
    - parent_node: list of parent node names corresponding to each node in nodes_name
    - node_values: list of values corresponding to each node in nodes_name
    """

    # Initialize lists for storing the output
    nodes_name = []  # List of node names
    parent_node = []  # List of parent node names
    node_values = []  # List of node values

    def process_subtree(subtree: dict[str, Any], parent_name: str) -> None:
        """
        Recursively process a subtree and add its nodes to the parent tree
        """
        for node_name, node_value in subtree.items():
            # Add the current node to the parent tree
            nodes_name.append(node_name)
            parent_node.append(parent_name)

            # Recursively process child nodes if current node is an inner node
            if isinstance(node_value, dict):
                node_values.append(0)
                process_subtree(node_value, node_name)
            else:
                node_values.append(node_value)

    # Call process_subtree on the root of the input dict tree
    process_subtree(dict_tree, "")

    return nodes_name, parent_node, node_values


def m2h(minutes: list[int]) -> list[float]:
    return [round(m / 60, 2) for m in minutes]


def draw_bars_chart(
    report: DayRangeReport,
    bar_list: dict[str, dict[str, Any]],
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
    )

    fig.show()


def stack_bar(report: DayRangeReport, match_dict_key: str) -> None:
    match_dict = get_match_dict(match_dict_key)
    res = []

    for key in match_dict:
        res.extend(
            report.get_long_format_data_list(
                tag=key,  # e.g match key is "jog", use it to query the data
                key_name_in_res=match_dict_key,
            )
        )

    res_data_frame = pd.DataFrame(res)

    fig = px.bar(
        res_data_frame,
        x="date",
        y="minutes",
        color=match_dict_key,
        text="minutes",
        title=f"{match_dict_key} Duration by Weekday",
        labels={"date": "Weekday", "minutes": "Minutes"},
    )

    fig.show()


def sunburst_tree_depth_2(report: DayRangeReport, match_dict_key: str) -> None:
    """
    plot sunburst graph based on 2 level dict tree(can not be more than 2 level)
    e.g each leaf node's key means label to match time intervals
    {
        "calm": {
            "walk": 10,
            "meditation": 20,
        }
    }
    """
    match_dict = get_match_dict(match_dict_key)
    res = {}

    for key in match_dict:
        res[key] = sum(
            time_spans_by_day_matching_label_minutes(
                day_records=report.day_records,
                match=Match.from_dict({key: None}),
            )
        )

    labels, parents, values = dict_tree_to_parent_tree({match_dict_key: res})
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
