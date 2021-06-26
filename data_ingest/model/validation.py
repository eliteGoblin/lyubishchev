import arrow
import logging
from typing import List, Callable
from . import metric


def validate_getup_sleep(series_day_bucket: List[metric.TimeSeriesEntry]) -> None:
    ct_getup: int = 0
    ct_sleep: int = 0

    cur_date: str = get_local_datestr_from_unixsec(series_day_bucket[0].TimeUnixSec)

    if metric.EventTag.GETUP.value != series_day_bucket[0].event():
        raise Exception("get up tag missing in first record, local date: {date}".format(
            date=cur_date
        ))

    if metric.EventTag.SLEEP.value != series_day_bucket[-1].event():
        raise Exception("sleep tag missing in last record, local date: {date}".format(
            date=cur_date
        ))

    for entry in series_day_bucket:
        if metric.EventTag.GETUP.value == entry.event():
            ct_getup += 1
        if metric.EventTag.SLEEP.value == entry.event():
            ct_sleep += 1

    if ct_getup != 1:
        raise Exception("daily getup more than 1: {date}".format(date=cur_date))
    if ct_sleep != 1:
        raise Exception("daily sleep more than 1: {date}".format(date=cur_date))


def validate_total_duration(series_day_bucket: List[metric.TimeSeriesEntry]) -> None:
    expected_mins: int = 14 * 60
    duration_count_mins: int = 0

    for entry in series_day_bucket:
        if entry.Unit != metric.ValueUnit.MIN:
            raise Exception("unit must be in mins, but{unit} got".format(unit=entry.Unit))
        duration_count_mins += int(entry.Value)

    if duration_count_mins < expected_mins:
        raise Exception("daily record {record} lower than expectation {expected} (mins)".format(
            record=duration_count_mins,
            expected=expected_mins,
        ))

    if duration_count_mins >= 24 * 60:
        raise Exception("daily record {record} larger than a day {expected} (mins)".format(
            record=duration_count_mins,
            expected=24 * 60,
        ))


def validate_labels(series_day_bucket: List[metric.TimeSeriesEntry]) -> None:
    """
    time entry: non empty `type` tag, LabelKey
    mandatory tags
        TYPE
        INFO
        BILLABLE
    optional:
        PROJECT
        EVENT: atm only getup and sleep
    """
    cur_date: str = get_local_datestr_from_unixsec(series_day_bucket[0].TimeUnixSec)
    for entry in series_day_bucket:
        for key in entry.Labels:
            assert type(key) == str, "actual {key} wit type: {typ}, date: {date}".format(key=key, typ=type(key), date=cur_date)
        if len(entry.Labels) < len(metric.mandatory_keys):
            raise Exception("mandatory key missing: {date}".format(
                date=get_local_datestr_from_unixsec(series_day_bucket[0].TimeUnixSec)
            ))
        if len(entry.Labels) > len(metric.mandatory_keys) + len(metric.optional_keys):
            raise Exception("too many keys, {date}".format(
                date=get_local_datestr_from_unixsec(series_day_bucket[0].TimeUnixSec)
            ))
        assert entry.type() != "", cur_date
        assert entry.info() != "", cur_date
        assert entry.billable() != "", cur_date

def validate_billable(series_day_bucket: List[metric.TimeSeriesEntry]) -> None:
    """
    check if time entry type is matching billable
    """
    cur_date: str = get_local_datestr_from_unixsec(series_day_bucket[0].TimeUnixSec)
    for entry in series_day_bucket:
        if entry.Labels[metric.LabelKey.BILLABLE.value] == str(False):
            continue
        if entry.Labels[metric.LabelKey.TYPE.value] != metric.EntryType.SELF_IMPROVING.value:
            raise Exception("billable should have self_improving tag, got {type}, of date{date}".format(
                            type=entry.Labels[metric.LabelKey.TYPE.value], date=cur_date))
        if entry.Labels[metric.LabelKey.PROJECT.value] is None:
            raise Exception("billable's project missing, date{date}".format(date=cur_date))
        if entry.project() not in metric.billableProjects:
            raise Exception("project {project} should not be billable".format(project=entry.project()))


def validate_project(series_day_bucket: List[metric.TimeSeriesEntry]) -> None:

    cur_date: str = get_local_datestr_from_unixsec(series_day_bucket[0].TimeUnixSec)
    for entry in series_day_bucket:
        if entry.project() == "":
            continue
        if entry.project() not in [e.value for e in metric.Project]:
            raise Exception("invalid project {project}, {date}".format(
                project=entry.project(), date=cur_date))
        if entry.project() == metric.Project.WORK.value:
            assert entry.Labels[metric.LabelKey.TYPE.value] == metric.EntryType.WORK.value, cur_date
        elif entry.project() == metric.Project.SPORTS.value:
            assert entry.Labels[metric.LabelKey.TYPE.value] == metric.EntryType.RECREATION.value, cur_date
        else:
            assert entry.Labels[metric.LabelKey.TYPE.value] == metric.EntryType.SELF_IMPROVING.value, \
                "entry {entry} with {date}".format(entry=entry, date=cur_date)


def validate_time_series(time_series: List[metric.TimeSeriesEntry],
                         *validators: Callable[[List[metric.TimeSeriesEntry]], None]) -> None:
    logging.debug("total series: {count}".format(count=len(time_series)))

    current_day: str = get_local_datestr_from_unixsec(time_series[0].TimeUnixSec)
    series_day_bucket: List[metric.TimeSeriesEntry] = []

    for e in time_series:
        if get_local_datestr_from_unixsec(e.TimeUnixSec) != current_day:
            validate_day_bucket(series_day_bucket, *validators)
            current_day = get_local_datestr_from_unixsec(e.TimeUnixSec)
            series_day_bucket.clear()

        series_day_bucket.append(e)
    else:
        if len(series_day_bucket) > 0:
            validate_day_bucket(series_day_bucket, *validators)

def validate_timeentry(series_day_bucket: List[metric.TimeSeriesEntry]) -> None:
    """
    not allow time entry across day
    """
    cur_date: str = get_local_datestr_from_unixsec(series_day_bucket[0].TimeUnixSec)
    for entry in series_day_bucket:
        date: str = get_local_datestr_from_unixsec(entry.TimeUnixSec + int(entry.Value) * 60)
        assert cur_date != date, "time entry{entry} across day".format(entry=entry)
        assert entry.Value < 8 * 60  # single time entry less than 8 rs, value in mins
        assert entry.type() != "", "entry tag is empty: {entry}".format(entry=entry)

def get_local_datestr_from_unixsec(unix_sec: int) -> str:
    return arrow.get(unix_sec, tzinfo='local').date().isoformat()


def validate_day_bucket(series_day_bucket: List[metric.TimeSeriesEntry],
                        *validators: Callable[[List[metric.TimeSeriesEntry]], None]) -> None:
    current_day: str = get_local_datestr_from_unixsec(series_day_bucket[0].TimeUnixSec)

    for v in validators:
        try:
            v(series_day_bucket)
        except Exception as e:
            if current_day > "2021-06-01":
                raise
            logging.warning("old record violate validation: {error}".format(error=e))

    logging.debug("{day} validated, entries: {count}".format(day=current_day, count=len(series_day_bucket)))


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
    validate_time_series(ts,
                         validate_getup_sleep,
                         validate_total_duration
    )