

# Requirements

*  查找: 比如指定开始 6-01, 并不知道601自己几点起床的.  需要从601开始00:00之后, 第一个wakeup time, 为开始.
*  结束: 
   *  [start, end] or [start, end): 6-05: 想不想要6.5数据? 不想要. end ) 更一致. 
   *  找到end日子的wakeup event, (从end date 0:00开始), 再找之前最后一个bed time event.
   *  返回TimeIntervals: 
      *  精确的处于: [start date's wakeup, end date之前最后一个bedtime]
      *  最后的bedtime可能 within end_date(比如02:00am睡觉), 也可能是之前22:00就睡了
      *  之前最后一天的睡眠时间, 用以fill第一天的睡眠时间. 


*  `fetch_time` 取决于implementation: 哪种backend; 只要取得了TimeInterval, 便进入了抽象的business domain, 与实现无关. 

```py
from collections import namedtuple

FetchResults = namedtuple("FetchResults", "time_intervals events")

class TimeIntervalFetcher(ABC):  # pylint: disable=too-few-public-methods
   """
   throw: ?
   """

   @abstractmethod
   def fetch_time_intervals_events(self, start_date: string, end_date: string) -> tuple[List[TimeInterval], List[Event]]:
      """
      start_date, end_date : YYYY-MM-DD
      [start, end)
      """

   # @abstractmethod
   # 感觉并不是真正的需求: 目前没有需要回溯的.
   # def fetch_last_event(self, timestamp: Arrow, event_type: str) -> Arrow
   #    """
   #    Get when was the last event before given timestamp
   #    """
```

# Output

TimeIntervals: 时间within event的时间range.
Events: 第一天wakeup第一条; 最后一条是bed.

# Design

*  简化接口: 标准化为timestamp.
*  过滤TimeInterval, 并装入DayRecord, 这是business logic. 并不是implementation difference.

TODO: think how to use it, 目前的想法: Fetcher只关心从无歧义timestamp, 获取intervals and events

Business Logic中:

1.  generate timestamp using date str
2.  using timestamp to get events and time intervals
3.  get accurate range: [fist wakeup, last bed] of events: 
    1.  start是00:00开始，wakeup一定在此之后: e.g June 1 的start: June 1 00:00之后的第一个wakeup.
    2.  如何区分最后一天bedtime: 可能是前一天凌晨睡觉; 也可能是后一天早睡; 诀窍: end的wakup之前的bedtime为最后一个bedtime. 
    3.  e.g [June 1, June 5) : end timestamp 为 June 5 23:59, 不想包含June 5的records: 首先从后往前找到最后一个wakeup, 即June 5的wakeup.(从来没有第二天的wakeup早于23:59); 以此，倒着找之前最后一个bedtime, 即为 June 4 的bedtime.
4.  用accurate range, refine TimeIntervals, 为分割成每天做准备. 


分割每天时: 

用类似函数, start index, parse_next_day(); 遍历所有的TimeIntervals, Events; Fill DayRecord data structure.