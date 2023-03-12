from datetime import datetime
from typing import Optional

import arrow

from lyubishchev.data_model import Event, Metadata, TimeInterval


def july_2_events(
    insert_pos: Optional[int] = None, dup_index: Optional[int] = None
) -> list[Event]:
    """
    if no insert_pos, then no dup_index: return data will pass
    if insert_pos, then dup_index:
        original data: dup_index will be inserted in insert_pos, then return, to generate dup data will fail a test
    """
    correct_date: list[Event] = [
        Event(
            metadata=Metadata(
                label={
                    "type": "bed",
                }
            ),
            extra_info="bed",
            timestamp=arrow.get(datetime(2022, 7, 2, 1, 30, 20), "Australia/Sydney"),
        ),
        Event(
            metadata=Metadata(
                label={
                    "type": "wakeup",
                }
            ),
            extra_info="morning wakeup",
            timestamp=arrow.get(datetime(2022, 7, 2, 9, 30, 20), "Australia/Sydney"),
        ),
        Event(
            metadata=Metadata(
                label={
                    "type": "bed",
                }
            ),
            extra_info="bed, kindle",
            timestamp=arrow.get(datetime(2022, 7, 3, 1, 20, 30), "Australia/Sydney"),
        ),
    ]
    if insert_pos is None:
        return correct_date
    correct_date.insert(insert_pos, correct_date[dup_index])  # type: ignore # Optional[int] expected type SupportsIndex
    return correct_date


def july_2_intervals(
    insert_pos: Optional[int] = None, dup_index: Optional[int] = None
) -> list[TimeInterval]:
    """
    if no insert_pos, then no dup_index: return data will pass
    if insert_pos, then dup_index:
        original data: dup_index will be inserted in insert_pos, then return, to generate dup data will fail a test
    """
    correct_date: list[TimeInterval] = [
        TimeInterval(
            metadata=Metadata(
                label={
                    "type": "routine",
                }
            ),
            extra_info="morning wakeup",
            timestamp=arrow.get(datetime(2022, 7, 2, 9, 30, 20), "Australia/Sydney"),
            duration_minutes=480,
        ),
        TimeInterval(
            metadata=Metadata(
                label={
                    "type": "routine",
                }
            ),
            extra_info="routine",
            timestamp=arrow.get(datetime(2022, 7, 2, 17, 40, 25), "Australia/Sydney"),
            duration_minutes=400,
        ),
        TimeInterval(
            metadata=Metadata(
                label={
                    "type": "relax",
                    "reading": "",
                }
            ),
            extra_info="kindle",
            timestamp=arrow.get(datetime(2022, 7, 3, 0, 20, 25), "Australia/Sydney"),
            duration_minutes=60,
        ),
    ]
    if insert_pos is None:
        return correct_date
    correct_date.insert(insert_pos, correct_date[dup_index])  # type: ignore # Optional[int] expected type SupportsIndex
    return correct_date
