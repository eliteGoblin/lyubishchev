#!/usr/bin/env python

import os
import sys
import arrow
import argparse
import logging

from typing import Tuple, List
from my_date import my_date
from datetime import datetime

from lyubishchev.data_ingest import simple_dedup
from lyubishchev.model import validation
from lyubishchev.model import metric
from lyubishchev.data_ingest.clockify_fetcher import clockify
from lyubishchev.data_ingest.promscale_ingest import promscale_http

"""
python lyubishchev.py --clockify-host=api.clockify.me \
--api-key=xxx \
--workspace=5e86fab7183a8475e0c7a757 \
--user=5e86fab6183a8475e0c7a755 \
--start-date=6-1 \
--end-date=6-3 \
--week=21 \
--offset-days=12
"""

def range_limited_float_type(arg):
    """
    Type function for argparse - a float within some predefined bounds 
    https://stackoverflow.com/questions/55324449/how-to-specify-a-minimum-or-maximum-float-value-with-argparse
    """
    MIN_VAL = 0
    MAX_VAL = 53
    f = int(arg)
    if f < MIN_VAL or f > MAX_VAL:
        raise argparse.ArgumentTypeError("Argument must be < " + str(MAX_VAL) + "and > " + str(MIN_VAL))
    return f


def timeRangeFromArgs(args) -> Tuple[int, int]:
    """
    return (startUnixSec, endUnixSec)
    """
    if args.start_date and args.end_date:
        return timeRangeFromStartEnd(args.time_zone, args.start_date, args.end_date)
    if args.week != None:
        return timeRangeFromWeek('local', args.week)
    if args.offset_days != None:
        return timeRangeFromOffsetDays(args.offset_days)

    logging.info("using default: import -7d")

    return timeRangeFromOffsetDays(-7)

def timeRangeFromStartEnd(tzName: str, startDate: str, endDate: str) -> Tuple[int, int]:
    """
    take local date
    output: UNIX time, both 00:00
    """
    if not startDate and not endDate:
        raise Exception("start and end date must not be empty")

    startDateArrow: arrow.Arrow = arrow.get(startDate, 'YYYY-M-D', tzinfo=tzName)
    endDateArrow: arrow.Arrow = arrow.get(endDate, 'YYYY-M-D', tzinfo=tzName)

    startUnixSec = int(startDateArrow.timestamp())
    endUnixSec = int(endDateArrow.timestamp())

    if startUnixSec > endUnixSec:
        raise Exception("start must before end date")

    return startUnixSec, endUnixSec

def timeRangeFromWeek(tzName: str, week: int) -> Tuple[int, int]:
    sunday, nextSunday = my_date.firstLastDayOfWeek(datetime.now().year, week)

    # arrow.get(sunday, tzinfo='Australia/Sydney') not working
    # avoid pass ambiguous datetime to arrow, even specify with timezone
    tzSunday = arrow.get(sunday.isoformat(), tzinfo=tzName)
    tzNextSunday = arrow.get(nextSunday.isoformat(), tzinfo=tzName)

    logging.debug("weekNumber:{week}, start: {start}, end: {end}".format(
        week=week,
        start=tzSunday.isoformat(),
        end=tzNextSunday.isoformat(),
    ))

    return int(tzSunday.timestamp()), int(tzNextSunday.timestamp())


def timeRangeFromOffsetDays(offsetDays: int) -> Tuple[int, int]:
    if offsetDays <= 0 or offsetDays > 30:
        raise Exception("invalid offset {offset}".format(offset=offsetDays))
    start_date = arrow.now().shift(days=-1 * offsetDays).date().isoformat()
    today_date = arrow.now().date().isoformat()
    return timeRangeFromStartEnd('local', start_date, today_date)


