import arrow

from lyubishchev.data_model import DayRecord, Metadata, TimeInterval


def day_records_2023_march_12_14() -> list[DayRecord]:
    return [
        DayRecord(
            timezone_name="Australia/Sydney",
            day_str="2023-03-12",
            wakeup_timestamp=arrow.get("2023-03-12T08:00:00+11:00"),
            getup_timestamp=arrow.get("2023-03-12T08:00:00+11:00"),
            bed_timestamp=arrow.get("2023-03-12T21:30:00+11:00"),
            last_night_sleep_minutes=570,
            time_intervals=[
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="morning wakeup",
                    timestamp=arrow.get("2023-03-12T08:00:00+11:00"),
                    duration_minutes=34,
                ),
                TimeInterval(
                    metadata=Metadata(
                        annotation={}, label={"oj": ""}
                    ),
                    extra_info="oj",
                    timestamp=arrow.get("2023-03-12T08:34:26+11:00"),
                    duration_minutes=54,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-12T09:29:24+11:00"),
                    duration_minutes=100,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-12T11:09:48+11:00"),
                    duration_minutes=58,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-12T12:15:14+11:00"),
                    duration_minutes=34,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-12T13:02:48+11:00"),
                    duration_minutes=7,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-12T13:10:00+11:00"),
                    duration_minutes=135,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-12T15:26:32+11:00"),
                    duration_minutes=66,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-12T16:33:07+11:00"),
                    duration_minutes=67,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-12T17:40:49+11:00"),
                    duration_minutes=139,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-12T20:00:00+11:00"),
                    duration_minutes=90,
                ),
            ],
            events=[],
        ),
        DayRecord(
            timezone_name="Australia/Sydney",
            day_str="2023-03-13",
            wakeup_timestamp=arrow.get("2023-03-13T04:00:00+11:00"),
            getup_timestamp=arrow.get("2023-03-13T04:00:00+11:00"),
            bed_timestamp=arrow.get("2023-03-13T20:45:00+11:00"),
            last_night_sleep_minutes=390,
            time_intervals=[
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="morning wakeup",
                    timestamp=arrow.get("2023-03-13T04:00:00+11:00"),
                    duration_minutes=45,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"bibliotherapy": ""}),
                    extra_info="full engagement",
                    timestamp=arrow.get("2023-03-13T04:45:00+11:00"),
                    duration_minutes=30,
                ),
                TimeInterval(
                    metadata=Metadata(
                        annotation={}, label={"oj": ""}
                    ),
                    extra_info="oj",
                    timestamp=arrow.get("2023-03-13T05:15:00+11:00"),
                    duration_minutes=15,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-13T05:30:00+11:00"),
                    duration_minutes=20,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"meditation": ""}),
                    extra_info="meditation",
                    timestamp=arrow.get("2023-03-13T05:50:00+11:00"),
                    duration_minutes=10,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T06:10:08+11:00"),
                    duration_minutes=36,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="tech reading",
                    timestamp=arrow.get("2023-03-13T06:47:00+11:00"),
                    duration_minutes=18,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-13T07:05:00+11:00"),
                    duration_minutes=15,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T07:20:00+11:00"),
                    duration_minutes=6,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T07:26:26+11:00"),
                    duration_minutes=20,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-13T07:47:20+11:00"),
                    duration_minutes=44,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T08:32:37+11:00"),
                    duration_minutes=38,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T09:10:47+11:00"),
                    duration_minutes=10,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-13T09:21:17+11:00"),
                    duration_minutes=38,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"work": ""}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-13T10:00:00+11:00"),
                    duration_minutes=39,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"work": ""}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-13T10:52:39+11:00"),
                    duration_minutes=119,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-13T12:52:20+11:00"),
                    duration_minutes=22,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"nap": ""}),
                    extra_info="nap",
                    timestamp=arrow.get("2023-03-13T13:15:00+11:00"),
                    duration_minutes=55,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-13T14:13:48+11:00"),
                    duration_minutes=22,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"work": ""}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-13T14:37:55+11:00"),
                    duration_minutes=12,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T14:50:05+11:00"),
                    duration_minutes=132,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-13T17:02:19+11:00"),
                    duration_minutes=34,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"lyubishchev": ""}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T17:37:21+11:00"),
                    duration_minutes=52,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-13T18:34:10+11:00"),
                    duration_minutes=130,
                ),
            ],
            events=[],
        ),
    ]
