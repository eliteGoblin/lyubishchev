
# v0.1.0 data model

Every time series is uniquely identified by its metric name and optional key-value pairs called labels.

A custom metric is identified by a unique combination of a metric’s name and tag values (including the host tag).

## Time interval

```json
{
    "metadata": {
        "version": "v0.1.0", # semver
        "annotation": {
            "key1": "value1",
            "key2": 2
        },
        "label": {
            "key1": "value1", # label value should be strings, bool
            "key2": "value2",
            "key3": true,
            "social": "" # empty value used as tag here (key only)
        }
    },
    "extra_info": "blah",
    "timestamp": 1112233, # use datatime object (with timezone), or arrow's datetime object?
    "duration_minutes": 15
}
```

Note:

*  Duration时间精度为mins
*  Label key value 都是string, 主要用于filter
*  Annotation key为string, value可以为valid JSON value

### Validation

*  Required fields, 除了annotation, 全部require
*  所有Fields不为空, 默认值

##  Event 

```json
{
    "metadata": {
        "version": "v0.1.0", # semver
        "annotations": {
            "key1": "value1",
            "key2": 2
        },
        "labels": {
            "key1": "value1", # label value should be strings, bool
            "key2": "value2",
            "key3": true
            "social": "" # empty value used as tag here (key only)
        }
    },
    "extra_info": "blah",
    "timestamp": 1112233
}
```


## Daily summary

*  统计的粒度最小是一天
*  给定日期: 如何界定一天: [起床开始, 睡觉]; 并不是严格按24小时分割.
   *  给定日期开始第一个起床时间标志day start
   *  getup之后第一个gobed标志结束
*  day summary非睡眠指标: 指这段时间的summary, 即清醒时间. 
*  day summary 睡眠指标: 
   *  睡眠时间=昨晚睡眠+白天daytime的sleep.
e.g 
   *  工作到凌晨, e.g Jun 2 01:30, 睡觉; 起床7:30; Jun 2 23:00 睡觉: 
      *  June 1 由起床时间算起, 到June 2 01:30结束
      *  June 2 由 7:30开始，到23:00结束


generated based on TimeIntervals and Events

```json
{
    "date": , # with timezone
    "wakeup_time": 123456789,
    "getup_time": 123456789,
    "bed_time": 123456789,
    "sleep_minutes": 9999,
    "happiness": 3.5, # 1-5, float
    "time_intervals": [], # 按发生时间排序
    "events": [] # 发生时间排序
}
```

*  time_intervals和events需要排序
*  events第一个为wakeup, 最后一个为gobed
*  List of Day = interval: 周总结，季度总结，年总结等. 

### Validation

*  有且仅有一个event: gobed, getup: gobed < wakeup <= getup
*  统计总时间合理: [13h - 20h]

