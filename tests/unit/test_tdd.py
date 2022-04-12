from dataclasses import dataclass
from typing import List

my_sort = sorted


def test_my_sort() -> None:
    @dataclass
    class TestCase:
        name: str
        input: List[float]
        expected: List[float]

    testcases = [
        TestCase(name="empty_slice", input=[], expected=[]),
        TestCase(name="already_sorted", input=[1, 4, 6, 8], expected=[1, 4, 6, 8]),
        TestCase(name="not_sorted", input=[1, 8, 3, 5], expected=[1, 3, 5, 8]),
    ]

    for case in testcases:
        actual = my_sort(case.input)
        assert case.expected == actual
