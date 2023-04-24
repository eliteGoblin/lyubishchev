from dataclasses import dataclass

import arrow
from arrow import Arrow

from lyubishchev.data_model.core_data_structure import Metadata

# from typing import Any, List


@dataclass
class TimeInterval:
    """
    TimeInterval object is for tracking a time interval,
    with additional labels and annotations
    """

    metadata: Metadata
    extra_info: str
    timestamp: Arrow
    duration_minutes: int

    # define a class method, generate an empty TimeInterval object
    @classmethod
    def empty(cls) -> "TimeInterval":
        return cls(
            metadata=Metadata(),
            extra_info="",
            timestamp=arrow.now(),
            duration_minutes=0,
        )

    # def __init__(self, **kwargs: Any) -> None:
    #     self.metadata = Metadata()
    #     self.extra_info = ""
    #     self.timestamp = arrow.utcnow()
    #     self.duration_minutes = 0

    #     valid_keys: List[str] = [
    #         "metadata",
    #         "extra_info",
    #         "timestamp",
    #         "duration_minutes",
    #     ]
    #     for key in valid_keys:
    #         if kwargs.get(key) is not None:
    #             setattr(self, key, kwargs.get(key))
