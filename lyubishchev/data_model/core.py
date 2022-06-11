from dataclasses import dataclass
from typing import Dict, Union

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

    def __init__(self) -> None:
        self.annotation = {}
        self.label = {}
