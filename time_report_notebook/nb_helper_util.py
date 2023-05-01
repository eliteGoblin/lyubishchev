from typing import Any, Tuple

import pandas as pd
import plotly.express as px
from arrow import Arrow

from lyubishchev.report import DayRangeReport, get_match_dict


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
        color="exercise",
        text="minutes",
        title=f"{match_dict_key} Duration by Weekday",
        labels={"date": "Weekday", "minutes": "Minutes"},
    )

    fig.show()
