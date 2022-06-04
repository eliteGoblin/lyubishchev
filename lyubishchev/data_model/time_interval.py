from dataclasses import dataclass

import arrow
from arrow import Arrow

from lyubishchev.data_model.core import Metadata


@dataclass
class TimeInterval:
    """TimeInterval object is for tracking a time interval, with additional labels and annotations"""

    metadata: Metadata
    extra_info: str
    timestamp: Arrow
    duration_minutes: int

    def __init__(self) -> None:
        self.metadata = Metadata()
        extra_info = ""
        timestamp = arrow.now()
        duration_minutes = 0
