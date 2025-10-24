from typing import Protocol

import pandas  # pylint: disable=unused-import


class Habit(Protocol):
    """
    Habit protocol defines the interface for habit data extractors.
    Implementations must provide a data() method returning a pandas Series.
    """

    def data(self) -> "pandas.Series[int]":
        ...
