from typing import Optional, Sequence, Union

from arrow import Arrow

from .core_data_structure import Label, TimeSeriesNotFound
from .event import Event
from .time_interval import TimeInterval


def find_first_match(
    sequence: Sequence[Union[Event, TimeInterval]],
    search_start_timestamp: Arrow,
    label: Optional[Label] = None,
    reverse: bool = False,
) -> int:
    """
    find_first_index search given list of objects, return first match;
        sequence usually buffer with 1 day (contain records both earlier and later by 1 day)
        No need to consider optimize for now, records for a month = 30 * 20 = 600
    Parameters:
        sequence: source records to be searched
        For Left to right search, requires
            reverse: False(default)
            search_start_timestamp: want first matching record >= start_timestamp
        For reverse order search, requires
            reverse: True
            search_start_timestamp: want first index matching record > than start_timestamp's - 1
        label: Optional
            None or empty means match any
            Otherwise return records also have key=value in Label
    Return:
        matching record's index
    Throws:
        TimeSeriesNotFound if no record found
    """
    if len(sequence) == 0:
        raise TimeSeriesNotFound(f"sequence is empty, while searching for {sequence}")

    start_index: int
    end_index: int
    step: int
    if not reverse:
        # If time-equal record non-exist, search in time order needs to start at first record > timestamp
        #   combine equal is: first record >= timestamp
        start_index = find_first_record_equal_or_later_than(
            sequence, search_start_timestamp
        )
        end_index = len(sequence)
        step = 1
    else:
        # If time-equal record non-exist, search in reverse order needs to start at last record < timestamp
        # combine equal is: last record <= timestamp
        start_index = reverse_find_first_record_equal_or_early_than(
            sequence, search_start_timestamp
        )
        end_index = -1
        step = -1

    if (
        label is None or len(label) == 0
    ):  # no label means no further condition, just return record match timestamp
        return start_index

    for index in range(start_index, end_index, step):
        if label.items() <= sequence[index].metadata.label.items():
            return index

    raise TimeSeriesNotFound(
        f"can't find time series matching timestamp {search_start_timestamp} "
        f"in {sequence}, reverse search: {reverse}"
    )


def find_first_record_equal_or_later_than(
    sequence: Sequence[Union[Event, TimeInterval]], timestamp: Arrow
) -> int:
    """
    raise RecordNotFound if no match
    """
    for index, record in enumerate(sequence):
        if record.timestamp >= timestamp:
            return index
    raise TimeSeriesNotFound(
        f"can't find record_equal_or_later_than {timestamp} in {sequence}"
    )


def reverse_find_first_record_equal_or_early_than(
    sequence: Sequence[Union[Event, TimeInterval]], timestamp: Arrow
) -> int:
    """
    raise RecordNotFound if no match
    """
    for index, record in reversed(list(enumerate(sequence))):
        if record.timestamp <= timestamp:
            return index
    raise TimeSeriesNotFound(
        f"can't reverse_find_first_record_equal_or_early_than {timestamp} in {sequence}"
    )
