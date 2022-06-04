from dataclasses import dataclass
from typing import Dict, Union

Annotation = Dict[str, Union[str, int, float]]
Label = Dict[str, str]

# TimeInterval

TYPE = "type"
# Valid type values
DISPUTE = "dispute"
DISTRACTED = "distracted"
EXERCISE = "exercise"
MEDITATION = "meditation"
PMO = "pmo"
RELAX = "relax"
ROUTINE = "routine"
SELF_IMPROVING = "self-improving"
SEX = "sex"
SLEEP = "sleep"
WORK = "work"

PROJECT = "project"


@dataclass
class Metadata:
    version: str  # semver, e.g v0.1.0
    annotations: Annotation
    labels: Label

    def __init__(self) -> None:
        self.version = ""
        self.annotations = {}
        self.labels = {}
