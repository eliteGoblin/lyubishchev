# from typing import Any

# from arrow import Arrow

# from lyubishchev import config
# from lyubishchev.data_model import (
#     TYPE_BED,
#     TYPE_GETUP,
#     TYPE_WAKEUP,
#     DayRecord,
#     Label,
#     is_label_match,
#     must_yyyy_mm_dd,
#     next_day,
#     time_diff_minutes,
#     timestamp_from_date_str,
# )

# # use minutes as unit, it's visualizer responsibility to decide how to display it(in hours, etc)


# def total_minutes(start_date_str: str, end_date_str: str) -> int:
#     must_yyyy_mm_dd(start_date_str)
#     must_yyyy_mm_dd(end_date_str)

#     if start_date_str >= end_date_str:
#         return 0

#     start = timestamp_from_date_str(config.get_iana_timezone_name(), start_date_str)
#     end = timestamp_from_date_str(config.get_iana_timezone_name(), end_date_str)

#     return time_diff_minutes(start, end)


# def time_spans_by_day_matching_label_minutes(
#     day_records: list[DayRecord], label: Label
# ) -> list[int]:
#     """
#     Calculate time spans(duration of activity) of day, matching label
#     Return:
#         list of time spans in hours, one element for each day
#     """
#     time_spans = []
#     for day in day_records:
#         minuts_of_current_day = 0
#         for time_interval in day.time_intervals:
#             if is_label_match(time_interval.metadata.label, label):
#                 minuts_of_current_day += time_interval.duration_minutes
#         time_spans.append(minuts_of_current_day)
#     return time_spans


# def time_spans_by_field_minutes(
#     day_records: list[DayRecord], field_name: str
# ) -> list[int]:
#     """
#     return a list of time spans, one element for each day
#     """
#     res = []
#     for day in day_records:
#         res.append(int(getattr(day, field_name)))
#     return res


# def timestamps_of_days_by_field(
#     day_records: list[DayRecord], field_name: str
# ) -> list[Arrow]:
#     """
#     timestamps_of_days returns a list of timestamps of a field in day_records array
#     """
#     res: list[Arrow] = []
#     for day in day_records:
#         timestamp: Arrow = getattr(day, field_name)
#         if not isinstance(timestamp, Arrow):
#             raise TypeError(f"field {field_name} of {day} is not a timestamp")
#         res.append(timestamp)
#     return res


# class DayRangeReport:
#     """
#     DayRangeReport represents a report of a range of days, design doc in docs/day_range_report.md
#     """

#     day_records: list[DayRecord]

#     def __init__(self, day_records: list[DayRecord]):
#         self.day_records = day_records

#     def __len__(self) -> int:
#         return len(self.day_records)

#     @property
#     def report_unit(self) -> str:
#         return "minutes"

#     @property
#     def start_date_str(self) -> str:
#         return self.day_records[0].date_str()

#     @property
#     def end_date_str(self) -> str:
#         return next_day(
#             timezone_name=config.get_iana_timezone_name(),
#             date_str=self.day_records[-1].date_str(),
#         )

#     def dates(self) -> list[str]:
#         return [day.date_str() for day in self.day_records]

#     def get_interval_metrics(self) -> dict[str, Any]:
#         return {
#             "effective_output": {
#                 "self_improving": time_spans_by_day_matching_label_minutes(
#                     self.day_records,
#                     {TIME_INTERVAL_TYPE: TYPE_SELF_IMPROVING},
#                 ),
#                 "work": time_spans_by_day_matching_label_minutes(
#                     self.day_records, {TIME_INTERVAL_TYPE: TYPE_WORK}
#                 ),
#             },
#             "sex": time_spans_by_day_matching_label_minutes(
#                 self.day_records, {TIME_INTERVAL_TYPE: TYPE_SEX}
#             ),
#             "exercise": time_spans_by_day_matching_label_minutes(
#                 self.day_records, {TIME_INTERVAL_TYPE: TYPE_EXERCISE}
#             ),
#             "sleep": {
#                 "night_sleep": time_spans_by_field_minutes(
#                     self.day_records, "last_night_sleep_minutes"
#                 ),
#                 "nap": time_spans_by_day_matching_label_minutes(
#                     self.day_records, {TIME_INTERVAL_TYPE: TYPE_SLEEP}
#                 ),  # TYPE_SLEEP only means nap, night sleep is not recorded and derived from bed and wakeup time
#             },
#             "meditation": time_spans_by_day_matching_label_minutes(
#                 self.day_records, {TIME_INTERVAL_TYPE: TYPE_MEDITATION}
#             ),
#             "walk": time_spans_by_day_matching_label_minutes(
#                 self.day_records, {TIME_INTERVAL_TYPE: TYPE_WALK}
#             ),
#             "connection": time_spans_by_day_matching_label_minutes(
#                 self.day_records, {TIME_INTERVAL_TYPE: TYPE_CONNECTION}
#             ),
#             # time I regret
#             "pmo": time_spans_by_day_matching_label_minutes(
#                 self.day_records, {TIME_INTERVAL_TYPE: TYPE_PMO}
#             ),
#             "numb": time_spans_by_day_matching_label_minutes(
#                 self.day_records, {TIME_INTERVAL_TYPE: TYPE_NUMB}
#             ),
#             "dispute": time_spans_by_day_matching_label_minutes(
#                 self.day_records, {TIME_INTERVAL_TYPE: TYPE_DISPUTE}
#             ),
#             # other
#             "routine": time_spans_by_day_matching_label_minutes(
#                 self.day_records, {TIME_INTERVAL_TYPE: TYPE_ROUTINE}
#             ),
#         }

#     def get_time_stats(self) -> dict[str, int]:
#         """
#         get_time_stats returns a dict of time stats
#         """
#         interval_metrics = self.get_interval_metrics()

#         minutes: int = total_minutes(
#             self.day_records[0].date_str(),
#             next_day(
#                 timezone_name=config.get_iana_timezone_name(),
#                 date_str=self.day_records[-1].date_str(),
#             ),
#         )

#         return {
#             "total": minutes,
#             "sleep_all": sum(interval_metrics["sleep"]["night_sleep"])
#             + sum(interval_metrics["sleep"]["nap"]),
#             "sleep_night": sum(interval_metrics["sleep"]["night_sleep"]),
#             "sleep_nap": sum(interval_metrics["sleep"]["nap"]),
#             "work": sum(interval_metrics["effective_output"]["work"]),
#             "exercise": sum(interval_metrics["exercise"]),
#             "self_improving": sum(
#                 interval_metrics["effective_output"]["self_improving"]
#             ),
#             "sex": sum(interval_metrics["sex"]),
#         }

#     def get_event_metrics(self) -> dict[str, list[Arrow]]:
#         suffix = "_timestamp"
#         return {
#             "wakeup": timestamps_of_days_by_field(
#                 self.day_records, TYPE_WAKEUP + suffix
#             ),
#             "getup": timestamps_of_days_by_field(self.day_records, TYPE_GETUP + suffix),
#             "bed": timestamps_of_days_by_field(self.day_records, TYPE_BED + suffix),
#         }