if __name__ == "__main__":

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    """
    ./ingest.py -s=6-1 -e=6-3 [start, end), 以00:00起始
    ./data_ingest -w=16  week来指定: SUN-SAT
    ./data_ingest -od=12 不算今天, 前12天
    """
    parser = argparse.ArgumentParser(
        description="Personal time tracking system"
    )

    required = parser.add_argument_group('date range arguments, specify one of them')
    dateRange = parser.add_argument_group('daterange arguments')

    required.add_argument('--clockify-host',
        default="api.clockify.me",
    )
    required.add_argument('--api-key',
        default=os.getenv('CLOCKIFY_API_KEY', 'fake_clockify_key')
    )
    required.add_argument('--workspace',
        help='workspaceID of clockify',
        default='5e86fab7183a8475e0c7a757',
    )
    required.add_argument('--user',
        help='userID of clockify',
        default='5e86fab6183a8475e0c7a755',
    )
    required.add_argument('--time-zone',
        help='timezone of input, default as system time',
        default='local',
    )

    dateRange.add_argument('--start-date',
        help='start date as YYYY-MM-DD, must also specify end-date, example: --start-date=2021-06-24 --end-date=2021-06-25',
    )
    dateRange.add_argument('--end-date',
        help='end date as YYYY-MM-DD, must also specify start-date',
    )
    dateRange.add_argument('--week',
        type=range_limited_float_type,
        help='import time entries of specific week, Sunday as first day, [0, 53], example: --week=24',
    )
    dateRange.add_argument('--offset-days',
        help='import time entries of previous days to yesterday: [-offset d, -1d], max 30',
        type=int,
        default=7,
    )

    #  
    # IDEA: date range group 输入以day为单位, 转为标准的range: unixTimeSec
    # setup metrics in graph, 关键指标，tickets
    # 考虑建立weekly dashboard metric以week命名? week总结? 有点远了. 

    args = parser.parse_args()

    logging.info("args: {args}".format(args=args))

    startUnixSec, endUnixSex = timeRangeFromArgs(args)

    fetcher = clockify.ClockifyFetcher(
        url=args.clockify_host,
        workspaceID=args.workspace,
        userID=args.user,
        apiKey=args.api_key,
    )

    # # Tue 08 Jun 2021 00:00:00 AEST 1623074400
    # # Wed 09 Jun 2021 00:00:00 AEST 1623160800
 
    logging.info("start time: {startTime}, end time: {endTime}".format(
        startTime=arrow.get(startUnixSec, tzinfo='local'),
        endTime=arrow.get(endUnixSex, tzinfo='local'),
    ))

    time_series = fetcher.Fetch(startUnixSec, endUnixSex)
    time_series.sort(key=lambda entry: entry.TimeUnixSec)
    # validate time series by applying check functions
    validation.validate_time_series(time_series,
                                          validation.validate_getup_sleep,
                                          validation.validate_total_duration,
                                          validation.validate_labels,
                                          validation.validate_billable,
                                          validation.validate_project,
                                          )

    # bypass record already ingested
    dedupCtl = simple_dedup.Dedup('./latest_timestamp.txt')
    last_record_timestamp = dedupCtl.get_latest_timestamp()

    dedup_ts: List[metric.TimeSeriesEntry] = []
    for v in time_series:
        if v.TimeUnixSec <= last_record_timestamp:
            logging.warning("possible dup record: {time} before latest time entry: {latest}".format(
                time=arrow.get(v.TimeUnixSec, tzinfo='local').isoformat(),
                latest=arrow.get(v.TimeUnixSec, tzinfo='local').isoformat(),
            ))
            continue
        dedup_ts.append(v)

    if len(dedup_ts) == 0:
        logging.info("no record to be ingested, exit...")
        sys.exit(0)

    if arrow.get(dedup_ts[-1].TimeUnixSec, tzinfo='local').date().isoformat() > '2022-06-01':
        # gap between last record and records to be ingested can not be more than 12hrs
        lastDt = arrow.get(dedup_ts[-1].TimeUnixSec, tzinfo='local').date().isoformat()
        gap: int = dedup_ts[0].TimeUnixSec - last_record_timestamp
        expect: int = 12 * 3600
        assert gap < expect, "{date} gap:{gap} should be less than {expect}".format(date=lastDt, gap=gap, expect=expect)

        logging.debug("last timestamp: {last}, first timestamp to ingest: {first}, gap since last ingested is {gap} hrs".format(
            first=arrow.get(dedup_ts[0].TimeUnixSec, tzinfo='local').isoformat(),
            last=arrow.get(last_record_timestamp, tzinfo='local').isoformat(),
            gap=gap / 3600.0))

    logging.info("Validation passed! time series count {count}".format(count=len(dedup_ts)))

    ing = promscale_http.PromscaleIngester("http://localhost:9201/write", dedupCtl)
    ing.Ingest(dedup_ts)

    sys.exit(0)
