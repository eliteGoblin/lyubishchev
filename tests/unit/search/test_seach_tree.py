from lyubishchev.data_model import Label, TimeInterval, Metadata
from lyubishchev.search import must_match_tree, match_function_from_dict, Match

import pytest
from typing import Any
import arrow
from icecream import ic

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
                    "k1=v1": {
                        "k11=v11": {
                            "k111=v111": {
                                "k1111=v1111": None
                            }
                        }
                    },
                    "k2=v2": None
                }
            ),
        ],
    )
    def test_valid_trees(self, match_dict: dict[str, Any]):
        try:
            must_match_tree(match_dict)
        except ValueError as e:
            pytest.fail(f"Unexpected error for valid tree: {e}")

    @pytest.mark.parametrize(
        "match_dict",
        [
            # Invalid trees
            ({"k1 v1": None}),
            ({"k1=v1": "invalid_value"}),
            ({"k1=v1": {"k21 v21": None}}),
            (
                {
                    "k1=v1": {
                        "k11=v11": {
                            "k111=v111": {
                                "k1111 v1111": None
                            }
                        }
                    },
                    "k2=v2": None
                }
            )
        ],
    )
    def test_invalid_trees(self, match_dict: dict[str, Any]):
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
        }
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
        ],
    )
    def test_match_function(self, label: Label, expected: bool):
        func = match_function_from_dict(self.match_dict)
        assert func(label) == expected, f"Unexpected result for label {label}"

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
        }
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
    def test_match_class(self, label: Label, expected: bool):
        match = Match.from_dict(self.match_dict)
        assert match.match_label(label) == expected, f"Unexpected result for label {label}"

    @pytest.mark.parametrize(
        "time_intervals, expected_time_intervals",
        [
            (
                [
                    TimeInterval(
                        Metadata(
                            annotation={},
                            label={'k1': 'v1'}
                        ),
                        extra_info="Extra info 0",
                        timestamp=fake_timestamp,
                        duration_minutes=10
                    )
                ],
                [
                    TimeInterval(
                        Metadata(
                            annotation={},
                            label={'k1': 'v1'}
                        ),
                        extra_info="Extra info 0",
                        timestamp=fake_timestamp,
                        duration_minutes=10
                    )
                ],
            ),
            # (
            #     [
            #         TimeInterval(
            #             Metadata(
            #                 annotation={},
            #                 label={'category': 'Category 1'}
            #             ),
            #             extra_info="Extra info 1",
            #             timestamp=arrow.now().shift(minutes=1),
            #             duration_minutes=20
            #         ),
            #         TimeInterval(
            #             Metadata(
            #                 annotation={},
            #                 label={'category': 'Category 2'}
            #             ),
            #             extra_info="Extra info 2",
            #             timestamp=arrow.now().shift(minutes=2),
            #             duration_minutes=30
            #         )
            #     ],
            #     True
            # ),
        ]
    )
    def test_match_time_intervals(self, time_intervals: list[TimeInterval], expected_time_intervals: list[TimeInterval]):
        match = Match.from_dict(self.match_dict)
        assert match.match(time_intervals) == expected_time_intervals