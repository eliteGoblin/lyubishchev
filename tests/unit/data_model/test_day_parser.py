import itertools
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

from .test_data.july_2 import july_2_events, july_2_intervals
from .test_data.july_2_3_4 import july_2_3_4_events, july_2_3_4_intervals


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


def test_parse_and_generate_day_record_expect_fail() -> None:
    @dataclass
    class TestCase:
        description: str
        events: list[Event]
        time_intervals: list[TimeInterval]
        day_search_start_timestamp: Arrow

    testcases: list[TestCase] = [
        TestCase(
            description="empty events expect fail",
            events=[],
            time_intervals=july_2_intervals(),
            day_search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 0, 0, 0), "Australia/Sydney"
            ),
        ),
        TestCase(
            description="no previous day's bed event expect fail",
            events=july_2_events()[1:],
            time_intervals=july_2_intervals(),
            day_search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 0, 0, 0), "Australia/Sydney"
            ),
        ),
        TestCase(
            description="no last day's bed event expect fail",
            events=july_2_events()[:-1],
            time_intervals=july_2_intervals(),
            day_search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 0, 0, 0), "Australia/Sydney"
            ),
        ),
        TestCase(
            description="2 previous bed in a row should fail",
            events=july_2_events(1, 0),
            time_intervals=july_2_intervals(),
            day_search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 0, 0, 0), "Australia/Sydney"
            ),
        ),
        TestCase(
            description="dup wakeup should fail",
            events=july_2_events(1, 1),
            time_intervals=july_2_intervals(),
            day_search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 0, 0, 0), "Australia/Sydney"
            ),
        ),
    ]

    for case in testcases:
        with pytest.raises(ValueError):
            parse_and_generate_day_record(
                single_day_events=case.events,
                single_day_time_intervals=case.time_intervals,
            )


def test_parse_and_generate_day_record() -> None:
    @dataclass
    class TestCase:
        description: str
        events: list[Event]
        time_intervals: list[TimeInterval]
        day_search_start_timestamp: Arrow
        expected_day_record: DayRecord

    testcases: list[TestCase] = [
        TestCase(
            description="",
            events=july_2_events(),
            time_intervals=july_2_intervals(),
            day_search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 0, 0, 0), "Australia/Sydney"
            ),
            expected_day_record=DayRecord(
                wakeup_timestamp=arrow.get(
                    datetime(2022, 7, 2, 9, 30, 20), "Australia/Sydney"
                ),
                getup_timestamp=arrow.get(
                    datetime(2022, 7, 2, 9, 50, 20), "Australia/Sydney"
                ),
                bed_timestamp=arrow.get(
                    datetime(2022, 7, 3, 1, 20, 30), "Australia/Sydney"
                ),
                last_night_sleep_minutes=480,
                events=[],  # wakeup, getup, bed events should be excluded from day records
                time_intervals=july_2_intervals(),
            ),
        )
    ]

    for i, case in enumerate(testcases):
        assert_message: str = f"case {i} failed, {case.description}"
        res = parse_and_generate_day_record(
            single_day_events=case.events,
            single_day_time_intervals=case.time_intervals,
        )
        assert case.expected_day_record == res, assert_message


def test_parse_and_generate_day_records_expect_fail() -> None:
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

    testcases: list[TestCase] = [
        TestCase(
            description="Invalid date format should raise",
            input=TestInput(
                start_date="2022.07.02",
                end_date="2022-07-03",
                events=[],
                time_intervals=[],
            ),
        ),
        TestCase(
            description="Invalid date format should raise",
            input=TestInput(
                start_date="2022-07-0223",
                end_date="2022-07-03",
                events=[],
                time_intervals=[],
            ),
        ),
        TestCase(
            description="Start date later than end date should raise",
            input=TestInput(
                start_date="2022-07-05",
                end_date="2022-07-03",
                events=[],
                time_intervals=[],
            ),
        ),
        # unordered events should fail
        # unordered time_intervals should fail
        # no buffer events should fail
    ]

    for case in testcases:
        with pytest.raises(Exception):
            parse_and_generate_day_records(
                case.input.start_date,
                case.input.end_date,
                events=case.input.events,
                time_intervals=case.input.time_intervals,
            )


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
        expected_day_records: list[DayRecord]

    testcases: list[TestCase] = [
        TestCase(
            description="Single valid day record 07.02 should pass",
            input=TestInput(
                start_date="2022-07-02",
                end_date="2022-07-03",
                events=july_2_events(),
                time_intervals=july_2_intervals(),
            ),
            expected_day_records=[
                DayRecord(
                    wakeup_timestamp=arrow.get(
                        datetime(2022, 7, 2, 9, 30, 20), "Australia/Sydney"
                    ),
                    getup_timestamp=arrow.get(
                        datetime(2022, 7, 2, 9, 50, 20), "Australia/Sydney"
                    ),
                    bed_timestamp=arrow.get(
                        datetime(2022, 7, 3, 1, 20, 30), "Australia/Sydney"
                    ),
                    last_night_sleep_minutes=480,
                    events=[],
                    time_intervals=july_2_intervals(),
                ),
            ],
        ),
        TestCase(
            description="07.02 and 07.03 07.04 should pass",
            input=TestInput(
                start_date="2022-07-02",
                end_date="2022-07-05",
                events=list(
                    itertools.chain.from_iterable(july_2_3_4_events().values())
                ),
                time_intervals=list(
                    itertools.chain.from_iterable(july_2_3_4_intervals().values())
                ),
            ),
            expected_day_records=[
                DayRecord(
                    wakeup_timestamp=arrow.get(
                        datetime(2022, 7, 2, 4, 30, 20), "Australia/Sydney"
                    ),
                    getup_timestamp=arrow.get(
                        datetime(2022, 7, 2, 4, 50, 20), "Australia/Sydney"
                    ),
                    bed_timestamp=arrow.get(
                        datetime(2022, 7, 2, 20, 50, 30), "Australia/Sydney"
                    ),
                    last_night_sleep_minutes=480,
                    events=[],
                    time_intervals=july_2_3_4_intervals()["2022-07-02"],
                ),
                DayRecord(
                    wakeup_timestamp=arrow.get(
                        datetime(2022, 7, 3, 4, 00, 20), "Australia/Sydney"
                    ),
                    getup_timestamp=arrow.get(
                        datetime(2022, 7, 3, 4, 15, 20), "Australia/Sydney"
                    ),
                    bed_timestamp=arrow.get(
                        datetime(2022, 7, 3, 22, 00, 30), "Australia/Sydney"
                    ),
                    last_night_sleep_minutes=429,
                    events=[],
                    time_intervals=july_2_3_4_intervals()["2022-07-03"],
                ),
                DayRecord(
                    wakeup_timestamp=arrow.get(
                        datetime(2022, 7, 4, 3, 40, 20), "Australia/Sydney"
                    ),
                    getup_timestamp=arrow.get(
                        datetime(2022, 7, 4, 4, 0, 20), "Australia/Sydney"
                    ),
                    bed_timestamp=arrow.get(
                        datetime(2022, 7, 5, 00, 30, 30), "Australia/Sydney"
                    ),
                    last_night_sleep_minutes=339,
                    events=[],
                    time_intervals=july_2_3_4_intervals()["2022-07-04"],
                ),
            ],
        ),
    ]

    for i, case in enumerate(testcases):
        assert_message: str = f"case {i} failed, {case.description}"
        res = parse_and_generate_day_records(
            start_date=case.input.start_date,
            end_date=case.input.end_date,
            events=case.input.events,
            time_intervals=case.input.time_intervals,
        )
        assert case.expected_day_records == res, assert_message
