import requests
from typing import List
import arrow
import urllib
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging
import os

from lyubishchev.model import metric
from lyubishchev.data_ingest.promscale_ingest import promscale_http

def Exist(self, id: str, te: metric.TimeSeriesEntry) -> bool:
    """
    save to DB "exactly once" logic
    if time-entry id exist, or hash change? test if change description, or labels, anything.
    or should we check after changing to timeseries, same? yes, model same means same, even unrelated data change.
    even if desc change: how to upsert?: delete db in time range, reimport seems fine.(if data lost, just re-import)
    发现重复数据: reimport
    """
    raise

retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

EVENT_LOG = "event_log"
PAGE_SIZE = 50 # Clockify default page size
MAX_PAGES = 25 # MAX 1250 entries

class ClockifyFetcher:
    url: str
    workspaceID: str
    userID: str
    apiKey: str

    def __init__(self, url: str, workspaceID: str, userID: str, apiKey: str) -> None:
        self.url = url
        self.workspaceID = workspaceID
        self.userID = userID
        self.apiKey = apiKey

    def Fetch(
        self, startTimeUnix: int, endTimeUnix: int
    ) -> List[metric.TimeSeriesEntry]:
        if startTimeUnix > endTimeUnix:
            raise Exception(
                "start {startTimeUnix} should be smaller than {endTimeUnix}".format(
                    startTimeUnix=startTimeUnix, endTimeUnix=endTimeUnix
                )
            )

        objs = self.fetchFromClockify(startTimeUnix, endTimeUnix)

        res = []

        for o in objs:
            te = clockifyToTimeSeriesEntry(o)
            if te is not None:
                res.append(te)

        return res

    def fetchFromClockify(self, startTimeUnix: int, endTimeUnix: int) -> List[dict]:
        # Must end with Z, even input is local time. Clockify only accept timestamp end with Z, bug?
        timestampFmt = "%Y-%m-%dT%H:%M:%SZ"
        headers = {"X-Api-Key": self.apiKey}
        query = (
            "{host}/api/v1/workspaces/{workspaceID}/user/{userID}/time-entries".format(
                host=self.url,
                workspaceID=self.workspaceID,
                userID=self.userID,
            )
        )
        
        params = {
            "start": arrow.get(startTimeUnix, tzinfo='local').strftime(timestampFmt),
            "end": arrow.get(endTimeUnix, tzinfo='local').strftime(timestampFmt),
            "page-size": str(PAGE_SIZE),
            "hydrated": "true",
        }

        s = requests.Session()
        s.mount("https://", HTTPAdapter(max_retries=retries))
        queryEncode = urllib.request.pathname2url(query)
        totalRes : List[dict] = []

        page: int = 1

        while page < MAX_PAGES:
            params["page"] = str(page)
            logging.info("query: {query}, params: {params}".format(query=query, params=params))
            r = s.get("https://" + queryEncode, headers=headers, params=params)
            if r.status_code != 200:
                raise Exception("Clockify return non 200", r.text)
            resp = r.json()
            if len(resp) == 0:
                break
            totalRes.extend(resp)
            page += 1
        else:
            logging.warning("hitting max page size: {MAX_PAGES}".format(MAX_PAGES=MAX_PAGES))

        return totalRes


def clockifyToTimeSeriesEntry(clockifyEntry: dict) -> metric.TimeSeriesEntry:

    timeIntervals = clockifyEntry["timeInterval"]
    startUTC = arrow.get(timeIntervals["start"], tzinfo='utc')
    endUTC = arrow.get(timeIntervals["end"], tzinfo='utc')

    if endUTC is None:
        raise Exception("incomplete time entry found, desc: {desc}, happened: {time}".format(
            desc=clockifyEntry["description"],
            time=startUTC.isoformat(),
        ))

    unixSec = int(startUTC.timestamp())
    durationInMins = int((endUTC - startUTC).total_seconds() / 60)

    labels = generateLabelsForClockifyEntry(clockifyEntry)

    te = metric.TimeSeriesEntry(
        metricName=EVENT_LOG,
        timeUnixSec=unixSec,
        valueUnit=metric.ValueUnit.MIN,  # all value unit is minute now
        value=durationInMins,
        labels=labels,
    )

    return te


def generateLabelsForClockifyEntry(clockifyEntry: dict) -> dict:

    """
    billable -> lables["billable"]
    tags -> labels["type"]
        dispute distracted getup pmo recreation relax routine selfimproving sleep work
    description -> labels["info"]
    """
    res: dict[str, str] = {}

    res[metric.LabelKey.INFO.value] = clockifyEntry["description"]
    res[metric.LabelKey.BILLABLE.value] = str(
        clockifyEntry["billable"]
    )  # convert bool to str otherwise Promscale will complain: label value can only be string

    if "project" in clockifyEntry and clockifyEntry["project"] is not None:
        res[metric.LabelKey.PROJECT.value] = clockifyEntry["project"]["name"].lower()

    for tag in clockifyEntry["tags"]:
        if tag["name"] in [e.value for e in metric.EntryType]:
            if "type" in res:
                logging.warning("multiple type in same entries: time: {tags}".format(tags=clockifyEntry["tags"]))
            res[metric.LabelKey.TYPE.value] = tag["name"] # if multiple type tag, latter will overwrite former
        elif tag["name"] in [e.value for e in metric.EventTag]:
            res[metric.LabelKey.EVENT.value] = tag["name"]
        else:
            if tag["archived"]:
                logging.warning("archived tag, skipping")
            else:
                raise Exception("tag: {tag} unknown".format(
                    tag=tag["name"]))

    return res


if __name__ == "__main__":

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    key = os.getenv('CLOCKIFY_API_KEY')
    if key is None:
        key = ''

    fetcher = ClockifyFetcher(
        url="api.clockify.me",
        workspaceID="5e86fab7183a8475e0c7a757",
        userID="5e86fab6183a8475e0c7a755",
        apiKey=key,
    )

    # Tue 08 Jun 2021 00:00:00 AEST 1623074400
    # Wed 09 Jun 2021 00:00:00 AEST 1623160800
    timeseries = fetcher.Fetch(1623074400, 1623160800)
    for t in timeseries:
        print(repr(t))
    ing = promscale_http.PromscaleIngester("http://localhost:9201/write", metric.FakeDedupCtl())
    ing.Ingest(timeseries)
