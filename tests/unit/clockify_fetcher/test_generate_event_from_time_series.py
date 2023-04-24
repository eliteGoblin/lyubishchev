import json
from dataclasses import dataclass
from functools import partial
from typing import Optional

import arrow

from lyubishchev.clockify_fetcher.fetcher import (
    generate_event_from_time_series,
)  # generate_event_from_time_series,
from lyubishchev.data_model import Event, Metadata

# import pytest


open_utf8 = partial(open, encoding="UTF-8")


def test_generate_event_from_time_series() -> None:
    @dataclass
    class TestCase:
        description: str
        test_data_path: str
        expect_success: bool
        expected_event: Optional[Event]

    testcases: list[TestCase] = [
        TestCase(
            description="empty dict should raise ValueError",
            test_data_path="empty.json",
            expect_success=False,
            expected_event=None,
        ),
        TestCase(
            description="meditation record should return None",
            test_data_path="time_series_meditation.json",
            expect_success=True,
            expected_event=None,
        ),
        TestCase(
            description="wakeup record should pass correctly",
            test_data_path="time_series_wakeup.json",
            expect_success=True,
            expected_event=Event(
                metadata=Metadata(
                    label={
                        "event_type": "wakeup",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get("2022-07-03T00:30:00Z").to("Australia/Sydney"),
            ),
        ),
        TestCase(
            description="bed record should pass correctly",
            test_data_path="time_series_bed.json",
            expect_success=True,
            expected_event=Event(
                metadata=Metadata(
                    label={
                        "event_type": "bed",
                    }
                ),
                extra_info="kindle",
                timestamp=arrow.get("2022-07-01T15:35:00Z").to("Australia/Sydney"),
            ),
        ),
        TestCase(
            description="dup event type: wakeup and bed record should pass fail",
            test_data_path="time_series_error_dup_event_type.json",
            expect_success=False,
            expected_event=None,
        ),
    ]
    test_data_folder: str = "./tests/unit/clockify_fetcher/test_data/"
    for case in testcases:
        with open_utf8(test_data_folder + case.test_data_path) as test_data:
            try:
                event: Optional[Event] = generate_event_from_time_series(
                    json.load(test_data)
                )
            except ValueError as exp:
                print(exp)
                assert not case.expect_success
            else:
                assert case.expect_success
                assert event == case.expected_event
