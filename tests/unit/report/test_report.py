from dataclasses import dataclass

import arrow

from lyubishchev.data_model import (
    TIME_INTERVAL_TYPE,
    TYPE_SELF_IMPROVING,
    TYPE_SLEEP,
    TYPE_WORK,
    DayRecord,
    Label,
)
from lyubishchev.report import (
    DayRangeReport,
    time_spans_by_day_matching_label_minutes,
    time_spans_by_field_minutes,
    timestamps_of_days_by_field,
    total_minutes,
)

from .test_data.march_12_16_2023 import day_records_2023_march_12_16

# import pytest
# from icecream import ic


def test_total_hours() -> None:
    @dataclass
    class TestCase:
        start_date: str
        end_date: str
        expected: float

    testcases = [
        TestCase(
            start_date="2021-01-01",
            end_date="2021-01-01",
            expected=0,
        ),
        TestCase(
            start_date="2021-01-01",
            end_date="2021-01-02",
            expected=24 * 60,
        ),
        TestCase(
            start_date="2021-01-01",
            end_date="2022-03-02",
            expected=425 * 24 * 60,
        ),
    ]

    for i, testcase in enumerate(testcases):
        assert_message = f"testcase {i} failed"
        assert (
            total_minutes(testcase.start_date, testcase.end_date) == testcase.expected
        ), assert_message


def test_time_spans_by_day_matching_label() -> None:
    @dataclass
    class TestCase:
        day_records: list[DayRecord]
        label: Label
        expected: list[float]

    testcases = [
        TestCase(
            day_records=day_records_2023_march_12_16()[0:1],
            label={TIME_INTERVAL_TYPE: TYPE_WORK},
            expected=[0],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16()[1:2],
            label={TIME_INTERVAL_TYPE: TYPE_WORK},
            expected=[170],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16()[2:3],
            label={TIME_INTERVAL_TYPE: TYPE_WORK},
            expected=[137],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16()[3:4],
            label={TIME_INTERVAL_TYPE: TYPE_WORK},
            expected=[211],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16(),
            label={TIME_INTERVAL_TYPE: TYPE_WORK},
            expected=[0, 170, 137, 211],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16(),
            label={TIME_INTERVAL_TYPE: TYPE_SLEEP},
            expected=[0, 55, 0, 88],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16(),
            label={TIME_INTERVAL_TYPE: TYPE_SELF_IMPROVING},
            expected=[358, 367, 205, 198],
        ),
    ]

    for i, testcase in enumerate(testcases):
        res = time_spans_by_day_matching_label_minutes(
            testcase.day_records, testcase.label
        )
        assert_message = (
            f"testcase {i} failed, expected: {testcase.expected}, got {res}"
        )
        assert testcase.expected == res, assert_message


def test_time_spans_night_sleep() -> None:
    res = time_spans_by_field_minutes(
        day_records_2023_march_12_16(), "last_night_sleep_minutes"
    )
    assert [570, 390, 500, 490] == res, f"expected: [], got: {res}"


def test_timestamps_of_days_by_field() -> None:
    res = timestamps_of_days_by_field(
        day_records_2023_march_12_16(), "wakeup_timestamp"
    )
    assert res == [
        arrow.get("2023-03-12T08:00:00+11:00"),
        arrow.get("2023-03-13T04:00:00+11:00"),
        arrow.get("2023-03-14T05:05:00+11:00"),
        arrow.get("2023-03-15T05:40:00+11:00"),
    ]


def test_day_range_report_interval_metrics() -> None:
    report = DayRangeReport(day_records_2023_march_12_16())
    interval_metrics = report.get_interval_metrics()

    assert interval_metrics["effective_output"] == {
        "self_improving": [358, 367, 205, 198],
        "work": [0, 170, 137, 211],
    }

    assert interval_metrics["sex"] == [0, 0, 0, 0]
    assert interval_metrics["exercise"] == [0, 0, 31, 0]
    assert interval_metrics["sleep"] == {
        "night_sleep": [570, 390, 500, 490],
        "nap": [0, 55, 0, 88],
    }


def test_day_range_report_time_stats() -> None:
    report = DayRangeReport(day_records_2023_march_12_16())
    time_stats = report.get_time_stats()

    assert time_stats["total"] == 24 * 60 * 4
    assert time_stats["sleep_all"] == sum([570, 445, 500, 578])
    assert time_stats["sleep_night"] == sum([570, 390, 500, 490])
    assert time_stats["sleep_nap"] == sum([0, 55, 0, 88])
    assert time_stats["work"] == sum([0, 170, 137, 211])
    assert time_stats["self_improving"] == sum([358, 367, 205, 198])


def test_day_range_report_event_metrics() -> None:
    report = DayRangeReport(day_records_2023_march_12_16())
    event_metrics = report.get_event_metrics()

    assert event_metrics["wakeup"] == [
        arrow.get("2023-03-12T08:00:00+11:00"),
        arrow.get("2023-03-13T04:00:00+11:00"),
        arrow.get("2023-03-14T05:05:00+11:00"),
        arrow.get("2023-03-15T05:40:00+11:00"),
    ]

    assert event_metrics["getup"] == [
        arrow.get("2023-03-12T08:00:00+11:00"),
        arrow.get("2023-03-13T04:00:00+11:00"),
        arrow.get("2023-03-14T05:05:00+11:00"),
        arrow.get("2023-03-15T05:40:00+11:00"),
    ]

    assert event_metrics["bed"] == [
        arrow.get("2023-03-12T21:30:00+11:00"),
        arrow.get("2023-03-13T20:45:00+11:00"),
        arrow.get("2023-03-14T21:30:00+11:00"),
        arrow.get("2023-03-15T21:30:00+11:00"),
    ]
