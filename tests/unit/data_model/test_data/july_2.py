from datetime import datetime

import arrow

from lyubishchev.data_model import Event, Metadata, TimeInterval

july_2_events_buffered: list[Event] = [
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
july_2_intervals: list[TimeInterval] = [
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
