from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import arrow
import pytest
from arrow import Arrow

from lyubishchev import config
from lyubishchev.data_model import (
    Event,
    Label,
    Metadata,
    TimeSeriesNotFound,
    find_first_match,
    get_day_range_from_relative_days,
    get_events_for_single_day,
    must_events_cover_date_range,
    remove_wakeup_getup_bed_from_day_events,
    timestamp_from_date_str,
)


def test_must_events_cover_date_range() -> None:
    @dataclass
    class TestCase:
        description: str
        events: list[Event]
        start_date: str
        end_date: str
        expected_success: bool

    timezone_name: str = config.get_iana_timezone_name()
    testcases: List[TestCase] = [
        TestCase(
            description="empty events not cover range",
            events=[],
            start_date="2020-07-01",
            end_date="2020-07-02",
            expected_success=False,
        ),
        TestCase(
            description="events with buffer should cover",
            events=[
                Event(
                    timestamp=timestamp_from_date_str(
                        date_str="2020-07-01",
                        timezone_name=timezone_name,
                    ).shift(minutes=-1)
                ),
                Event(
                    timestamp=timestamp_from_date_str(
                        date_str="2020-07-02", timezone_name=timezone_name
                    )
                ),
            ],
            start_date="2020-07-01",
            end_date="2020-07-02",
            expected_success=True,
        ),
        TestCase(
            description="events exact match should succeed",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2020, 7, 1, 0, 0, 0), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2020, 7, 2, 0, 0, 0), "Australia/Sydney"
                    ),
                ),
            ],
            start_date="2020-07-01",
            end_date="2020-07-02",
            expected_success=True,
        ),
        TestCase(
            description="beginning events just cover end date should fail",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2020, 7, 1, 1, 0, 0), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2020, 7, 1, 23, 59, 59), "Australia/Sydney"
                    ),
                ),
            ],
            start_date="2020-07-01",
            end_date="2020-07-02",
            expected_success=True,
        ),
        TestCase(
            description="ending events be an early sleep should succeeded",
            events=[
                Event(
                    timestamp=timestamp_from_date_str(
                        date_str="2024-07-01",
                        timezone_name=timezone_name,
                    ).shift(minutes=-1)
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2024, 7, 2, 20, 30, 59), "Australia/Sydney"
                    ),
                ),
            ],
            start_date="2024-07-01",
            end_date="2024-07-03",
            expected_success=True,
        ),
        TestCase(
            description="ending events before (end date -1) 's late bound should fail",
            events=[
                Event(
                    timestamp=timestamp_from_date_str(
                        date_str="2024-07-01",
                        timezone_name=timezone_name,
                    ).shift(minutes=-1)
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2024, 7, 2, 17, 59, 59), "Australia/Sydney"
                    ),
                ),
            ],
            start_date="2024-07-01",
            end_date="2024-07-03",
            expected_success=False,
        ),
    ]

    for index, case in enumerate(testcases):
        assert_message: str = f"case {index} failed! "
        try:
            must_events_cover_date_range(
                case.events,
                case.start_date,
                case.end_date,
            )
        except ValueError:
            assert not case.expected_success, assert_message
        else:
            assert case.expected_success, assert_message


def test_find_first_match_event() -> None:
    @dataclass
    class TestCase:
        description: str
        events: list[Event]
        search_start_timestamp: Arrow
        label: Optional[Label] = None
        reverse: bool = False
        expected_find: bool = False
        expected_index: int = -1

    testcases: List[TestCase] = [
        TestCase(
            description="empty events return no result",
            events=[],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
            ),
            expected_find=False,
        ),
        # search without label(means match any)
        TestCase(
            description="should return first event match timestamp",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 51, 00), "Australia/Sydney"
                    ),
                ),
            ],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
            ),
            expected_find=True,
            expected_index=1,
        ),
        TestCase(
            description="return if timestamp is equal",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
                    ),
                ),
            ],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
            ),
            expected_find=True,
            expected_index=0,
        ),
        TestCase(
            description="reversed, should return first event match timestamp",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 51, 00), "Australia/Sydney"
                    ),
                ),
            ],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
            ),
            reverse=True,
            expected_find=True,
            expected_index=0,
        ),
        TestCase(
            description="quite early timestamp would match first event",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 51, 00), "Australia/Sydney"
                    ),
                ),
            ],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 1, 18, 52, 21), "Australia/Sydney"
            ),
            expected_find=True,
            expected_index=0,
        ),
        TestCase(
            description="reverse, quite late timestamp would match last event",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 51, 00), "Australia/Sydney"
                    ),
                ),
            ],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 15, 18, 52, 21), "Australia/Sydney"
            ),
            reverse=True,
            expected_find=True,
            expected_index=1,
        ),
        TestCase(
            description="reverse, quite early timestamp would NOT match",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 51, 00), "Australia/Sydney"
                    ),
                ),
            ],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 1, 18, 52, 21), "Australia/Sydney"
            ),
            reverse=True,
            expected_find=False,
        ),
        # search with label
        TestCase(
            description="should return first event match timestamp and label",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 51, 00), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "tag1": "",
                            "key1": "value1",
                        },
                    ),
                ),
            ],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
            ),
            expected_find=True,
            label={
                "tag1": "",
                "key1": "value1",
            },
            expected_index=1,
        ),
        TestCase(
            description="event match timestamp but not label should NotFound",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 51, 00), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "key1": "value1",
                        },
                    ),
                ),
            ],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
            ),
            expected_find=False,
            label={
                "tag1": "",
                "key1": "value1",
            },
        ),
        TestCase(
            description="reversed, event match timestamp both should found",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "key0": "value0",
                            "tag0": "",
                        },
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 51, 00), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "tag1": "",
                            "key1": "value1",
                        },
                    ),
                ),
            ],
            search_start_timestamp=arrow.get(
                datetime(2022, 7, 3, 18, 50, 21), "Australia/Sydney"
            ),
            expected_find=False,
            label={
                "tag0": "",
                "key0": "value0",
            },
        ),
    ]

    for index, case in enumerate(testcases):
        assert_message: str = f"case {index} failed! {case.description}"
        try:
            event_index: int = find_first_match(
                sequence=case.events,
                search_start_timestamp=case.search_start_timestamp,
                label=case.label,
                reverse=case.reverse,
            )
        except TimeSeriesNotFound:
            assert not case.expected_find, assert_message
        except Exception as exp:
            print(assert_message + f"unexpected exception: {exp}")
            raise
        else:
            assert case.expected_find, assert_message
            assert case.expected_index == event_index, assert_message


