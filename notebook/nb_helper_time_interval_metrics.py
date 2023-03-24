from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from arrow import Arrow


def get_weekdays(timestamps: list[Arrow]) -> list[str]:
    return [timestamp.format("ddd") for timestamp in timestamps]


def draw_bar_chart_se_work(
    dates: list[str],
    day_timestamps: list[Arrow],
    self_improving_minutes: list[int],
    work_minutes: list[int],
) -> None:

    dates = [
        date[5:] for date in dates
    ]  # remove year, e.g. 2021-03-18 -> 03-18, since it will couse X axis label overlap
    weekdays = get_weekdays(day_timestamps)
    # zip the dates and weekdays, like 03-18\nMON
    dates = [f"{date}\n{weekday}" for date, weekday in zip(dates, weekdays)]

    # Set the width of each bar
    bar_width = 0.35

    self_improving_hours = np.round(np.array(self_improving_minutes) / 60, 2)
    work_hours = np.round(np.array(work_minutes) / 60, 2)

    # Set the x position of each bar group
    x_self_improving = np.arange(len(self_improving_hours))
    x_work = [x + bar_width for x in x_self_improving]

    # Plotting
    plt.bar(
        x_self_improving,
        self_improving_hours,
        color="green",
        width=bar_width,
        label="Self Improving",
    )
    plt.bar(x_work, work_hours, color="blue", width=bar_width, label="Work")

    # Axis labels
    plt.xlabel("Date")
    plt.ylabel("Hours")

    # Title
    plt.title("self_improving_hours and work duration over time")

    # X-axis tick labels
    plt.xticks([r + bar_width / 2 for r in range(len(self_improving_hours))], dates)

    # Legend
    plt.legend()

    # Show the plot
    plt.show()


def draw_bars_chart(
    dates: list[str],
    day_timestamps: list[Arrow],
    bar_list: dict[str, dict[str, Any]],
) -> None:

    """
    draw_bars_chart draws a bar chart with multiple bars; align middle bar in middle of tick
    bar_list = {
        "label1": {
            "color": "red",
            "time_span_minutes": [1, 2, 3, 4, 5, 6, 7]
        },
        "label2": {
            "color": "blue",
            "time_span_minutes": [1, 2, 3, 4, 5, 6, 7]
        },
        "label3": {
            "color": "yellow",
            "time_span_minutes": [1, 2, 3, 4, 5, 6, 7]
        },
        "label4": {
            "color": "cyan",
            "time_span_minutes": [1, 2, 3, 4, 5, 6, 7]
        },
        "label5": {
            "color": "pink",
            "time_span_minutes": [1, 2, 3, 4, 5, 6, 7]
        },
        "label6": {
            "color": "black",
            "time_span_minutes": [1, 2, 3, 4, 5, 6, 7]
        }
    }
    """
    num_bars = len(bar_list)
    num_dates = len(next(iter(bar_list.values()))["time_span_minutes"])

    _, axis = plt.subplots()

    bar_width = 2 / 3 / num_bars
    group_positions = np.arange(num_dates)

    mid = num_bars // 2
    for idx, (label, data) in enumerate(bar_list.items()):
        axis.bar(
            x=group_positions + (idx - mid) * bar_width,
            height=np.round(np.array(data["time_span_minutes"]) / 60.0, 2),
            width=bar_width,
            label=label,
            color=data["color"],
        )

    axis.set_xlabel("Groups")
    axis.set_ylabel("Time Span in Hours")
    axis.set_title("Bar Chart of Time Spans")
    axis.set_xticks(group_positions)

    dates = [
        date[5:] for date in dates
    ]  # remove year, e.g. 2021-03-18 -> 03-18, since it will couse X axis label overlap
    weekdays = get_weekdays(day_timestamps)
    # zip the dates and weekdays, like 03-18\nMON
    dates = [f"{date}\n{weekday}" for date, weekday in zip(dates, weekdays)]
    axis.set_xticklabels([f"{dates[i]}" for i in range(num_dates)])

    axis.legend()

    plt.show()
