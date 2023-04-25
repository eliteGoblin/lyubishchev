from dataclasses import dataclass
from datetime import datetime

import arrow
import pytest

from lyubishchev.data_model import (
    Event,
    Metadata,
    TimeInterval,
    TimeSeriesNotFound,
    get_time_intervals_for_single_day,
)


def test_get_time_intervals_for_single_day_expect_fail() -> None:
    single_day_events: list[Event] = [
        Event(
            timestamp=arrow.get(datetime(2022, 7, 1, 20, 50, 21), "Australia/Sydney"),
            metadata=Metadata(
                label={
                    "event_type": "bed",
                }
            ),
        ),
        Event(
            timestamp=arrow.get(datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"),
            metadata=Metadata(
                label={
                    "event_type": "wakeup",
                }
            ),
        ),
        Event(
            timestamp=arrow.get(datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"),
            metadata=Metadata(
                label={
                    "event_type": "bed",
                }
            ),
        ),
    ]

    @dataclass
    class TestCase:
        description: str
        time_intervals: list[TimeInterval]

    testcases: list[TestCase] = [
        TestCase(
            description="no time interval after wakeup should fail",
            time_intervals=[],
        ),
        TestCase(
            description="no time interval after wakeup should fail",
            time_intervals=[
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 20), "Australia/Sydney"
                    ),
                    metadata=Metadata(),
                    extra_info="",
                    duration_minutes=0,
                )
            ],
        ),
        TestCase(
            description="no time interval after wakeup should fail",
            time_intervals=[
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 20), "Australia/Sydney"
                    ),
                    metadata=Metadata(),
                    extra_info="",
                    duration_minutes=0,
                )
            ],
        ),
    ]

    for case in testcases:
        with pytest.raises(TimeSeriesNotFound):
            get_time_intervals_for_single_day(
                date_range_intervals=case.time_intervals,
                current_day_events=single_day_events,
            )


def test_get_time_intervals_for_single_day() -> None:
    # time interval same timestamp should pass
    # only 1 time interval should pass
    # time interval same timestamp should pass
    # only 1 time interval should pass
    single_day_events: list[Event] = [
        Event(
            timestamp=arrow.get(datetime(2022, 7, 1, 20, 50, 21), "Australia/Sydney"),
            metadata=Metadata(
                label={
                    "event_type": "bed",
                }
            ),
        ),
        Event(
            timestamp=arrow.get(datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"),
            metadata=Metadata(
                label={
                    "event_type": "wakeup",
                }
            ),
        ),
        Event(
            timestamp=arrow.get(datetime(2022, 7, 2, 20, 50, 21), "Australia/Sydney"),
            metadata=Metadata(
                label={
                    "event_type": "bed",
                }
            ),
        ),
    ]

    @dataclass
    class TestCase:
        description: str
        time_intervals: list[TimeInterval]
        expected_time_intervals: list[TimeInterval]

    testcases: list[TestCase] = [
        TestCase(
            description="time intervals with wakeup in first time intervals and bed in last time intervals should pass",
            time_intervals=[
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"
                    ),
                    extra_info="morning wakeup",
                    duration_minutes=90,
                    metadata=Metadata(),
                ),
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    extra_info="routine",
                    duration_minutes=120,
                    metadata=Metadata(),
                ),
            ],
            expected_time_intervals=[
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"
                    ),
                    extra_info="morning wakeup",
                    duration_minutes=90,
                    metadata=Metadata(),
                ),
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    extra_info="routine",
                    duration_minutes=120,
                    metadata=Metadata(),
                ),
            ],
        ),
        TestCase(
            description="skip the time intervals start from today's bed time event",
            time_intervals=[
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"
                    ),
                    extra_info="morning wakeup",
                    duration_minutes=90,
                    metadata=Metadata(),
                ),
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    extra_info="routine",
                    duration_minutes=120,
                    metadata=Metadata(),
                ),
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 20, 50, 21), "Australia/Sydney"
                    ),
                    extra_info="shouldn't include me, because I'm after today's bed time event",
                    duration_minutes=120,
                    metadata=Metadata(),
                ),
            ],
            expected_time_intervals=[
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"
                    ),
                    extra_info="morning wakeup",
                    duration_minutes=90,
                    metadata=Metadata(),
                ),
                TimeInterval(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    extra_info="routine",
                    duration_minutes=120,
                    metadata=Metadata(),
                ),
            ],
        ),
    ]

    for i, case in enumerate(testcases):
        assert_message = f"case {i} failed! {case.description}"
        res = get_time_intervals_for_single_day(
            date_range_intervals=case.time_intervals,
            current_day_events=single_day_events,
        )
        assert case.expected_time_intervals == res, assert_message
