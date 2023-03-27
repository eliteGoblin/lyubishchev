from typing import Optional

import matplotlib.pyplot as plt
from arrow import Arrow

from lyubishchev.data_model import day_start_timestamp_early_bound

from .nb_helper_util import remove_year_add_weekday


def timestamp_diff(timestamp: Arrow, base_timestamp: Optional[Arrow] = None) -> float:

    if base_timestamp is None:
        start_of_day = timestamp.floor("day")
    else:
        start_of_day = base_timestamp.floor("day")

    difference = timestamp - start_of_day
    offset_hours = difference.seconds / 3600

    return round(offset_hours, 2)


def draw_wakeup_plot(
    wakeup_timestamps: list[Arrow],
    dates: list[str],
) -> None:
    dates = remove_year_add_weekday(
        dates=dates,
        day_timestamps=wakeup_timestamps,
    )
    diff_hours = [timestamp_diff(tm) for tm in wakeup_timestamps]
    _, axis = plt.subplots()
    axis.plot(dates, diff_hours, marker="o", linestyle="-", linewidth=2)

    axis.set_xlabel("Wakeup Hour Offset")
    axis.set_ylabel("Dates of Day")

    # Display the plot
    plt.show()


def draw_bed_plot(
    bed_timestamps: list[Arrow],
    dates: list[str],
) -> None:
    """
    bedtime can be after midnight, so when calculate offset, we can't always the start of sameday,
        we need to calculate the start of previous day
    """
    base_timestamps = [day_start_timestamp_early_bound(date) for date in dates]
    diff_hours = []
    for idx, timestamp in enumerate(bed_timestamps):
        diff_hours.append(timestamp_diff(timestamp, base_timestamps[idx]))

    dates = remove_year_add_weekday(
        dates=dates,
        day_timestamps=bed_timestamps,
    )

    _, axis = plt.subplots()
    axis.plot(dates, diff_hours, marker="o", linestyle="-", linewidth=2)

    axis.set_xlabel("Bed Hour Offset")
    axis.set_ylabel("Dates of Day")

    # Display the plot
    plt.show()
