import pandas as pd
import plotly.express as px

from lyubishchev.report import DayRangeReport, time_spans_by_field_minutes


def stack_bar_sleep_all(report: DayRangeReport) -> None:
    # get nap data first
    sleep_res = report.get_long_format_data_list("nap", "sleep")
    # add night sleep data
    night_sleeps = time_spans_by_field_minutes(
        report.day_records, "last_night_sleep_minutes"
    )
    dates = report.dates(is_add_weekday=True, is_remove_year=True)

    for i, night_sleep in enumerate(night_sleeps):
        df_item = {"date": dates[i], "minutes": night_sleep, "sleep": "night_sleep"}

        sleep_res.append(df_item)

    res_data_frame = pd.DataFrame(sleep_res)

    res_data_frame["hours"] = (res_data_frame["minutes"] / 60).round(2)  # type: ignore
    res_data_frame.drop("minutes", axis=1, inplace=True)

    fig = px.bar(
        res_data_frame,
        x="date",
        y="hours",
        color="sleep",
        text="hours",
        title="Sleep Duration by Weekday",
        labels={"date": "Weekday", "hours": "Hours"},
    )

    fig.update_layout(
        # autosize=False,  # Disable autosizing
        # width=800,  # Set the plot width
        # height=500,  # Set the plot height
        # margin=dict(l=50, r=50, b=100, t=100, pad=4),
    )

    fig.show()
