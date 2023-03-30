from typing import Union

import matplotlib.pyplot as plt
import numpy as np


def time_stat_to_pie_chart_data(time_stat: dict[str, int]) -> dict[str, int]:
    """
    cherry-pick data from timestats, and return a dict for pie chart
    """

    res = {
        "sleep": time_stat["sleep_all"],
        "work": time_stat["work"],
        "exercise": time_stat["exercise"],
        "self_improving": time_stat["self_improving"],
        "sex": time_stat["sex"],
    }

    res["other"] = time_stat["total"] - sum(res.values())

    return res


def create_array(data: dict[str, Union[dict[str, int], int]]) -> np.ndarray:
    rows = []

    for key in data:
        if isinstance(data[key], dict):
            row = list(data[key].values())
            rows.append(row)
        elif isinstance(data[key], int):
            row = [data[key], 0]
            rows.append(row)

    return np.array(rows)


def show_time_stat_as_piechart(report_time_stat: dict[str, int]) -> None:
    """
    show time stat as a pie chart
    """
    piechart_data = time_stat_to_pie_chart_data(report_time_stat)

    _, axis = plt.subplots()
    axis.pie(piechart_data.values(), labels=piechart_data.keys(), autopct="%1.1f%%")
    axis.set_title("Pie Chart of Data")
    plt.show()


def show_nested_piechart(values_dict: dict[str, Union[dict[str, int], int]]) -> None:
    """
    Support up to 2 levels of piechart, i.e dict nested level is 1 or 2
    values_dict is a dict of main category and its sub categories
    {
        "sleep": {
            "night_sleep": 380,
            "nap": 60,
        },
        work: 480,
        exercise: {
            "jogging": 60,
            "yoga": 30,
        },
    }
    """

    _, axis = plt.subplots()

    size = 0.3
    matrix = create_array(values_dict)

    row, col = matrix.shape
    cmap = plt.get_cmap("tab20c")

    # color index in color map, closer means color is similar
    outer_color_values = (
        np.arange(row) * 4
    )  # 4 is arbeitrary number, to make outter piechart color different
    inner_color_value: list[int] = []

    outer_labels = list(values_dict.keys())
    inner_labels = []

    for key in values_dict:
        if isinstance(values_dict[key], dict):
            inner_labels += list(values_dict[key].keys())
        elif isinstance(values_dict[key], int):
            inner_labels.append(key)

    # pickup inner colors near value of color of its parent pie slice
    for i in range(row):
        for j in range(col):
            if matrix[i][j] != 0:
                inner_color_value.append(outer_color_values[i] + j)

    # Create outer pie chart with labels
    axis.pie(
        matrix.sum(axis=1),
        radius=1,
        colors=cmap(outer_color_values),
        labels=outer_labels,
        wedgeprops=dict(width=size, edgecolor="w"),
        autopct="%.1f%%",
        pctdistance=0.85,
    )

    # Create inner pie chart with labels
    non_zero_values = matrix.flatten()[matrix.flatten() != 0]
    axis.pie(
        non_zero_values,
        radius=1 - size,
        colors=cmap(inner_color_value),
        labels=inner_labels,
        wedgeprops=dict(width=size, edgecolor="w"),
        autopct="%.1f%%",
        pctdistance=0.75,
    )

    axis.set(aspect="equal", title="Pie plot with `ax.pie`")
    plt.show()
