import arrow

from lyubishchev.data_model import DayRecord, Metadata, TimeInterval


def day_records_2023_march_12_16() -> list[DayRecord]:
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
                        annotation={}, label={"type": "self-improving", "project": "OJ"}
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
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-12T11:09:48+11:00"),
                    duration_minutes=58,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-12T12:15:14+11:00"),
                    duration_minutes=34,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
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
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
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
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
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
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="full engagement",
                    timestamp=arrow.get("2023-03-13T04:45:00+11:00"),
                    duration_minutes=30,
                ),
                TimeInterval(
                    metadata=Metadata(
                        annotation={}, label={"type": "self-improving", "project": "OJ"}
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
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="meditation",
                    timestamp=arrow.get("2023-03-13T05:50:00+11:00"),
                    duration_minutes=10,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T06:10:08+11:00"),
                    duration_minutes=36,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
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
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T07:20:00+11:00"),
                    duration_minutes=6,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
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
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-13T08:32:37+11:00"),
                    duration_minutes=38,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
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
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-13T10:00:00+11:00"),
                    duration_minutes=39,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
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
                    metadata=Metadata(annotation={}, label={"type": "sleep"}),
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
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-13T14:37:55+11:00"),
                    duration_minutes=12,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
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
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
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
        DayRecord(
            timezone_name="Australia/Sydney",
            day_str="2023-03-14",
            wakeup_timestamp=arrow.get("2023-03-14T05:05:00+11:00"),
            getup_timestamp=arrow.get("2023-03-14T05:05:00+11:00"),
            bed_timestamp=arrow.get("2023-03-14T21:30:00+11:00"),
            last_night_sleep_minutes=500,
            time_intervals=[
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="morning wakeup",
                    timestamp=arrow.get("2023-03-14T05:05:00+11:00"),
                    duration_minutes=24,
                ),
                TimeInterval(
                    metadata=Metadata(
                        annotation={}, label={"type": "self-improving", "project": "OJ"}
                    ),
                    extra_info="oj",
                    timestamp=arrow.get("2023-03-14T05:29:53+11:00"),
                    duration_minutes=42,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-14T06:12:25+11:00"),
                    duration_minutes=16,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-14T06:30:15+11:00"),
                    duration_minutes=51,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-14T07:22:13+11:00"),
                    duration_minutes=11,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-14T07:33:53+11:00"),
                    duration_minutes=81,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-14T08:55:00+11:00"),
                    duration_minutes=16,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-14T08:55:43+11:00"),
                    duration_minutes=68,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "exercise"}),
                    extra_info="jog",
                    timestamp=arrow.get("2023-03-14T09:11:00+11:00"),
                    duration_minutes=31,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-14T09:42:00+11:00"),
                    duration_minutes=30,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-14T10:12:00+11:00"),
                    duration_minutes=38,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="breakfast",
                    timestamp=arrow.get("2023-03-14T10:50:00+11:00"),
                    duration_minutes=10,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-14T11:00:00+11:00"),
                    duration_minutes=65,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-14T12:05:00+11:00"),
                    duration_minutes=43,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-14T12:49:03+11:00"),
                    duration_minutes=34,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-14T13:25:54+11:00"),
                    duration_minutes=73,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-14T14:39:31+11:00"),
                    duration_minutes=25,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="lunch",
                    timestamp=arrow.get("2023-03-14T15:05:00+11:00"),
                    duration_minutes=10,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "pmo"}),
                    extra_info="trigger: Nearmap computer",
                    timestamp=arrow.get("2023-03-14T15:15:00+11:00"),
                    duration_minutes=125,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-14T15:16:18+11:00"),
                    duration_minutes=6,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "numb"}),
                    extra_info="video",
                    timestamp=arrow.get("2023-03-14T17:20:00+11:00"),
                    duration_minutes=80,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-14T18:40:00+11:00"),
                    duration_minutes=170,
                ),
            ],
            events=[],
        ),
        DayRecord(
            timezone_name="Australia/Sydney",
            day_str="2023-03-15",
            wakeup_timestamp=arrow.get("2023-03-15T05:40:00+11:00"),
            getup_timestamp=arrow.get("2023-03-15T05:40:00+11:00"),
            bed_timestamp=arrow.get("2023-03-15T21:30:00+11:00"),
            last_night_sleep_minutes=490,
            time_intervals=[
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="morning wakeup",
                    timestamp=arrow.get("2023-03-15T05:40:00+11:00"),
                    duration_minutes=41,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-15T06:22:48+11:00"),
                    duration_minutes=27,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-15T06:50:00+11:00"),
                    duration_minutes=19,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-15T07:09:25+11:00"),
                    duration_minutes=124,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-15T09:14:15+11:00"),
                    duration_minutes=48,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="meeting",
                    timestamp=arrow.get("2023-03-15T10:02:00+11:00"),
                    duration_minutes=21,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="meeting",
                    timestamp=arrow.get("2023-03-15T10:23:56+11:00"),
                    duration_minutes=21,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="breakfast",
                    timestamp=arrow.get("2023-03-15T10:45:00+11:00"),
                    duration_minutes=25,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-15T11:10:00+11:00"),
                    duration_minutes=7,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="meditation",
                    timestamp=arrow.get("2023-03-15T11:39:11+11:00"),
                    duration_minutes=6,
                ),
                TimeInterval(
                    metadata=Metadata(
                        annotation={}, label={"type": "self-improving", "project": "OJ"}
                    ),
                    extra_info="oj",
                    timestamp=arrow.get("2023-03-15T11:46:01+11:00"),
                    duration_minutes=5,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "work"}),
                    extra_info="ssuper, work",
                    timestamp=arrow.get("2023-03-15T11:51:15+11:00"),
                    duration_minutes=11,
                ),
                TimeInterval(
                    metadata=Metadata(
                        annotation={}, label={"type": "self-improving", "project": "OJ"}
                    ),
                    extra_info="oj",
                    timestamp=arrow.get("2023-03-15T12:04:55+11:00"),
                    duration_minutes=40,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "sleep"}),
                    extra_info="nap",
                    timestamp=arrow.get("2023-03-15T12:45:33+11:00"),
                    duration_minutes=88,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-15T14:17:50+11:00"),
                    duration_minutes=12,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="meditation",
                    timestamp=arrow.get("2023-03-15T14:31:14+11:00"),
                    duration_minutes=10,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-15T14:41:50+11:00"),
                    duration_minutes=43,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "self-improving"}),
                    extra_info="lyubishchev",
                    timestamp=arrow.get("2023-03-15T15:44:19+11:00"),
                    duration_minutes=94,
                ),
                TimeInterval(
                    metadata=Metadata(annotation={}, label={"type": "routine"}),
                    extra_info="routine",
                    timestamp=arrow.get("2023-03-15T17:19:40+11:00"),
                    duration_minutes=250,
                ),
            ],
            events=[],
        ),
    ]