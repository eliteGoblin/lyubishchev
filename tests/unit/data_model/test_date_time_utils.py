import pytest

from lyubishchev.data_model import get_day_range_from_relative_weeks


# Test function for relative_week
@pytest.mark.parametrize(
    "description,start_date,week_offset,expected_start,expected_end",
    [
        (
            "Test Case 1: If given date is 2023-06-07 (a Wednesday)",
            "2023-06-07",
            0,
            "2023-06-04",
            "2023-06-07",
        ),
        (
            "current week, should return from Sunday to next Sunday",
            "2023-06-07",
            -1,
            "2023-05-28",
            "2023-06-04",
        ),
        (
            "Test Case 2: If given date is 2023-06-04 (a Sunday)",
            "2023-06-04",
            0,
            "2023-06-04",
            "2023-06-04",
        ),
        (
            "current week, should return from Sunday to next Sunday",
            "2023-06-04",
            -1,
            "2023-05-28",
            "2023-06-04",
        ),
        (
            "last 2 weeks",
            "2023-06-04",
            -2,
            "2023-05-21",
            "2023-05-28",
        ),
    ],
)
def test_relative_week(
    description: str,
    start_date: str,
    week_offset: int,
    expected_start: str,
    expected_end: str,
) -> None:
    result_start, result_end = get_day_range_from_relative_weeks(
        start_date, week_offset
    )
    assert expected_start == result_start, description
    assert expected_end == result_end, description
