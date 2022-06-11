
# Background

*  时间是business model的核心属性
*  涉及到时区travel, 如何显示不同时区的时刻是个问题.

# Use Case

## 跨时区

*  Frank query time entry 和 event, using date; 最小粒度是day: YYYYMMDD
*  Date should be "local" where Frank was at, where TimeInterval/Event happened
  

E.g Frank 

*  Jun 1 in Sydney; 
*  Jun 2 in Beijing. 
*  Jun 3 in US.

In Jun 3, generate report [Jun 1, Jun 3]

When specify Jun 1, means get day summary using Beijing Time. 


## Day light saving

Australian Eastern Standard Time (AEST), UTC+10:00: 冬季采用
Australian Eastern Daylight Time (AEDT), UTC+11:00: 夏季采用
北京 (CST) UTC + 8
悉尼在北京的东(东南)

*  Oct 1: 
*  Oct 2: 2am 

Frank希望respect daylight saving; 

时刻应该遵循DST, e.g: 

起床曲线: 应该与当时Frank的iphone手机显示时间相同(iphone respect DST)

以为着应该用 `IANA` 标准: 时区命名标准化

## Fetch data

Frank在US，想分析在Sydney, 北京记录的数据: 

Fetch [Jun1, Jun3) , 即Jun 1(Sydney)， June 2(Beijing), 但不包括US.

"Give me Jun 1, Jun 2" data, I don't care which local timezone with the time entries.

想要的是: 

local time 为 Jun 1 的; 完整的一天: 第一条wakeup; 最后一条: gobed.

问题:
backend中, 并不存储timezone信息; 
比如clockify: 并没有存储时区，返回一律UTC.

因为Jun 1, Jun 2对于系统有歧义: 不知道是哪个时区，因此Jun 1采用local time. 

根据 you aren't gonna need it 原则: 只考虑Sydney time. 
 
# Design

```
timedatectl list-timezones
```
常用:
*  Sydney: `Australia/Sydney`
*  Beijing: `Asia/Shanghai`

内部用 IANA 的timezone 名字. 
外部如何Query? 


```python
class TimeIntervalFetcher(ABC):
    def fetch_time(self, start_time Arrow, end_time: Arrow) -> List[TimeInterval]
```

全部是local time. 不考虑跨时区需求. 

## Clockify

> start: string, in query You send time according to your account's timezone (from Profile Settings) and get response with time in UTC
