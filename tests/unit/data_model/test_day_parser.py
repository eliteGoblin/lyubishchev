from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import arrow
import pytest
from arrow import Arrow

from lyubishchev.data_model import (
    DayRecord,
    Event,
    TimeInterval,
    date_range_to_timestamp_range,
    parse_and_generate_day_record,
    parse_and_generate_day_records,
)

from .test_data.july_2 import july_2_events_buffered, july_2_intervals


def test_date_range_to_timestamp_range() -> None:
    @dataclass
    class TestCase:
        description: str
        input_date_str_range: tuple[str, str]
        expect_success: bool
        expected_timestamp_range: Optional[tuple[Arrow, Arrow]]
        buffer_days: int = 0

    testcases: list[TestCase] = [
        TestCase(
            description="To get single day 2022 7.2",
            input_date_str_range=("2022-07-02", "2022-07-03"),
            expect_success=True,
            expected_timestamp_range=(
                arrow.get(datetime(2022, 7, 2), "Australia/Sydney"),
                arrow.get(datetime(2022, 7, 3, 18), "Australia/Sydney"),
            ),
        ),
        TestCase(
            description="To get days 2022 [7.3, 7.17)",
            input_date_str_range=("2022-07-03", "2022-07-17"),
            expect_success=True,
            expected_timestamp_range=(
                arrow.get(datetime(2022, 7, 3), "Australia/Sydney"),
                arrow.get(datetime(2022, 7, 17, 18), "Australia/Sydney"),
            ),
        ),
        TestCase(
            description="non yyyy-mm-dd format should raise",
            input_date_str_range=("07-02-2022", "2022-07-03"),
            expect_success=False,
            expected_timestamp_range=None,
        ),
        TestCase(
            description="non yyyy-mm-dd format should raise",
            input_date_str_range=("2022-07-03", "2022.07.04"),
            expect_success=False,
            expected_timestamp_range=None,
        ),
        TestCase(
            description="empty range should raise",
            input_date_str_range=("2022-07-02", "2022-07-02"),
            expect_success=False,
            expected_timestamp_range=None,
        ),
        TestCase(
            description="end date before start should raise",
            input_date_str_range=("2022-07-03", "2022-07-02"),
            expect_success=False,
            expected_timestamp_range=None,
        ),
        TestCase(
            description="To get days 2022 [7.2, 7.3), buffer 1 day",
            input_date_str_range=("2022-07-02", "2022-07-03"),
            buffer_days=1,
            expect_success=True,
            expected_timestamp_range=(
                arrow.get(datetime(2022, 7, 1), "Australia/Sydney"),
                arrow.get(datetime(2022, 7, 4, 18), "Australia/Sydney"),
            ),
        ),
        TestCase(
            description="To get days 2022 [7.2, 7.17), buffer 3 day",
            input_date_str_range=("2022-07-02", "2022-07-17"),
            buffer_days=3,
            expect_success=True,
            expected_timestamp_range=(
                arrow.get(datetime(2022, 6, 29), "Australia/Sydney"),
                arrow.get(datetime(2022, 7, 20, 18), "Australia/Sydney"),
            ),
        ),
    ]

    for case in testcases:
        try:
            res = date_range_to_timestamp_range(
                case.input_date_str_range[0],
                case.input_date_str_range[1],
                case.buffer_days,
            )
        except ValueError as exp:
            print(exp)
            assert not case.expect_success
        else:
            assert case.expect_success
            assert case.expected_timestamp_range == res


