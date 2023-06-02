from typing import Any, Optional

from arrow import Arrow

from lyubishchev import config
from lyubishchev.data_model import (
    TYPE_BED,
    TYPE_GETUP,
    TYPE_WAKEUP,
    DayRecord,
    TimeInterval,
    must_yyyy_mm_dd,
    next_day,
    time_diff_minutes,
    timestamp_from_date_str,
)
from lyubishchev.search import Match, must_tag

# use minutes as unit, it's visualizer responsibility to decide how to display it(in hours, etc)


def total_minutes(start_date_str: str, end_date_str: str) -> int:
    must_yyyy_mm_dd(start_date_str)
    must_yyyy_mm_dd(end_date_str)

    if start_date_str >= end_date_str:
        return 0

    start = timestamp_from_date_str(date_str=start_date_str)
    end = timestamp_from_date_str(date_str=end_date_str)

    return time_diff_minutes(start, end)


def time_spans_matching_label_minutes(
    time_intervals: list[TimeInterval], match: Match
) -> list[int]:
    """
    Calculate time spans of time_intervals, matching label
    Return:
        list of original TimeInterval's time spans in minutes, not aggregated
    """
    time_spans = []

    matched_time_intervals = match.match(time_intervals)
    for time_interval in matched_time_intervals:
        time_spans.append(time_interval.duration_minutes)

    return time_spans


def time_spans_by_day_matching_label_minutes(
    day_records: list[DayRecord], match: Match
) -> list[int]:
    """
    Calculate time spans(duration of activity) of day, matching label
    Return:
        list of time spans in hours, one element for each day
    """
    time_spans = []

    for day in day_records:
        minuts_of_current_day = 0
        matched_time_intervals = match.match(day.time_intervals)
        for time_interval in matched_time_intervals:
            minuts_of_current_day += time_interval.duration_minutes
        time_spans.append(minuts_of_current_day)

    return time_spans


def time_spans_by_field_minutes(
    day_records: list[DayRecord], field_name: str
) -> list[int]:
    """
    return a list of time spans, one element for each day
    """
    res = []
    for day in day_records:
        res.append(int(getattr(day, field_name)))
    return res


def timestamps_of_days_by_field(
    day_records: list[DayRecord], field_name: str
) -> list[Arrow]:
    """
    timestamps_of_days returns a list of timestamps of a field in day_records array
    """
    res: list[Arrow] = []
    for day in day_records:
        timestamp: Arrow = getattr(day, field_name)
        if not isinstance(timestamp, Arrow):
            raise TypeError(f"field {field_name} of {day} is not a timestamp")
        res.append(timestamp)
    return res


def get_match_dict(name: str) -> dict[str, Any]:
    self_improving_dict = {
        "bibliotherapy": None,
        "linkedin": None,
        "lyubishchev": None,
        "oj": None,
        "software": None,
        "audible": None,
    }
    self_improving_tech = {
        "linkedin": None,
        "lyubishchev": None,
        "oj": None,
        "software": None,
    }
    self_improving_non_tech = {
        k: v for k, v in self_improving_dict.items() if k not in self_improving_tech
    }

    abstract_label_match_dict = {
        "self_improving": self_improving_dict,
        "self_improving_tech": self_improving_tech,
        "self_improving_non_tech": self_improving_non_tech,
        "work_all": {
            "work": None,
            "job": None,
        },
        "sex_all": {
            "sex": None,
            "mbate": None,
        },
        "exercise": {
            "jog": None,
            "swim": None,
            "anaerobic": None,
        },
        "calm": {
            "meditation": None,
            "walk": None,
        },
        "intangible": {
            "friends": None,
            "family": None,
            "lisha": None,
            "dating": None,
        },
        "regret": {
            "pmo": None,
            "numb": None,
            "dispute": None,
            "video_game": None,
            "internet": None,
        },
        "routine_all": {
            "cook": None,
            "self_routine": None,
            "housework": None,
            "meal": None,
        },
        "solitude": {
            "novel": None,
            "karaoke": None,
            "non-fiction": None,
        },
    }
    return abstract_label_match_dict[name]


def remove_year(dates: list[str]) -> list[str]:
    # remove year, e.g. 2021-03-18 -> 03-18, since it will couse X axis label overlap
    return [date[5:] for date in dates]


def get_weekdays(timestamps: list[Arrow]) -> list[str]:
    return [timestamp.format("ddd") for timestamp in timestamps]


