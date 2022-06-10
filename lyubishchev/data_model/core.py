from dataclasses import dataclass
from typing import Dict, Union

Annotation = Dict[str, Union[str, int, float]]
Label = Dict[str, str]


class InvalidLabelTag(Exception):
    """Exception raised when missing required labels, invalid label or label and tag not matching the"""

    pass


@dataclass
class Metadata:
    version: str  # semver, e.g v0.1.0
    annotation: Annotation
    label: Label

    def __init__(self) -> None:
        self.version = ""
        self.annotation = {}
        self.label = {}

    def validate(self) -> None:
        """
        throw InvalidLabelTag
        """
        raise NotImplementedError("not implemented!")
