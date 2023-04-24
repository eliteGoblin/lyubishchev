from datetime import datetime

import arrow

from lyubishchev.data_model import Event, Metadata, TimeInterval


def july_2_3_4_events() -> dict[str, list[Event]]:

    res: dict[str, list[Event]] = {
        "2022-07-02": [
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "bed",
                    }
                ),
                extra_info="bed",
                timestamp=arrow.get(
                    datetime(2022, 7, 1, 20, 30, 20), "Australia/Sydney"
                ),
            ),
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "wakeup",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get(
                    datetime(2022, 7, 2, 4, 30, 20), "Australia/Sydney"
                ),
            ),
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "getup",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get(
                    datetime(2022, 7, 2, 4, 50, 20), "Australia/Sydney"
                ),
            ),
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "bed",
                    }
                ),
                extra_info="bed, kindle",
                timestamp=arrow.get(
                    datetime(2022, 7, 2, 20, 50, 30), "Australia/Sydney"
                ),
            ),
        ],
        "2022-07-03": [
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "wakeup",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get(
                    datetime(2022, 7, 3, 4, 00, 20), "Australia/Sydney"
                ),
            ),
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "getup",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get(
                    datetime(2022, 7, 3, 4, 15, 20), "Australia/Sydney"
                ),
            ),
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "bed",
                    }
                ),
                extra_info="bed, kindle",
                timestamp=arrow.get(
                    datetime(2022, 7, 3, 22, 00, 30), "Australia/Sydney"
                ),
            ),
        ],
        "2022-07-04": [
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "wakeup",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get(
                    datetime(2022, 7, 4, 3, 40, 20), "Australia/Sydney"
                ),
            ),
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "getup",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get(datetime(2022, 7, 4, 4, 0, 20), "Australia/Sydney"),
            ),
            Event(
                metadata=Metadata(
                    label={
                        "event_type": "bed",
                    }
                ),
                extra_info="bed, kindle",
                timestamp=arrow.get(
                    datetime(2022, 7, 5, 00, 30, 30), "Australia/Sydney"
                ),
            ),
        ],
    }
    return res


def july_2_3_4_intervals() -> dict[str, list[TimeInterval]]:

    res: dict[str, list[TimeInterval]] = {
        "2022-07-02": [
            TimeInterval(
                metadata=Metadata(
                    label={
                        "self_routine": "",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get(
                    datetime(2022, 7, 2, 4, 30, 20), "Australia/Sydney"
                ),
                duration_minutes=480,
            ),
            TimeInterval(
                metadata=Metadata(
                    label={
                        "self_routine": "",
                    }
                ),
                extra_info="routine",
                timestamp=arrow.get(
                    datetime(2022, 7, 2, 17, 40, 25), "Australia/Sydney"
                ),
                duration_minutes=180,
            ),
        ],
        "2022-07-03": [
            TimeInterval(
                metadata=Metadata(
                    label={
                        "self_routine": "",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get(
                    datetime(2022, 7, 3, 4, 20, 20), "Australia/Sydney"
                ),
                duration_minutes=700,
            ),
            TimeInterval(
                metadata=Metadata(
                    label={
                        "relax": "",
                        "reading": "",
                    }
                ),
                extra_info="kindle",
                timestamp=arrow.get(
                    datetime(2022, 7, 3, 16, 20, 25), "Australia/Sydney"
                ),
                duration_minutes=80,
            ),
            TimeInterval(
                metadata=Metadata(
                    label={
                        "relax": "",
                        "reading": "",
                    }
                ),
                extra_info="bondi have fun",
                timestamp=arrow.get(
                    datetime(2022, 7, 3, 18, 00, 25), "Australia/Sydney"
                ),
                duration_minutes=200,
            ),
        ],
        "2022-07-04": [
            TimeInterval(
                metadata=Metadata(
                    label={
                        "self_routine": "",
                    }
                ),
                extra_info="morning wakeup",
                timestamp=arrow.get(
                    datetime(2022, 7, 4, 4, 20, 20), "Australia/Sydney"
                ),
                duration_minutes=900,
            ),
        ],
    }

    return res
