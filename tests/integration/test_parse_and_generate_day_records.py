import os

import arrow
import pytest

from lyubishchev.clockify_fetcher import ClockifyConfig, ClockifyFetcher
from lyubishchev.data_model import (
    DayRecord,
    Metadata,
    TimeInterval,
    date_range_to_timestamp_range,
    parse_and_generate_day_records,
)

# 2022-07-02 via WebUI: https://app.clockify.me/tracker?page=15&limit=200

config: ClockifyConfig = ClockifyConfig(
    host="api.clockify.me",
    workspace_id="5e86fab7183a8475e0c7a757",
    user_id="5e86fab6183a8475e0c7a755",
    api_key=os.getenv("CLOCKIFY_API_KEY", "fake_clockify_key"),
)


@pytest.mark.focus
def test_parse_and_generate_day_records_single_day() -> None:
    fetcher: ClockifyFetcher = ClockifyFetcher(config)
    time_intervals, events = fetcher.fetch_time_intervals_events(
        *date_range_to_timestamp_range(
            "2022-07-02", "2022-07-03"
        )  # get [7.2, 7.3), 1 day
    )
    day_records = parse_and_generate_day_records(
        start_date="2022-07-02",
        end_date="2022-07-03",
        time_intervals=time_intervals,
        events=events,
    )

    assert len(day_records) == 1
    assert day_records[0] == DayRecord(
        wakeup_timestamp=arrow.get("2022-07-02T09:15:00+10:00"),
        getup_timestamp=arrow.get("2022-07-02T09:15:00+10:00"),
        bed_timestamp=arrow.get("2022-07-03T04:00:00+10:00"),
        last_night_sleep_minutes=460,
        time_intervals=[
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "routine"}),
                extra_info="morning wakeup",
                timestamp=arrow.get("2022-07-02T09:15:00+10:00"),
                duration_minutes=210,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                extra_info="record",
                timestamp=arrow.get("2022-07-02T12:45:00+10:00"),
                duration_minutes=13,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "sleep"}),
                extra_info="nap",
                timestamp=arrow.get("2022-07-02T12:58:50+10:00"),
                duration_minutes=31,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "routine"}),
                extra_info="routine",
                timestamp=arrow.get("2022-07-02T13:30:00+10:00"),
                duration_minutes=90,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"social": "", "type": "relax"}),
                extra_info="chat Li",
                timestamp=arrow.get("2022-07-02T15:00:00+10:00"),
                duration_minutes=90,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "routine"}),
                extra_info="routine",
                timestamp=arrow.get("2022-07-02T16:30:00+10:00"),
                duration_minutes=105,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "sleep"}),
                extra_info="nap",
                timestamp=arrow.get("2022-07-02T18:15:00+10:00"),
                duration_minutes=45,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "routine"}),
                extra_info="routine, bath, recover",
                timestamp=arrow.get("2022-07-02T19:00:00+10:00"),
                duration_minutes=60,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                extra_info="record",
                timestamp=arrow.get("2022-07-02T20:00:00+10:00"),
                duration_minutes=17,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "meditation"}),
                extra_info="meditation",
                timestamp=arrow.get("2022-07-02T20:18:14+10:00"),
                duration_minutes=5,
            ),
            TimeInterval(
                metadata=Metadata(
                    annotation={},
                    label={"project": "software-engineering", "type": "self-improving"},
                ),
                extra_info="lyubishchev",
                timestamp=arrow.get("2022-07-02T20:23:39+10:00"),
                duration_minutes=5,
            ),
            TimeInterval(
                metadata=Metadata(
                    annotation={},
                    label={"project": "software-engineering", "type": "self-improving"},
                ),
                extra_info="lyubishchev",
                timestamp=arrow.get("2022-07-02T20:34:08+10:00"),
                duration_minutes=48,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "routine"}),
                extra_info="routine",
                timestamp=arrow.get("2022-07-02T21:22:00+10:00"),
                duration_minutes=218,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"type": "dispute"}),
                extra_info="dispute",
                timestamp=arrow.get("2022-07-03T01:00:00+10:00"),
                duration_minutes=30,
            ),
            TimeInterval(
                metadata=Metadata(annotation={}, label={"family": "", "type": "relax"}),
                extra_info="chat",
                timestamp=arrow.get("2022-07-03T01:30:00+10:00"),
                duration_minutes=120,
            ),
            TimeInterval(
                metadata=Metadata(
                    annotation={}, label={"reading": "", "type": "self-improving"}
                ),
                extra_info="kindle",
                timestamp=arrow.get("2022-07-03T03:30:00+10:00"),
                duration_minutes=30,
            ),
        ],
        events=[],
    )
