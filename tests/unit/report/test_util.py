import copy
from typing import Any

import pytest

from lyubishchev.report.report_utils import prune_dict


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "key1": {
                    "key11": 11,
                    "key12": 0,
                },
                "key2": {},
            },
            {
                "key1": {
                    "key11": 11,
                }
            },
        ),
        (
            {
                "key1": {
                    "key11": 0,
                    "key12": 0,
                },
                "key2": {},
            },
            {},
        ),
        (
            {
                "key1": {
                    "key11": 12,
                    "key12": 23,
                },
                "key2": {"key21": 0, "key22": 32},
            },
            {
                "key1": {
                    "key11": 12,
                    "key12": 23,
                },
                "key2": {"key22": 32},
            },
        ),
        (
            {
                "key1": {
                    "key11": {
                        "key111": {
                            "key1111": 0,
                        }
                    }
                }
            },
            {},
        ),
        ({}, {}),
    ],
)
def test_prune_dict(test_input: dict[str, Any], expected: dict[str, Any]) -> None:
    clone_input = copy.deepcopy(test_input)
    prune_dict(test_input)
    assert (
        test_input == expected
    ), f"input is {clone_input}, output {test_input} != expected {expected}"
