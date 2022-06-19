from dataclasses import dataclass
from typing import Any, Dict, List, Union

Annotation = Dict[str, Union[str, int, float]]
Label = Dict[str, str]


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
        valid_keys: List[str] = [
            "annotation",
            "label",
        ]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))
