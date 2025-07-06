from dataclasses import dataclass

from lyubishchev.data_model import InvalidLabelTag, Label, validate_event_label_and_tag


def test_validate_event() -> None:
    @dataclass
    class TestCase:
        name: str
        input: Label
        expect_is_valid: bool

    testcases = [
        TestCase(
            name="empty dict missing required type should fail",
            input={},
            expect_is_valid=False,
        ),
        TestCase(
            name="with empty required type should fail",
            input={
                "event_type": "",
            },
            expect_is_valid=False,
        ),
        TestCase(
            name="with valid required type should pass",
            input={
                "event_type": "wakeup",
            },
            expect_is_valid=True,
        ),
        TestCase(
            name="with valid required type, valid tag should pass",
            input={
                "event_type": "wakeup",
            },
            expect_is_valid=True,
        ),
        TestCase(
            name="with valid required type, compatible tag should pass",
            input={
                "event_type": "unwell",
                "cold": "",
            },
            expect_is_valid=True,
        ),
        TestCase(
            name="with valid required type, compatible tag should fail",
            input={
                "event_type": "unwell",
                "cold": "",
            },
            expect_is_valid=True,
        ),
        TestCase(
            name="with valid required type, compatible tag should fail",
            input={
                "event_type": "recover_unwell",
                "cold": "",
            },
            expect_is_valid=True,
        ),
        TestCase(
            name="with valid required type, compatible tag should fail",
            input={
                "event_type": "wakeup",
                "cold": "",
            },
            expect_is_valid=False,
        ),
    ]

    for case in testcases:
        try:
            validate_event_label_and_tag(case.input)
        except InvalidLabelTag:
            assert not case.expect_is_valid
        else:
            assert case.expect_is_valid
