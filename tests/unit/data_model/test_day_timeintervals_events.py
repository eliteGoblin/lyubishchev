from dataclasses import dataclass
from typing import List

import arrow

from lyubishchev.data_model import (
    DayRecord,
    Event,
    InvalidDayRecord,
    Metadata,
    TimeInterval,
    validate_events,
    validate_time_intervals_match_events,
    validate_time_intervals_order,
)

# import pytest


def test_validate_time_intervals_order() -> None:
    @dataclass
    class TestCase:
        description: str
        input: DayRecord
        expect_success: bool

    testcases: List[TestCase] = [
        TestCase(
            description="empty TimeIntervals should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.now(),
                time_intervals=[],
            ),
            expect_success=False,
        ),
        TestCase(
            description="TimeIntervals disorder should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.now(),
                time_intervals=[
                    TimeInterval(
                        timestamp=arrow.now().shift(hours=-8),
                        duration_minutes=10,
                        metadata=Metadata(),
                        extra_info="",
                    ),
                    TimeInterval(
                        timestamp=arrow.now().shift(hours=-9),
                        duration_minutes=10,
                        metadata=Metadata(),
                        extra_info="",
                    ),
                    TimeInterval(
                        timestamp=arrow.now().shift(hours=-10),
                        duration_minutes=10,
                        metadata=Metadata(),
                        extra_info="",
                    ),
                ],
            ),
            expect_success=False,
        ),
        TestCase(
            description="TimeIntervals disorder larger than 5 mins should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.now(),
                time_intervals=[
                    TimeInterval(
                        timestamp=arrow.get("1986-01-01T00:00:00+00:00"),
                        duration_minutes=15,
                        metadata=Metadata(),
                        extra_info="",
                    ),
                    TimeInterval(
                        timestamp=arrow.get("1986-01-01T00:05:00+00:00"),
                        duration_minutes=10,
                        metadata=Metadata(),
                        extra_info="",
                    ),
                ],
            ),
            expect_success=False,
        ),
        TestCase(
            description="TimeIntervals disorder within 5 mins should fail, too (no tolerance)",
            input=DayRecord(
                wakeup_timestamp=arrow.now(),
                time_intervals=[
                    TimeInterval(
                        timestamp=arrow.get("1987-01-01T00:00:00+00:00"),
                        duration_minutes=10,
                        metadata=Metadata(),
                        extra_info="",
                    ),
                    TimeInterval(
                        timestamp=arrow.get("1987-01-01T00:08:00+00:00"),
                        duration_minutes=20,
                        metadata=Metadata(),
                        extra_info="",
                    ),
                ],
            ),
            expect_success=False,
        ),
    ]

    for index, case in enumerate(testcases):
        assert_msg: str = f"case {index} failed"
        try:
            validate_time_intervals_order(case.input)
        except InvalidDayRecord as exp:
            print(exp)
            assert not case.expect_success, assert_msg
        except ValueError:
            print(assert_msg)
            raise
        else:
            assert case.expect_success, assert_msg


def test_validate_events() -> None:
    @dataclass
    class TestCase:
        description: str
        input: DayRecord
        expect_success: bool

    testcases: List[TestCase] = [
        TestCase(
            description="empty events is ok",
            input=DayRecord(
                wakeup_timestamp=arrow.now(),
                events=[],
            ),
            expect_success=True,
        ),
        TestCase(
            description="events disorder should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.now(),
                events=[
                    Event(
                        metadata=Metadata(label={"event_type": "cold"}),
                        timestamp=arrow.get("1970-01-01T00:08:00+00:00"),
                    ),
                    Event(
                        metadata=Metadata(label={"event_type": "cold"}),
                        timestamp=arrow.get("1970-01-01T00:07:59+00:00"),
                    ),
                ],
            ),
            expect_success=False,
        ),
        TestCase(
            description="events contain bed related type should fail"
            "which should be filled into DayRecord then deleted",
            input=DayRecord(
                wakeup_timestamp=arrow.now(),
                events=[
                    Event(
                        metadata=Metadata(label={"event_type": "wakeup"}),
                        timestamp=arrow.get("1970-01-01T00:08:00+00:00"),
                    ),
                    Event(
                        metadata=Metadata(label={"event_type": "getup"}),
                        timestamp=arrow.get("1970-01-01T00:07:59+00:00"),
                    ),
                ],
            ),
            expect_success=False,
        ),
    ]

    for case in testcases:
        try:
            validate_events(case.input)
        except InvalidDayRecord as exp:
            print(exp)
            assert not case.expect_success
        else:
            assert case.expect_success


def test_validate_time_intervals_match_events() -> None:
    @dataclass
    class TestCase:
        description: str
        input: DayRecord
        expect_success: bool

    testcases: List[TestCase] = [
        TestCase(
            description="first interval before wakeup should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-23T05:15:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-23T23:15:58.970460+10:00"),
                time_intervals=[
                    TimeInterval(
                        timestamp=arrow.get("2000-05-23T05:00:58.970460+10:00"),
                        metadata=Metadata(),
                        extra_info="",
                        duration_minutes=0,
                    )
                ],
            ),
            expect_success=False,
        ),
        TestCase(
            description="last interval finish after bedtime should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-22T05:15:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-23T01:15:58.970460+10:00"),
                time_intervals=[
                    TimeInterval(
                        timestamp=arrow.get("2000-05-23T01:00:58.970460+10:00"),
                        duration_minutes=30,
                        metadata=Metadata(),
                        extra_info="",
                    )
                ],
            ),
            expect_success=False,
        ),
        TestCase(
            description="recorded time < 85% of day length should fail",
            input=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-22T05:15:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-23T01:15:58.970460+10:00"),
                time_intervals=[
                    TimeInterval(
                        timestamp=arrow.get("2000-05-22T10:00:58.970460+10:00"),
                        duration_minutes=6,
                        metadata=Metadata(),
                        extra_info="",
                    )
                ],
            ),
            expect_success=False,
        ),
        TestCase(
            description="time intervals with valid order, "
            "recorded time > 85% of day length should succeeded",
            input=DayRecord(
                wakeup_timestamp=arrow.get("2000-05-22T05:15:58.970460+10:00"),
                bed_timestamp=arrow.get("2000-05-23T01:15:58.970460+10:00"),
                time_intervals=[
                    TimeInterval(
                        timestamp=arrow.get("2000-05-22T05:16:58.970460+10:00"),
                        duration_minutes=1100,
                        metadata=Metadata(),
                        extra_info="",
                    )
                ],
            ),
            expect_success=True,
        ),
    ]
    for case in testcases:
        try:
            validate_time_intervals_match_events(case.input)
        except InvalidDayRecord as exp:
            print(case.description, exp)
            assert not case.expect_success
        except Exception as exp:
            print(case.description, exp)
            raise
        else:
            assert case.expect_success
