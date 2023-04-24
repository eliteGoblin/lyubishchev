from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from arrow import Arrow

from .nb_helper_util import remove_year_add_weekday


def draw_bars_chart_legacy(
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

    dates = remove_year_add_weekday(
        dates=dates,
        day_timestamps=day_timestamps,
    )
    axis.set_xticklabels([f"{dates[i]}" for i in range(num_dates)])

    axis.legend()

    plt.show()


def show_effective_output_highlights(high_lights) -> None:
    print("effective_output:\t\t", high_lights["effective_output"])
    print("self_improving:\t\t\t", high_lights["self_improving"])
    print("work:\t\t\t\t", high_lights["work"])


def draw_stacked_bar_chats() -> None:
    raise NotImplementedError
