from dataclasses import dataclass
from typing import Any, Union

Annotation = dict[str, Union[str, int, float]]
Label = dict[str, str]


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
