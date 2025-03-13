from typing import Callable, Optional

from dataclasses import dataclass
from data_model import DayRecord

from pandas import DataFrame

DataFrameFunction = Callable[[list[int]], DataFrame]

@dataclass
class Habit:
    name: str
    cmap_min: Optional[float] = None
    cmap_max: Optional[float] = None
    habit_data_retriever: DataFrameFunction

    def get_habit_data(self, day_records: list[DayRecord]) -> DataFrame:
        """
        get_habit_data returns a DataFrame with the habit data for the given habit_name
        Return a DataFrame with the habit data for the given habit_name
        DataFrame has 2 columns: 'date'() and 'habit_name'(float)
        """
        pass


# NEXT:
# implement habit for exercise, sleep_early, getup_early
# generate heatmap for each habit
# make a copy of heatmap lib into code