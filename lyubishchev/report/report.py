from typing import Any

from arrow import Arrow

from lyubishchev import config
from lyubishchev.data_model import TYPE_EXERCISE  # events
from lyubishchev.data_model import (
    TIME_INTERVAL_TYPE,
    TYPE_BED,
    TYPE_GETUP,
    TYPE_SELF_IMPROVING,
    TYPE_SEX,
    TYPE_SLEEP,
    TYPE_WAKEUP,
    TYPE_WORK,
    DayRecord,
    Label,
    TimeInterval,
    next_day,
)


def total_hours(day_records: list[DayRecord]) -> float:
    raise NotImplementedError


def time_spans_matching_label(
    day_records: list[DayRecord], label: Label
) -> list[TimeInterval]:
    raise NotImplementedError


def time_spans_night_sleep(day_records: list[DayRecord]) -> list[float]:
    raise NotImplementedError


def timestamps_of_days(day_records: list[DayRecord], field_name: str) -> list[Arrow]:
    """
    timestamps_of_days returns a list of timestamps of a field in day_records array
    """
    raise NotImplementedError


class DayRangeReport:
    """
    DayRangeReport represents a report of a range of days, design doc in docs/day_range_report.md
    """

    day_records: list[DayRecord]

    def __init__(self, day_records: list[DayRecord]):
        self.day_records = day_records

    @property
    def start_date_str(self) -> str:
        return self.day_records[0].date_str()

    @property
    def end_date_str(self) -> str:
        return next_day(
            timezone_name=config.get_iana_timezone_name(),
            date_str=self.day_records[-1].date_str(),
        )

    def get_interval_metrics(self) -> dict[str, Any]:
        return {
            "effective_output": {
                "self_improving": time_spans_matching_label(
                    self.day_records,
                    {TIME_INTERVAL_TYPE: TYPE_SELF_IMPROVING},
                ),
                "work": time_spans_matching_label(
                    self.day_records, {TIME_INTERVAL_TYPE: TYPE_WORK}
                ),
            },
            "sex": time_spans_matching_label(
                self.day_records, {TIME_INTERVAL_TYPE: TYPE_SEX}
            ),
            "exercise": time_spans_matching_label(
                self.day_records, {TIME_INTERVAL_TYPE: TYPE_EXERCISE}
            ),
            "sleep": {
                "night_hours": time_spans_night_sleep(self.day_records),
                "nap": time_spans_matching_label(
                    self.day_records, {TIME_INTERVAL_TYPE: TYPE_SLEEP}
                ),  # TYPE_SLEEP only means nap, night sleep is not recorded and derived from bed and wakeup time
            },
        }

    def get_time_stats(self) -> dict[str, float]:
        """
        get_time_stats returns a dict of time stats
        """
        interval_metrics = self.get_interval_metrics()
        return {
            "total": total_hours(self.day_records),
            "sleep": sum(interval_metrics["sleep"]["night_hours"])
            + sum(interval_metrics["sleep"]["nap"]),
            "work": sum(interval_metrics["effective_output"]["work"]),
            "exercise": sum(interval_metrics["exercise"]),
            "self_improving": sum(
                interval_metrics["effective_output"]["self_improving"]
            ),
        }

    def get_event_metrics(self) -> dict[str, list[Arrow]]:
        return {
            "wakeup": timestamps_of_days(self.day_records, TYPE_WAKEUP),
            "getup": timestamps_of_days(self.day_records, TYPE_GETUP),
            "bed": timestamps_of_days(self.day_records, TYPE_BED),
        }
