import sys
sys.path.append("..")
from model import metric
import requests
import json
from typing import List
import logging, arrow


class TranslateIter(object):
    translateName: dict

    def __init__(self, translateName):
        self.translateName = translateName

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if attr != "translateName":
                yield attr, value


def toDictItem(obj):
    if isinstance(obj, TranslateIter):
        res = {}
        for k, v in obj:
            subObj = getattr(obj, k)
            res[k] = toDictItem(subObj)
        if hasattr(obj, "translateName"):
            for k, v in obj.translateName.items():
                res[v] = res.pop(k)
        return res
    if isinstance(obj, list):
        res = []
        for k in obj:
            res.append(toDictItem(k))
        return res
    op = getattr(obj, "toDictItem", None)
    if callable(op):
        return obj.toDictItem()
    return obj


class Sample:
    unixTimeInMilliSec: int
    value: float

    def __init__(self, timestamp: int, value: float) -> None:
        self.unixTimeInMilliSec = timestamp
        self.value = value

    def toDictItem(self) -> list:
        return [self.unixTimeInMilliSec, self.value]


class PromscaleRequest(TranslateIter):
    labels: dict
    samples: List[Sample]

    def __init__(self, labels: dict, samples: List[Sample]) -> None:
        self.labels = labels
        self.samples = samples

    def __repr__(self):
        from pprint import pformat

        return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4, width=1)

    def validate(self) -> None:
        if "__name__" not in self.labels:
            raise Exception(self, "__name__ must be present in labels")
        if len(self.samples) == 0:
            raise Exception(self, "samples must not be empty")


class PromscaleIngester:
    promscaleURL: str
    session: requests.Session
    dedup: metric.DedupCtl

    def __init__(self, promscaleURL: str, dedup: metric.DedupCtl) -> None:
        self.promscaleURL = promscaleURL
        self.session = requests.Session()
        self.dedup = dedup

    def Ingest(self, series: List[metric.TimeSeriesEntry]) -> None:
        for v in series:
            promReq = TimeSeriesEntryToPromscaleRequest(v)
            r = self.session.post(self.promscaleURL, json=toDictItem(promReq))
            logging.debug("request: {request}, response: {code}, {txt}".format(
                request=json.dumps(toDictItem(promReq)),
                code=r.status_code,
                txt=r.text))
            assert r.status_code == 200, "code got {code}".format(code=r.status_code)
            # save to end of last entry, not start of last time entry, value in DurationInMins
            assert v.Unit == metric.ValueUnit.MIN
            self.dedup.save_latest_timestamp(v.TimeUnixSec + int(v.Value) * 60)


def TimeSeriesEntryToPromscaleRequest(te: metric.TimeSeriesEntry) -> PromscaleRequest:
    """
    1 entry -> 1 request
    MetricName as label `__name__`, must not be mixed case
    TimeUnixSec as sample[0]
    Value as sample[1]
    Labels -> labels
    """
    labels = te.Labels
    labels["__name__"] = te.MetricName.lower()
    sample = Sample(
        timestamp=te.TimeUnixSec
        * 1000,  # Promscale's timestamp,integer timestamp in milliseconds since epoch
        value=te.Value,
    )
    pr = PromscaleRequest(
        labels=labels,
        samples=[sample],
    )
    pr.validate()
    return pr


if __name__ == "__main__":
    ts = [
        metric.TimeSeriesEntry(
            metricName="event_log",
            timeUnixSec=1623275236,
            valueUnit=metric.ValueUnit.MIN,
            value=15,
            labels={
                "userID": "frank.sun",
                "category": "I",
                "type": "routine",
                "billable": "false",
                "info": "routine",
            },
        ),
        metric.TimeSeriesEntry(
            metricName="event_log",
            timeUnixSec=1623275237,
            valueUnit=metric.ValueUnit.MIN,
            value=61,
            labels={
                "userID": "frank.sun",
                "category": "II",
                "type": "selfimproving",
                "billable": "true",
                "project": "OJ",
                "info": "level=easy,id=12|level=hard,id=223",
            },
        ),
    ]
    # ing = PromscaleIngester("https://hookb.in/jezoDdXNzLieBB23ypmz")
    ing = PromscaleIngester("http://localhost:9201/write", metric.FakeDedupCtl())
    ing.Ingest(ts)