@pytest.mark.skip(reason="todo next, logic changed completely")
def test_parse_and_generate_day_record() -> None:
    @dataclass
    class TestCase:
        description: str
        events: list[Event]
        time_intervals: list[TimeInterval]
        day_search_start_timestamp: Arrow
        expect_success: bool
        expected_day_record: DayRecord

    testcases: list[TestCase] = [
        TestCase(
            description="",
            events=july_2_events_buffered,
            time_intervals=july_2_intervals,
            day_search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 0, 0, 0), "Australia/Sydney"
            ),
            expect_success=True,
            expected_day_record=DayRecord(
                wakeup_timestamp=arrow.get(
                    datetime(2022, 7, 2, 9, 30, 20), "Australia/Sydney"
                ),
                getup_timestamp=arrow.get(
                    datetime(2022, 7, 2, 9, 30, 20), "Australia/Sydney"
                ),
                bed_timestamp=arrow.get(
                    datetime(2022, 7, 3, 1, 20, 30), "Australia/Sydney"
                ),
                last_night_sleep_minutes=480,
                events=[],  # wakeup, getup, bed events should be excluded from day records
                time_intervals=july_2_intervals,
            ),
        )
    ]

    for i, case in enumerate(testcases):
        assert_message: str = f"case {i} failed, {case.description}"
        try:
            res = parse_and_generate_day_record(
                single_day_events=case.events,
                single_day_time_intervals=case.time_intervals,
            )
        except ValueError as exp:
            assert not case.expect_success, assert_message + f"exception: {exp}"
        except Exception as exp:
            print(assert_message + f"unexpected exception {exp}")
            raise
        else:
            assert case.expect_success, assert_message
            assert case.expected_day_record == res, assert_message


@pytest.mark.skip(reason="todo next")
def test_parse_and_generate_day_records() -> None:
    @dataclass
    class TestInput:
        start_date: str
        end_date: str
        events: list[Event]
        time_intervals: list[TimeInterval]

    @dataclass
    class TestCase:
        description: str
        input: TestInput
        expect_success: bool
        expected_day_records: Optional[list[DayRecord]] = None

    testcases: list[TestCase] = [
        TestCase(
            description="Invalid date format should raise",
            input=TestInput(
                start_date="2022.07.02",
                end_date="2022-07-03",
                events=[],
                time_intervals=[],
            ),
            expect_success=False,
        ),
        TestCase(
            description="Invalid date format should raise",
            input=TestInput(
                start_date="2022-07-0223",
                end_date="2022-07-03",
                events=[],
                time_intervals=[],
            ),
            expect_success=False,
        ),
        TestCase(
            description="Start date later than end date should raise",
            input=TestInput(
                start_date="2022-07-05",
                end_date="2022-07-03",
                events=[],
                time_intervals=[],
            ),
            expect_success=False,
        ),
        # unordered events should fail
        # unordered time_intervals should fail
        # no buffer events should fail
        # wakeup getup same or different, test cases
        TestCase(
            description="Single valid day record 07.02 should pass",
            input=TestInput(
                start_date="2022-07-02",
                end_date="2022-07-03",
                events=july_2_events_buffered,
                time_intervals=july_2_intervals,
            ),
            expect_success=True,
            expected_day_records=[
                DayRecord(
                    wakeup_timestamp=arrow.get(
                        datetime(2022, 7, 2, 9, 30, 20), "Australia/Sydney"
                    ),
                    getup_timestamp=arrow.get(
                        datetime(2022, 7, 2, 9, 30, 20), "Australia/Sydney"
                    ),
                    bed_timestamp=arrow.get(
                        datetime(2022, 7, 3, 1, 20, 30), "Australia/Sydney"
                    ),
                    last_night_sleep_minutes=480,
                    events=july_2_events_buffered[1:],
                    time_intervals=july_2_intervals,
                ),
            ],
        ),
    ]

    for i, case in enumerate(testcases):
        assert_message: str = f"case {i} failed, {case.description}"
        try:
            res = parse_and_generate_day_records(
                case.input.start_date,
                case.input.end_date,
                events=case.input.events,
                time_intervals=case.input.time_intervals,
            )
        except ValueError as exp:
            assert not case.expect_success, assert_message + f"exception: {exp}"
        except Exception as exp:
            print(assert_message + f"unexpected exception {exp}")
            raise
        else:
            assert case.expect_success, assert_message
            assert case.expected_day_records == res, assert_message