class DayRangeReport:
    """
    DayRangeReport represents a report of a range of days, design doc in docs/day_range_report.md
    """

    day_records: list[DayRecord]

    def __init__(self, day_records: list[DayRecord]):
        self.day_records = day_records

    def __len__(self) -> int:
        return len(self.day_records)

    @property
    def report_unit(self) -> str:
        return "minutes"

    @property
    def start_date_str(self) -> str:
        return self.day_records[0].date_str()

    @property
    def end_date_str(self) -> str:
        return next_day(
            timezone_name=config.get_iana_timezone_name(),
            date_str=self.day_records[-1].date_str(),
        )

    def dates(
        self, is_remove_year: bool = False, is_add_weekday: bool = False
    ) -> list[str]:
        dates_res = [day.date_str() for day in self.day_records]
        if not is_remove_year and not is_add_weekday:
            return dates_res
        day_timestamps = self.get_event_metrics()["wakeup"]
        if is_remove_year:
            dates_res = remove_year(dates_res)
        if is_add_weekday:
            weekdays = get_weekdays(day_timestamps)
            dates_res = [
                f"{date}\n{weekday}" for date, weekday in zip(dates_res, weekdays)
            ]
        # fix bug seems in Jupyter: 05-01 plot won't show, changed to 05/01
        dates_res_workaround = []
        for date_str in dates_res:
            dates_res_workaround.append(date_str.replace("-", "/"))
        return dates_res_workaround

    def get_interval_metrics(self) -> dict[str, Any]:
        """
        Mainly for hightlights; for drill down, avoid using this in case extra coupling
        data structure if nested, depends on how you want to visualize it
        If you want to show night_sleep and nap separately in overall piechart,
            make them separte, here group them together in sleep_all
        """
        return {
            "effective_output": {
                "self_improving": time_spans_by_day_matching_label_minutes(
                    self.day_records,
                    Match.from_dict(get_match_dict("self_improving")),
                ),
                "work": time_spans_by_day_matching_label_minutes(
                    self.day_records,
                    Match.from_dict(get_match_dict("work_all")),
                ),
            },
            "sex_all": {
                "sex": time_spans_by_day_matching_label_minutes(
                    self.day_records, Match.from_dict({"sex": None})
                ),
                "mbate": time_spans_by_day_matching_label_minutes(
                    self.day_records, Match.from_dict({"mbate": None})
                ),
            },
            "exercise": time_spans_by_day_matching_label_minutes(
                self.day_records,
                Match.from_dict(get_match_dict("exercise")),
            ),
            "sleep_all": {
                "night_sleep": time_spans_by_field_minutes(
                    self.day_records, "last_night_sleep_minutes"
                ),
                "nap": time_spans_by_day_matching_label_minutes(
                    self.day_records,
                    Match.from_dict(
                        {
                            "nap": None,
                        }
                    ),
                ),  # TYPE_SLEEP only means nap, night sleep is not recorded and derived from bed and wakeup time
            },
            "calm": time_spans_by_day_matching_label_minutes(
                self.day_records,
                Match.from_dict(get_match_dict("calm")),
            ),
            "intangible": time_spans_by_day_matching_label_minutes(
                self.day_records,
                Match.from_dict(get_match_dict("intangible")),
            ),
            "regret": time_spans_by_day_matching_label_minutes(
                self.day_records,
                Match.from_dict(get_match_dict("regret")),
            ),
            "routine_all": time_spans_by_day_matching_label_minutes(
                self.day_records,
                Match.from_dict(get_match_dict("routine_all")),
            ),
            "solitude": time_spans_by_day_matching_label_minutes(
                self.day_records,
                Match.from_dict(get_match_dict("solitude")),
            ),
        }

    def get_long_format_data_list(
        self, tag: str, key_name_in_res: str, match: Optional[Match] = None
    ) -> list[dict[str, Any]]:
        """
        Given a single label or tag, return matched data, as long format dict
        Return: list of dict, contain date and minutes, with key_name_in_res:tag
        e.g input: tag=jog key_name_in_res=exercise
        res will contain exercise=jog also date and minutes keys
        [
            {'date': 'Monday', 'exercise': 'jog', 'minutes': 10},
            {'date': 'Tuesday', 'exercise': 'jog', 'minutes': 10},
        ]
        """
        must_tag(tag)
        res = []
        dates = self.dates(is_remove_year=True, is_add_weekday=True)
        for i, day in enumerate(self.day_records):
            day_res = {}
            if match is None:  # if match not passed in,
                match = Match.from_dict({tag: None})
            matched_time_intervals = match.match(day.time_intervals)
            minutes_of_day = sum(
                time_interval.duration_minutes
                for time_interval in matched_time_intervals
            )
            # even no match, generate a record with 0 minutes for that day
            #   to explicitly show that day has no such tag
            day_res = {
                "date": dates[i],
                key_name_in_res: tag,
                "minutes": minutes_of_day,
            }
            res.append(day_res)

        return res

    def get_total_minutes(self) -> int:
        minutes: int = total_minutes(
            self.day_records[0].date_str(),
            next_day(
                timezone_name=config.get_iana_timezone_name(),
                date_str=self.day_records[-1].date_str(),
            ),
        )
        return minutes

    def get_time_intervals(self) -> list[TimeInterval]:
        time_intervals: list[TimeInterval] = []
        for day in self.day_records:
            time_intervals.extend(day.time_intervals)
        return time_intervals

    def get_event_metrics(self) -> dict[str, list[Arrow]]:
        suffix = "_timestamp"
        return {
            "wakeup": timestamps_of_days_by_field(
                self.day_records, TYPE_WAKEUP + suffix
            ),
            "getup": timestamps_of_days_by_field(self.day_records, TYPE_GETUP + suffix),
            "bed": timestamps_of_days_by_field(self.day_records, TYPE_BED + suffix),
        }
