import arrow
import pytest

from lyubishchev.data_model.core_data_structure import Metadata
from lyubishchev.data_model.day import DayRecord
from lyubishchev.data_model.event import Event
from lyubishchev.data_model.time_interval import TimeInterval
from lyubishchev.report.report import DayRangeReport


@pytest.fixture
def sample_dayrangereport() -> DayRangeReport:
    # 5 days, each with different intervals and events
    base = arrow.get("2024-01-01T07:00:00+00:00")
    day_records = []
    for i in range(5):
        day = base.shift(days=i)
        # TimeIntervals: one with label "work", one with label "exercise"
        intervals = [
            TimeInterval(
                metadata=Metadata(label={"work": ""}),
                extra_info="",
                timestamp=day.replace(hour=9),
                duration_minutes=60 + i * 10,
            ),
            TimeInterval(
                metadata=Metadata(label={"exercise": ""}),
                extra_info="",
                timestamp=day.replace(hour=18),
                duration_minutes=30,
            ),
        ]
        # Events: one with label "unwell" on day 2 and 4
        events = []
        if i in (1, 3):
            events.append(
                Event(
                    metadata=Metadata(label={"unwell": ""}),
                    extra_info="",
                    timestamp=day.replace(hour=12),
                )
            )
        # getup at 7:00, target is 7:00
        day_record = DayRecord(
            timezone_name="UTC",
            wakeup_timestamp=day.replace(hour=6),
            getup_timestamp=day.replace(hour=7),
            bed_timestamp=day.replace(hour=23),
            last_night_sleep_minutes=420,
            time_intervals=intervals,
            events=events,
        )
        day_records.append(day_record)
    return DayRangeReport(day_records)
