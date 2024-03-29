import arrow

from lyubishchev.clockify_fetcher import ClockifyConfig, ClockifyFetcher
from lyubishchev.data_model import Event, Metadata, date_range_to_timestamp_range

# import pytest
# from icecream import ic


# 2022-07-02 via WebUI: https://app.clockify.me/tracker?page=15&limit=200


def test_fetch_time_intervals_events_single_day() -> None:
    config: ClockifyConfig = ClockifyConfig()
    fetcher: ClockifyFetcher = ClockifyFetcher(config)
    time_intervals, events = fetcher.fetch_time_intervals_events(
        *date_range_to_timestamp_range(
            "2022-07-02", "2022-07-03"
        )  # get [7.2, 7.3), 1 day
    )
    assert events == [
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "bed"}),
            extra_info="kindle",
            timestamp=arrow.get("2022-07-02T01:35:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "wakeup"}),
            extra_info="morning wakeup",
            timestamp=arrow.get("2022-07-02T09:15:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "bed"}),
            extra_info="kindle",
            timestamp=arrow.get("2022-07-03T04:00:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "wakeup"}),
            extra_info="morning wakeup",
            timestamp=arrow.get("2022-07-03T10:30:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "getup"}),
            extra_info="routine",
            timestamp=arrow.get("2022-07-03T11:10:00+10:00"),
        ),
    ]
    assert len(time_intervals) == 30


def test_fetch_raw_time_series_3_days() -> None:
    config: ClockifyConfig = ClockifyConfig()
    fetcher: ClockifyFetcher = ClockifyFetcher(config)
    time_intervals, events = fetcher.fetch_time_intervals_events(
        *date_range_to_timestamp_range(
            "2022-07-02", "2022-07-05"
        )  # get [7.2, 7.5), 3 day
    )
    assert events == [
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "bed"}),
            extra_info="kindle",
            timestamp=arrow.get("2022-07-02T01:35:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "wakeup"}),
            extra_info="morning wakeup",
            timestamp=arrow.get("2022-07-02T09:15:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "bed"}),
            extra_info="kindle",
            timestamp=arrow.get("2022-07-03T04:00:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "wakeup"}),
            extra_info="morning wakeup",
            timestamp=arrow.get("2022-07-03T10:30:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "getup"}),
            extra_info="routine",
            timestamp=arrow.get("2022-07-03T11:10:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "bed"}),
            extra_info="routine",
            timestamp=arrow.get("2022-07-04T02:40:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "wakeup"}),
            extra_info="morning wakeup",
            timestamp=arrow.get("2022-07-04T09:00:00+10:00"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "bed"}),
            extra_info="routine",
            timestamp=arrow.get("2022-07-05T00:20:00+10:00]"),
        ),
        Event(
            metadata=Metadata(annotation={}, label={"event_type": "wakeup"}),
            extra_info="morning wakeup",
            timestamp=arrow.get("2022-07-05T09:15:00+10:00"),
        ),
    ]
    assert len(time_intervals) == 75
