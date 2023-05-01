import re
from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeAlias

from lyubishchev.data_model import Label, TimeInterval

# Create an alias for the function type
# label is dict[str, str]
TimeIntervalMatchFunction: TypeAlias = Callable[[Label], bool]


def must_tag(node_str: str) -> None:
    pattern = r"^[a-zA-Z0-9-_]+$"

    if not re.match(pattern, node_str):
        raise ValueError(f"Invalid format: '{node_str}' contains invalid characters")


def must_label_or_tag(node_str: str) -> None:
    """
    node key can be key=value(label) or key(tag)
    """
    pattern = r"^[a-zA-Z0-9-_]+$"

    # Split the input string on the '=' character
    parts = node_str.split("=")

    # Check if there are at most two parts (key and value)
    if len(parts) > 2:
        raise ValueError("Invalid format: more than one '=' character found")

    # Check if key and value are in the correct format
    for part in parts:
        if not re.match(pattern, part):
            raise ValueError(f"Invalid format: '{part}' contains invalid characters")


def must_match_tree(match_dict: dict[str, Any], depth: int = 0, path: str = "") -> None:
    """
    match_dict MUST follow:
    key is a string, (must be key=value format if it's label otherwise be valid tag);
    key and value MUST not contain whitespace
    value is a dict or None
    if it's a dict, it must follow the same rule
    Raise ValueError, specify where violate it , ideally visualize partial tree structure
    """
    for key, value in match_dict.items():
        current_path = f"{path}{'  ' * depth} {key}"

        # Check if key is in "key=value" format
        must_label_or_tag(key)
        # Check if value is a dictionary or None
        if value is not None and not isinstance(value, dict):
            raise ValueError(
                f"Invalid value at path '{current_path}'. Value must be a dictionary or None."
            )
        # Recursively check nested dictionaries
        if isinstance(value, dict):
            must_match_tree(value, depth=depth + 1, path=current_path)


def match_function_from_dict(match_dict: dict[str, Any]) -> TimeIntervalMatchFunction:
    """
    Create a match function from a dictionary, representing a tree
    {
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
    children on same level means "OR"
    children on a path till leaf node means "AND"
    Return True if at least on path to leaf node is found
    """
    must_match_tree(match_dict)

    def match_tree(
        label: Label, current_tree: Optional[dict[str, Optional[dict[str, Any]]]]
    ) -> bool:
        if current_tree is None:
            return False
        for key, value in label.items():
            kv_pair = f"{key}={value}" if value != "" else key
            if kv_pair in current_tree:
                if current_tree[kv_pair] is None:  # already leaf
                    return True
                if match_tree(label, current_tree[kv_pair]):
                    return True
        return False

    def match_function(label: Label) -> bool:
        return match_tree(label, match_dict)

    return match_function


@dataclass
class Match:
    """
    define condition when matching for TimeInterval
    """

    _match_func: Callable[[Label], bool] = lambda _: True

    @classmethod
    def from_function(cls, match_func: TimeIntervalMatchFunction) -> "Match":
        return cls(_match_func=match_func)

    @classmethod
    def from_dict(cls, match_dict: dict[str, Any]) -> "Match":
        return cls(_match_func=match_function_from_dict(match_dict))

    def match_label(self, label: Label) -> bool:
        match_func = self._match_func
        return match_func(label)

    def match(self, time_intervals: list[TimeInterval]) -> list[TimeInterval]:
        res = []
        match_func = self._match_func
        for time_interval in time_intervals:
            if match_func(time_interval.metadata.label):
                res.append(time_interval)
        return res
