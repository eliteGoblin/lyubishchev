from abc import ABC, abstractmethod
from typing import List

from arrow import Arrow

from lyubishchev.data_model import Event, TimeInterval


class TimeIntervalFetcher(ABC):  # pylint: disable=too-few-public-methods
    """
    throw: ?
    """

    @abstractmethod
    def fetch_time_intervals_events(
        self, start_timestamp: Arrow, end_timestamp: Arrow
    ) -> tuple[List[TimeInterval], List[Event]]:
        """
        Fetch records between: [start_timestamp, end_timestamp]
        """

    @abstractmethod
    def fetch_last_bedtime(self, timestamp: Arrow) -> Arrow:
        """
        Get when was the last bedtime
        """
