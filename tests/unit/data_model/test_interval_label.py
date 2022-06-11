from dataclasses import dataclass

from lyubishchev.data_model import *  # pylint: disable=wildcard-import,unused-wildcard-import)


def test_validate_time_interval() -> None:
    @dataclass
    class TestCase:
        name: str
        input: Label
        expect_is_valid: bool

    testcases = [
        TestCase(
            name="empty dict missing required type is invalid",
            input={},
            expect_is_valid=False,
        ),
        TestCase(
            name="with type, with valid name",
            input={
                "type": "dispute",
            },
            expect_is_valid=True,
        ),
        TestCase(
            name="with type, with invalid name, should error",
            input={
                "type": "disputeX",
            },
            expect_is_valid=False,
        ),
        TestCase(
            name="with type, with valid name, type=relax, with valid tag",
            input={
                "type": "relax",
                "family": "",
                "happy": "",
            },
            expect_is_valid=True,
        ),
        TestCase(
            name="relax, invalid tag, should error",
            input={
                "type": "relax",
                "game": "",
            },
            expect_is_valid=False,
        ),
        TestCase(
            name="relax, with key not a tag, should error",
            input={
                "type": "relax",
                "intimacy": "true",
            },
            expect_is_valid=False,
        ),
    ]

    for case in testcases:
        try:
            validate_time_interval_label_and_tag(case.input)
        except InvalidLabelTag:
            assert not case.expect_is_valid
        else:
            assert case.expect_is_valid
