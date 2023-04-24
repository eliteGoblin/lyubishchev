from dataclasses import dataclass
from typing import List

import arrow

from lyubishchev.data_model import (
    DayRecord,
    InvalidDayRecord,
    Metadata,
    TimeInterval,
    validate_required_fields,
    validate_time_order,
    validate_value_range,
)

# Syd:
#   AEST(UTC +10) Apr - Sep
#   AEDT(UTC +11) others


def test_date_str() -> None:
    @dataclass
    class TestCase:
        description: str
        input_day: DayRecord
        expected_date_str: str

    testcases: List[TestCase] = [
        TestCase(
            description="for Sydney AEDT time: 2000-01-23 05:15, date is correct",
            input_day=DayRecord(
                wakeup_timestamp=arrow.get("2000-01-23T05:15:58.970460+11:00"),
            ),
            expected_date_str="2000-01-23",
        ),
        TestCase(
            description="for Sydney AEST time: 2000-05-23 05:15, date should be correct",
            input_day=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T05:15:58.970460+10:00"),
            ),
            expected_date_str="2000-05-23",
        ),
        TestCase(
            description="for Beijing time: 1986-01-23 05:15, date is correct",
            input_day=DayRecord(
                wakeup_timestamp=arrow.get("1986-01-23T05:15:58.970460+08:00"),
            ),
            expected_date_str="1986-01-23",
        ),
    ]

    for case in testcases:
        assert case.input_day.date_str() == case.expected_date_str\

def test_recorded_minutes() -> None:
    @dataclass
    class TestCase:
        description: str
        input_day: DayRecord
        expected: int

    testcases: List[TestCase] = [
        TestCase(
            description="recorded minutes should be accumulation of all intervals",
            input_day=DayRecord(
                time_intervals=[
                    TimeInterval(
                        metadata=Metadata(label={"type": "routine"}),
                        duration_minutes=10,
                    ),
                    TimeInterval(
                        metadata=Metadata(label={"type": "sleep"}),
                        duration_minutes=30,
                    ),
                    TimeInterval(
                        metadata=Metadata(label={"type": "relax"}),
                        duration_minutes=50,
                    ),
                    TimeInterval(
                        metadata=Metadata(label={"type": "self-improving"}),
                        duration_minutes=20,
                    ),
                ],
            ),
            expected=110,
        ),
    ]
    for case in testcases:
        assert case.input_day.recorded_minutes == case.expected


def test_day_validate_required_fields() -> None:
    valid_time_intervals: List[TimeInterval] = [
        TimeInterval(timestamp=arrow.now().shift(hours=-10)),
        TimeInterval(timestamp=arrow.now().shift(hours=-9)),
        TimeInterval(timestamp=arrow.now().shift(hours=-8)),
    ]

    @dataclass
    class TestCase:
        description: str
        input: DayRecord
        expect_success: bool

    testcases: List[TestCase] = [
        TestCase(
            description="DayRecord has all required fields should pass",
            input=DayRecord(
                wakeup_timestamp=arrow.now().shift(hours=-10),
                getup_timestamp=arrow.now().shift(hours=-9),
                bed_timestamp=arrow.now(),
                last_night_sleep_minutes=11 * 60,
                time_intervals=valid_time_intervals,
            ),
            expect_success=True,
        ),
        TestCase(
            description="DayRecord missing wakeup_timestamp should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.now().shift(hours=-9),
                bed_timestamp=arrow.now(),
                last_night_sleep_minutes=11 * 60,
                time_intervals=valid_time_intervals,
            ),
            expect_success=False,
        ),
    ]

    for case in testcases:
        try:
            validate_required_fields(case.input)
        except (AttributeError, InvalidDayRecord) as exp:
            print(exp)
            assert not case.expect_success
        else:
            assert case.expect_success


def test_validate_value_range() -> None:
    @dataclass
    class TestCase:
        description: str
        input: DayRecord
        expect_success: bool

    testcases: List[TestCase] = [
        TestCase(
            description="DayRecord fields range valid should pass",
            input=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T05:15:58.970460+10:00"),
                getup_timestamp=arrow.get("2000-05-23T05:40:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-24T01:01:58.970460+10:00"),
                last_night_sleep_minutes=11 * 60,
                timezone_name="Australia/Sydney",
            ),
            expect_success=True,
        ),
        TestCase(
            description="DayRecord fields invalid wakeup should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T18:15:58.970460+10:00"),
                getup_timestamp=arrow.get("2000-05-23T05:40:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-24T01:01:58.970460+10:00"),
                last_night_sleep_minutes=11 * 60,
                timezone_name="Australia/Sydney",
            ),
            expect_success=False,
        ),
        TestCase(
            description="DayRecord fields invalid bedtime should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T05:15:58.970460+10:00"),
                getup_timestamp=arrow.get("2000-05-23T05:40:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-24T17:01:58.970460+10:00"),
                last_night_sleep_minutes=11 * 60,
                timezone_name="Australia/Sydney",
            ),
            expect_success=False,
        ),
        TestCase(
            description="DayRecord fields last night sleep should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T05:15:58.970460+10:00"),
                getup_timestamp=arrow.get("2000-05-23T05:40:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-24T17:01:58.970460+10:00"),
                last_night_sleep_minutes=18 * 60,
                timezone_name="Australia/Sydney",
            ),
            expect_success=False,
        ),
    ]

    for case in testcases:
        try:
            validate_value_range(case.input)
        except (AttributeError, InvalidDayRecord) as exp:
            print(exp)
            assert not case.expect_success
        else:
            assert case.expect_success


def test_validate_time_order() -> None:
    @dataclass
    class TestCase:
        description: str
        input_day: DayRecord
        expect_success: bool

    testcases: List[TestCase] = [
        TestCase(
            description="DayRecord with timestamp in order should pass",
            input_day=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T05:15:58.970460+10:00"),
                getup_timestamp=arrow.get("2000-05-23T05:40:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-24T01:01:58.970460+10:00"),
            ),
            expect_success=True,
        ),
        TestCase(
            description="DayRecord 2 with timestamp in order should pass",
            input_day=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T03:15:58.970460+10:00"),
                getup_timestamp=arrow.get("2000-05-23T05:40:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-24T03:01:58.970460+10:00"),
            ),
            expect_success=True,
        ),
        TestCase(
            description="DayRecord invalid timestamp order should fail",
            input_day=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T06:15:58.970460+10:00"),
                getup_timestamp=arrow.get("2000-05-23T05:40:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-24T03:01:58.970460+10:00"),
            ),
            expect_success=False,
        ),
        TestCase(
            description="DayRecord 2 invalid timestamp order should fail",
            input_day=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T05:15:58.970460+10:00"),
                getup_timestamp=arrow.get("2000-05-23T05:40:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-23T03:01:58.970460+10:00"),
            ),
            expect_success=False,
        ),
    ]

    for case in testcases:
        try:
            validate_time_order(case.input_day)
        except InvalidDayRecord as exp:
            print(exp)
            assert not case.expect_success
        else:
            assert case.expect_success
