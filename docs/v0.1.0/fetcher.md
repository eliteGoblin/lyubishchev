

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

问题: 

*  DayRecord模型里，把getup, wakeup, bed视为event吗? 还是implementation detail; 这几个作为day summary的field, 而不是event, 减少工作量(貌似这个合理).

TODO:

*  决定 ^^ 
*  Unit test of DayRecord
