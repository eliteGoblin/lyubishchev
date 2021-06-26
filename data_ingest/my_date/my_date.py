
from datetime import datetime
import dateutil.relativedelta as relativedelta
from typing import Tuple

"""
isoweekday() - Monday is 1 and Sunday is 7
weekday() - Monday is 0 and Sunday is 6
"""

"""
与date +'%U'兼容的算法
"""

"""
365 / 7  = 52.xxx
[0, 51], e.g 2020-52-1 = 2020-12-28, 内部是从monday开始的.
一年的规划: 
    允许周跨年: 每年[0, 51], 共计52个完整周
    0周的Monday很可能在前一年; 52周的结束很可能在后一年
2021.0 == 2020.52
"""

def firstLastDayOfWeek(year: int, week: int) -> Tuple[datetime, datetime]:
    """
    firstDay is Sunday, timezone aware
    week [firstDay, lastDay) i.e Sunday to next Sunday
    """
    if week < 0 or week > 52:
        raise Exception("week should be [0, 52]")
    # get monday, then get previous Sunday
    # datetime's week start Monday, finish Sunday
    # my week start Sunday, finish before next Sunday
    monday = datetime.strptime('{year}-{week}-1'.format(year=year, week=week), "%Y-%W-%w")
    sunday = monday + relativedelta.relativedelta(days=-1)
    nextSunday = sunday + relativedelta.relativedelta(days=7)
    
    return sunday, nextSunday


if __name__ == '__main__':
    ds, dl = firstLastDayOfWeek(2021, 23)
    print(ds.isoformat(), dl.isoformat())