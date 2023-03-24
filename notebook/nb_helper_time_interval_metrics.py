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
