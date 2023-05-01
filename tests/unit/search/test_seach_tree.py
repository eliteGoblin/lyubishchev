from typing import Any

import arrow
import pytest

from lyubishchev.data_model import Label, Metadata, TimeInterval
from lyubishchev.search import Match, match_function_from_dict, must_match_tree


class TestMustMatchTree:
    @pytest.mark.parametrize(
        "match_dict",
        [
            # Valid trees
            ({"k1=v1": None}),
            ({"k1=v1": None, "k2=v2": {"k21=v21": None}}),
            ({"k1=v1": None, "k2=v2": {"k21=v21": {"k211=v211": None}}}),
            (
                {
                    "k1=v1": {"k11=v11": {"k111=v111": {"k1111=v1111": None}}},
                    "k2=v2": None,
                }
            ),
        ],
    )
    def test_valid_trees(self, match_dict: dict[str, Any]) -> None:
        try:
            must_match_tree(match_dict)
        except ValueError as value_error:
            pytest.fail(f"Unexpected error for valid tree: {value_error}")

    @pytest.mark.parametrize(
        "match_dict",
        [
            # valid tree with label and tag
            (
                {
                    "k1=v1": None,
                    "k2=v2": {"k21=v21": None},
                    "k3": None,
                    "k4": {"k41=v41": None},
                }
            ),
        ],
    )
    def test_valid_tree_label_tag(self, match_dict: dict[str, Any]) -> None:
        try:
            must_match_tree(match_dict)
        except ValueError as value_error:
            pytest.fail(f"Unexpected error for valid tree: {value_error}")

    @pytest.mark.parametrize(
        "match_dict",
        [
            # Invalid trees
            ({"k1 v1": None}),
            ({"k1=v1": "invalid_value"}),
            ({"k1=v1": {"k21 v21": None}}),
            (
                {
                    "k1=v1": {"k11=v11": {"k111=v111": {"k1111 v1111": None}}},
                    "k2=v2": None,
                }
            ),
        ],
    )
    def test_invalid_trees(self, match_dict: dict[str, Any]) -> None:
        with pytest.raises(ValueError):
            must_match_tree(match_dict)


class TestMatchFunctionFromDict:
    match_dict = {
        "k1=v1": None,
        "k2=v2": {
            "k21=v21": {
                "k211=v211": None,
                "k212=v212": None,
            },
        },
        "k3=v3": {
            "k31=v31": None,
        },
        "k4": None,
        "k5": {
            "k51": None,
            "k52": {
                "k521=v521": None,
            },
        },
    }

    @pytest.mark.parametrize(
        "label, expected",
        [
            ({"k1": "v1"}, True),
            ({"k2": "v2", "k21": "v21", "k211": "v211"}, True),
            ({"k3": "v3", "k31": "v31"}, True),
            ({"k4": "v4"}, False),
            ({"k1": "v2"}, False),
            ({"k3": "v3"}, False),
            ({"k2": "v2", "k21": "v21"}, False),
            ({"k5": ""}, False),
            ({"k5": "", "k51": ""}, True),
            ({"k5": "", "k52": "", "k521": "v521"}, True),
        ],
    )
    def test_match_function(self, label: Label, expected: bool) -> None:
        func = match_function_from_dict(self.match_dict)
        assert func(label) == expected, f"Unexpected result for label {label}"

    def test_dummy(self) -> None:
        pass


class TestMatchClass:
    match_dict = {
        "k1=v1": None,
        "k2=v2": {
            "k21=v21": {
                "k211=v211": None,
                "k212=v212": None,
            },
        },
        "k3=v3": {
            "k31=v31": None,
        },
    }
    fake_timestamp = arrow.now()

    @pytest.mark.parametrize(
        "label, expected",
        [
            ({"k1": "v1"}, True),
            ({"k2": "v2", "k21": "v21", "k211": "v211"}, True),
            ({"k3": "v3", "k31": "v31"}, True),
            ({"k4": "v4"}, False),
            ({"k1": "v2"}, False),
            ({"k3": "v3"}, False),
            ({"k2": "v2", "k21": "v21"}, False),
        ],
    )
    def test_match_class(self, label: Label, expected: bool) -> None:
        match = Match.from_dict(self.match_dict)
        assert (
            match.match_label(label) == expected
        ), f"Unexpected result for label {label}"

    @pytest.mark.parametrize(
        "time_intervals, expected_time_intervals",
        [
            (
                [
                    TimeInterval(
                        Metadata(annotation={}, label={"k1": "v1"}),
                        extra_info="Extra info 0",
                        timestamp=fake_timestamp,
                        duration_minutes=10,
                    )
                ],
                [
                    TimeInterval(
                        Metadata(annotation={}, label={"k1": "v1"}),
                        extra_info="Extra info 0",
                        timestamp=fake_timestamp,
                        duration_minutes=10,
                    )
                ],
            ),
        ],
    )
    def test_match_time_intervals(
        self,
        time_intervals: list[TimeInterval],
        expected_time_intervals: list[TimeInterval],
    ) -> None:
        match = Match.from_dict(self.match_dict)
        assert match.match(time_intervals) == expected_time_intervals
