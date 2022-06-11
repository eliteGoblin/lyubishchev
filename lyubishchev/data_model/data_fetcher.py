from abc import ABC, abstractmethod
from typing import List

from arrow import Arrow

from lyubishchev.data_model import TimeInterval


class TimeIntervalFetcher(ABC):  # pylint: disable=too-few-public-methods
    """
    throw: ?
    """

    @abstractmethod
    def fetch_time(self, start_date: Arrow, end_date: Arrow) -> List[TimeInterval]:
        """
        start_time: entry with wakeup, mark start of the day, Arrow must have timezone
            i.e must unambiguously specify an absolute timestamp
        """
