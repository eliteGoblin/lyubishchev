import json
from dataclasses import dataclass
from datetime import datetime
from functools import partial

import arrow

# import pytest
from arrow import Arrow

from lyubishchev.clockify_fetcher.fetcher import (  # generate_event_from_time_series,
    generate_time_interval_from_time_series,
    time_diff_minutes,
)
from lyubishchev.data_model import Metadata, TimeInterval

open_utf8 = partial(open, encoding="UTF-8")


def test_time_diff_minutes() -> None:
    timestamp_1: Arrow = arrow.get(datetime(2022, 7, 2, 18, 50, 20), "Australia/Sydney")
    timestamp_2: Arrow = arrow.get(datetime(2022, 7, 2, 18, 55, 10), "Australia/Sydney")
    timestamp_3: Arrow = arrow.get("2022-07-02T18:59:05.970460+10:00")

    assert time_diff_minutes(timestamp_1, timestamp_2) == 4
    assert time_diff_minutes(timestamp_2, timestamp_3) == 3


def test_generate_time_interval_from_time_series() -> None:
    @dataclass
    class TestCase:
        description: str
        test_data_path: str
        expect_success: bool
        expected_time_interval: TimeInterval

    testcases: list[TestCase] = [
        TestCase(
            description="empty dict should raise ValueError",
            test_data_path="empty.json",
            expect_success=False,
            expected_time_interval=TimeInterval(),
        ),
        TestCase(
            description="meditation record should pass correctly",
            test_data_path="time_series_meditation.json",
            expect_success=True,
            expected_time_interval=TimeInterval(
                metadata=Metadata(
                    label={
                        "type": "meditation",
                    }
                ),
                extra_info="meditation",
                timestamp=arrow.get("2022-07-03T07:11:13Z").to("Australia/Sydney"),
                duration_minutes=6,
            ),
        ),
        TestCase(
            description="wakeup record should pass correctly",
            test_data_path="time_series_wakeup.json",
            expect_success=True,
            expected_time_interval=TimeInterval(
                metadata=Metadata(
                    label={
                        "type": "pmo",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get("2022-07-03T00:30:00Z").to("Australia/Sydney"),
                duration_minutes=40,
            ),
        ),
        TestCase(
            description="bed record should pass correctly",
            test_data_path="time_series_bed.json",
            expect_success=True,
            expected_time_interval=TimeInterval(
                metadata=Metadata(
                    label={
                        "type": "self-improving",
                        "reading": "",
                    }
                ),
                extra_info="kindle",
                timestamp=arrow.get("2022-07-01T15:10:00Z").to("Australia/Sydney"),
                duration_minutes=25,
            ),
        ),
        TestCase(
            description="record with project should pass correctly",
            test_data_path="time_series_project.json",
            expect_success=True,
            expected_time_interval=TimeInterval(
                metadata=Metadata(
                    label={
                        "type": "self-improving",
                        "project": "software-engineering",
                    }
                ),
                extra_info="lyubishchev",
                timestamp=arrow.get("2022-07-02T10:23:39").to("Australia/Sydney"),
                duration_minutes=5,
            ),
        ),
        # time_series_error_dup_interval_type.json
        TestCase(
            description="record with duplicate interval type should fail",
            test_data_path="time_series_error_dup_interval_type.json",
            expect_success=False,
            expected_time_interval=TimeInterval(),
        ),
    ]
    test_data_folder: str = "./tests/unit/clockify_fetcher/test_data/"
    for case in testcases:
        with open_utf8(test_data_folder + case.test_data_path) as test_data:
            try:
                time_interval: TimeInterval = generate_time_interval_from_time_series(
                    json.load(test_data)
                )
            except ValueError as exp:
                print(exp)
                assert not case.expect_success
            else:
                assert case.expect_success
                assert time_interval == case.expected_time_interval
