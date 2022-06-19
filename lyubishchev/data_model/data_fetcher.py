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
        self, start_date: str, end_date: str
    ) -> tuple[List[TimeInterval], List[Event]]:
        """
        start_date, end_date : YYYY-MM-DD
        Fetch records between: [start's 00:00, end)
        """

    @abstractmethod
    def fetch_last_bedtime(self, timestamp: Arrow) -> Arrow:
        """
        Get when was the last bedtime before given timestamp within 24 hrs
        """
