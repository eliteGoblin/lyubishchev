from dataclasses import dataclass

import arrow

from lyubishchev.data_model import DayRecord, Label
from lyubishchev.report import (
    DayRangeReport,
    time_spans_by_day_matching_label_minutes,
    time_spans_by_field_minutes,
    timestamps_of_days_by_field,
    total_minutes,
)
from lyubishchev.search import Match

from .test_data.march_12_13_14 import day_records_2023_march_12_14
from .test_data.march_12_16_2023_legacy_label import day_records_2023_march_12_16


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
            label={"type": "work"},
            expected=[0],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16()[1:2],
            label={"type": "work"},
            expected=[170],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16()[2:3],
            label={"type": "work"},
            expected=[137],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16()[3:4],
            label={"type": "work"},
            expected=[211],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16(),
            label={"type": "work"},
            expected=[0, 170, 137, 211],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16(),
            label={"type": "sleep"},
            expected=[0, 55, 0, 88],
        ),
        TestCase(
            day_records=day_records_2023_march_12_16(),
            label={"type": "self-improving"},
            expected=[358, 367, 205, 198],
        ),
    ]

    for i, testcase in enumerate(testcases):
        key, label = list(testcase.label.items())[0]
        res = time_spans_by_day_matching_label_minutes(
            testcase.day_records,
            Match.from_dict(
                {
                    f"{key}={label}": None,
                }
            ),
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
    report = DayRangeReport(day_records_2023_march_12_14())
    interval_metrics = report.get_interval_metrics()

    assert interval_metrics["effective_output"] == {
        "self_improving": [358, 357],
        "work": [0, 170],
    }
    assert interval_metrics["sex_all"] == {
        "sex": [0, 0],
        "mbate": [0, 0],
    }
    assert interval_metrics["exercise"] == [0, 0]
    assert interval_metrics["sleep_all"] == {
        "night_sleep": [570, 390],
        "nap": [0, 55],
    }


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
