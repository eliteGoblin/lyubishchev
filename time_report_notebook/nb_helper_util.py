from arrow import Arrow


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
