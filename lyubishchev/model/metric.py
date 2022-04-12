from enum import Enum
from typing import Protocol, List
import arrow


class ValueUnit(Enum):
    MIN = "min"
    UNIX_SEC = "unix_sec"


class EntryType(Enum):
    DISPUTE = "dispute"
    DISTRACTED = "distracted"
    PMO = "pmo"
    RECREATION = "recreation"
    RELAX = "relax"
    ROUTINE = "routine"
    SELF_IMPROVING = "self_improving"
    WORK = "work"
    SOCIAL = "social"


class EventTag(Enum):
    GETUP = "getup"
    SLEEP = "sleep"


class LabelKey(Enum):
    TYPE = "type"
    INFO = "info"
    BILLABLE = "billable"
    PROJECT = "project"
    EVENT = "event"


mandatory_keys = {
    LabelKey.TYPE.value,
    LabelKey.INFO.value,
    LabelKey.BILLABLE.value,
}

optional_keys = {
    LabelKey.PROJECT.value,
    LabelKey.EVENT.value,
}

class Project(Enum):
    BLOG = "blog"
    ENGINEERING = "engineering"
    GIS = "gis"
    MATH = "math"
    OJ = "oj"
    POKER = "poker"
    REVIEW_PLANNING = "reviewplanning"
    SPORTS = "sports"
    READING = "usefulreading"
    WORK = "work"


billableProjects = {
    Project.BLOG.value,
    Project.ENGINEERING.value,
    Project.GIS.value,
    Project.MATH.value,
    Project.OJ.value,
}

class TimeSeriesEntry:
    # MetricName should be lowercase connected with _, e.g event_log
    MetricName: str
    TimeUnixSec: int
    Unit: ValueUnit
    Value: float
    Labels: dict

    def __init__(
        self,
        metricName: str,
        timeUnixSec: int,
        valueUnit: ValueUnit,
        value: float,
        labels: dict,
    ) -> None:
        self.MetricName = metricName
        self.TimeUnixSec = timeUnixSec
        self.Unit = valueUnit
        self.Value = value
        self.Labels = labels

    def __repr__(self) -> str:
        return "{MetricName}, {startTime}, labels:{Labels}".format(
            MetricName=self.MetricName,
            startTime=arrow.get(self.TimeUnixSec, tzinfo='local').isoformat(),
            Labels=self.Labels,
        )

    def project(self) -> str:
        return self.Labels.get(LabelKey.PROJECT.value, '')

    def billable(self) -> str:
        return self.Labels.get(LabelKey.BILLABLE.value, '')

    def type(self) -> str:
        return self.Labels.get(LabelKey.TYPE.value, '')

    def info(self) -> str:
        return self.Labels.get(LabelKey.INFO.value, '')

    def event(self) -> str:
        return self.Labels.get(LabelKey.EVENT.value, '')


# Fetch data from datasource, currently is Clockify
class Fetcher(Protocol):
    def Fetch(self, startTimeUnix: int, endTimeUnix: int) -> List[TimeSeriesEntry]:
        raise


# Ingest data into data backend, currently is Promscale(backed by TimescaleDB)
class Ingester(Protocol):
    def Ingest(self, series: List[TimeSeriesEntry]) -> None:
        raise

class DedupCtl(Protocol):
    def get_latest_timestamp(self) -> int:
        raise
    def save_latest_timestamp(self, unix_timestamp: int) -> None:
        raise


class FakeDedupCtl:
    def get_latest_timestamp(self) -> int:
        ...

    def save_latest_timestamp(self, unix_timestamp: int) -> None:
        ...

class BatchImport:
    """
    Batch import cmd, specify [start, end]
    """

    fetcher: Fetcher
    ingester: Ingester
    startTimeUnix: int
    endTimeUnix: int
    ...


class Monitor:
    fetcher: Fetcher
    ingester: Ingester
    fetchAheadDays: int
    fetchLagDays: int

    def __init__(self):
        pass

    def monitor(self):
        # endless loop to keep fetching data [now-fetchAheadDays, now-fetchLagDays]
        # 只要把data注入即可，考虑周总结
        # 做成一次性的script也行: 每次周总结时，ingest上周的metric? 都支持
        # 终极目标是daily bucket统计各项关键指标, 可能需要advanced query: Advanced analytic queries https://docs.timescale.com/timescaledb/latest/how-to-guides/query-data/advanced-analytic-queries/##advanced-analytic-queries
        # if found active entry, stop; skip over active entry
        pass


if __name__ == "__main__":
    te = TimeSeriesEntry(
        "event_log",
        1623074400,
        ValueUnit.MIN,
        1.0,
        {
            "__name__": "event_log",
            "type": "routine",
        },
    )
    print(repr(te))
    print([e.value for e in Project])
    print(type(LabelKey), type(LabelKey.INFO), type(LabelKey.INFO.value))