def test_remove_wakeup_getup_bed_from_day_events() -> None:
    @dataclass
    class TestCase:
        description: str
        events: list[Event]
        expected_events: list[Event]

    testcases: list[TestCase] = [
        TestCase(
            description="events not contain bed related events should return same",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 3, 18, 50, 21), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 4, 18, 50, 21), "Australia/Sydney"
                    ),
                ),
            ],
            expected_events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 3, 18, 50, 21), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 4, 18, 50, 21), "Australia/Sydney"
                    ),
                ),
            ],
        ),
        TestCase(
            description="events contain bed related events should strip",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 8, 0, 0), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "wakeup",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 8, 30, 0), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "getup",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 8, 31, 0), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 8, 32, 0), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 23, 32, 0), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "bed",
                        }
                    ),
                ),
            ],
            expected_events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 8, 31, 0), "Australia/Sydney"
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 8, 32, 0), "Australia/Sydney"
                    ),
                ),
            ],
        ),
    ]

    for index, case in enumerate(testcases):
        assert_message: str = f"case {index} failed! {case.description}"
        assert case.expected_events == remove_wakeup_getup_bed_from_day_events(
            day_events=case.events
        ), assert_message


def test_get_events_for_single_day_expect_fail() -> None:
    @dataclass
    class TestCase:
        description: str
        events: list[Event]

    testcases: list[TestCase] = [
        TestCase(
            description="no wakeup should raise exception",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "type": "bed",
                        }
                    ),
                ),
            ],
        ),
        TestCase(
            description="no bed should raise exception",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "type": "wakeup",
                        }
                    ),
                ),
            ],
        ),
        TestCase(
            description="no last night bed should raise exception",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "type": "wakeup",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 20, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "type": "bed",
                        }
                    ),
                ),
            ],
        ),
    ]

    for case in testcases:
        with pytest.raises(TimeSeriesNotFound):
            get_events_for_single_day(
                date_range_events=case.events,
                date="2022-07-02",
            )


def test_get_events_for_single_day() -> None:
    @dataclass
    class TestCase:
        description: str
        events: list[Event]
        expected_events: list[Event]

    testcases: list[TestCase] = [
        TestCase(
            description="wakeup and bed should return events",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 1, 20, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "bed",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "wakeup",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "bed",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 3, 3, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "wakeup",
                        }
                    ),
                ),
            ],
            expected_events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 1, 20, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "bed",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "wakeup",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "bed",
                        }
                    ),
                ),
            ],
        ),
        TestCase(
            description="wakeup, getup and bed should return events",
            events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 1, 20, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "bed",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "wakeup",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 4, 20, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "getup",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "bed",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 3, 3, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "wakeup",
                        }
                    ),
                ),
            ],
            expected_events=[
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 1, 20, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "bed",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 3, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "wakeup",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 4, 20, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "getup",
                        }
                    ),
                ),
                Event(
                    timestamp=arrow.get(
                        datetime(2022, 7, 2, 18, 50, 21), "Australia/Sydney"
                    ),
                    metadata=Metadata(
                        label={
                            "event_type": "bed",
                        }
                    ),
                ),
            ],
        ),
    ]

    for index, case in enumerate(testcases):
        assert_message: str = f"case {index} failed! {case.description}"
        res = get_events_for_single_day(
            date_range_events=case.events,
            date="2022-07-02",
        )
        assert res == case.expected_events, assert_message


def test_get_day_range_from_relative_days() -> None:
    @dataclass
    class TestCase:
        start_date: str
        days_delta: int
        expected_day_range: tuple[str, str]

    testcases: list[TestCase] = [
        TestCase(
            start_date="2021-01-01",
            days_delta=0,
            expected_day_range=("2021-01-01", "2021-01-01"),
        ),
        TestCase(
            start_date="2021-01-01",
            days_delta=1,
            expected_day_range=("2021-01-01", "2021-01-02"),
        ),
        TestCase(
            start_date="2021-01-01",
            days_delta=5,
            expected_day_range=("2021-01-01", "2021-01-06"),
        ),
        TestCase(
            start_date="2021-01-01",
            days_delta=-1,
            expected_day_range=("2020-12-31", "2021-01-01"),
        ),
        TestCase(
            start_date="2021-01-01",
            days_delta=-5,
            expected_day_range=("2020-12-27", "2021-01-01"),
        ),
    ]

    for i, testcase in enumerate(testcases):
        assert_message = f"case {i} failed!"
        res = get_day_range_from_relative_days(
            start_date=testcase.start_date, days_delta=testcase.days_delta
        )
        assert testcase.expected_day_range == res, assert_message
