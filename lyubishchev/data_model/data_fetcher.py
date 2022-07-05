from abc import ABC, abstractmethod
from typing import List

from arrow import Arrow

from lyubishchev.data_model.event import Event
from lyubishchev.data_model.time_interval import TimeInterval


class TimeIntervalFetcher(ABC):  # pylint: disable=too-few-public-methods
    """
    throw: ValueError, Exception
    """

    @abstractmethod
    def fetch_time_intervals_events(
        self, start_timestamp: Arrow, end_timestamp: Arrow
    ) -> tuple[List[TimeInterval], List[Event]]:
        """
        Fetch records exactly between: [start_timestamp, end_timestamp]
        """
