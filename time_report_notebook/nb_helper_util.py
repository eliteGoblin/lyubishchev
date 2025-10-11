from typing import Any, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from arrow import Arrow

from lyubishchev.report import (
    DayRangeReport,
    get_match_dict,
    time_spans_by_day_matching_label_minutes,
    time_spans_by_field_minutes,
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
    dict_tree: dict[str, Any],
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
        # autosize=False,  # Disable autosizing
        # width=800,       # Set the plot width
        # height=500,      # Set the plot height
        # margin=dict(l=50, r=50, b=100, t=100, pad=4),
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

    fig.update_layout(
        # autosize=False,  # Disable autosizing
        # width=800,       # Set the plot width
        # height=500,      # Set the plot height
        # margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )

    fig.show()


def sunburst_tree_depth_2(
    report: DayRangeReport,
    match_dict_key: str,
    sleep_all_minutes: int = 0,
    total_minutes: int = 0,
) -> None:
    """
    plot sunburst graph based on 2 level dict tree(can not be more than 2 level)
    e.g sunburst_tree_depth_2(report=report, match_dict_key="exercise")
    1. got match_dict of "exercise":
        {
            "jog": None,
            "swim": None,
            "anaerobic": None,
        }
    2. generate dict, representing tree structure of res:
        {
            "jog": 10,
            "swim": 20,
            "anaerobic": 30,
        }
    3. change dict tree to parent tree(not limited to depth 2):
        labels = ["exercise", "jog", "swim", "anaerobic"]
        parents = ["", "exercise", "exercise", "exercise"]
        values = [60, 10, 20, 30]
    """
    match_dict = get_match_dict(match_dict_key)
    res: dict[str, Any] = {match_dict_key: {}}

    for key in match_dict:
        res[match_dict_key][key] = sum(
            time_spans_by_day_matching_label_minutes(
                day_records=report.day_records,
                match=Match.from_dict({key: None}),
            )
        )

    if total_minutes > 0:
        res["other"] = total_minutes - sleep_all_minutes - sum_dict_values(res)

    labels, parents, values = dict_tree_to_parent_tree(res)

    fig = go.Figure(
        go.Sunburst(
            labels=labels,
            parents=parents,
            values=m2h(values),
            textinfo="label+percent entry",
            maxdepth=3,
        )
    )
    fig.update_layout(margin={"t": 0, "l": 0, "r": 0, "b": 0})
    fig.show()


def sum_dict_values(dct: dict[str, Any]) -> int:
    """
    sum all values in a dict, if value is a dict, sum it recursively
    """
    if isinstance(dct, dict):
        return sum(sum_dict_values(v) for v in dct.values())
    return dct


def sunburst_tree_depth_2_total_time(
    report: DayRangeReport,
    match_dict_key: str,
) -> None:
    """
    Thin wrapper of sunburst_tree_depth_2, include total time and total sleep time
        plot sunburst graph based on 2 level dict tree(can not be more than 2 level)
    """

    total_minutes = report.get_total_minutes()
    nap_time_minutes = sum(
        time_spans_by_day_matching_label_minutes(
            day_records=report.day_records,
            match=Match.from_dict({"nap": None}),
        )
    )
    night_sleep_time_minutes = sum(
        time_spans_by_field_minutes(
            day_records=report.day_records, field_name="last_night_sleep_minutes"
        )
    )

    sleep_all_minutes = nap_time_minutes + night_sleep_time_minutes

    sunburst_tree_depth_2(
        report=report,
        match_dict_key=match_dict_key,
        total_minutes=total_minutes,
        sleep_all_minutes=sleep_all_minutes,
    )
