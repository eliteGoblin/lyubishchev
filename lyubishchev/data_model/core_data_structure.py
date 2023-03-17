from dataclasses import dataclass
from typing import Any, Union

Annotation = dict[str, Union[str, int, float]]
Label = dict[str, str]


def is_label_match(label: Label, search_label: Label) -> bool:
    return all(key_value in label.items() for key_value in search_label.items())


class InvalidLabelTag(Exception):
    """
    Exception raised when missing required labels,
    invalid label or label and tag not matching the
    """


@dataclass
class Metadata:
    annotation: Annotation
    label: Label

    def __init__(self, **kwargs: Any) -> None:
        self.annotation = {}
        self.label = {}

        valid_keys: list[str] = [
            "annotation",
            "label",
        ]
        for key in valid_keys:
            if kwargs.get(key) is not None:
                setattr(self, key, kwargs.get(key))


class TimeSeriesNotFound(Exception):
    """
    Exception raised indicating can't find record matching criteria
    """
