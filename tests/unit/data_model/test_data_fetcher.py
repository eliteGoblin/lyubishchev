from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import arrow
from arrow import Arrow

from lyubishchev.data_model import date_range_to_timestamp_range


def test_date_range_to_timestamp_range() -> None:
    @dataclass
    class TestCase:
        description: str
        input_date_str_range: tuple[str, str]
        expect_success: bool
        expected_timestamp_range: Optional[tuple[Arrow, Arrow]]

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
    ]

    for case in testcases:
        try:
            res = date_range_to_timestamp_range(
                case.input_date_str_range[0],
                case.input_date_str_range[1],
            )
        except ValueError as exp:
            print(exp)
            assert not case.expect_success
        else:
            assert case.expect_success
            assert case.expected_timestamp_range == res
