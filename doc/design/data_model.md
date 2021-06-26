
*  Time entry转为metric, 每个有unique tags
*  不同的tag, 组成不同的time series

## Time entry

starttime: 转为产生timestamp
duration: 转为value

扁平化的tag(不带value), 转为key-value pair

```json
{
    "id": "60b7eac0f3682e75a2dc92ad",
    "description": "routine",
    "tagIds": [
      "5e86fde4fbe9b56304197ebf"
    ],
    "userId": "5e86fab6183a8475e0c7a755",
    "billable": false,
    "taskId": null,
    "projectId": null,
    "timeInterval": {
      "start": "2021-06-02T20:32:00Z",
      "end": "2021-06-02T20:45:01Z",
      "duration": "PT13M1S"
    },
    "workspaceId": "5e86fab7183a8475e0c7a757",
    "isLocked": false,
    "customFieldValues": null
  },
```

# Metric

*  metric name用tag指明， 如果shard by metrics,  无法显示两人的起床时间在一张图上? 可以倒是. 
    +  shard by metric容易扩展吧? 
*  metric = metricName + Timestamp + Value(float) + labels

## TimeEntry

```json
{
  "name": "timeEntry",
  "timestamp": UNIX,
  "unit": "durationInMinute",
  "value": 20,
  "labels": [
    {
      "type": "routine", # selfimproving, etc
      "category": "I",
      "billable": true,
      "project": "",
      "info": "type=book,task=奇特的一生"
    }
  ]
}
```

### info 

对比用标准的subtag来给出额外信息: "task": "subtype, could be housework, chinatown? 不灵活?"

汇总时间的产出:

列出每项事花了多少时间: 具体task:

每个project具体做了什么, 或者match filter result的时间内的产出:

*  routine都花在哪里, 家务? 子标签还是输入

*  阅读一本书花了多久
*  做一个具体项目, 花了多久
*  routine花在哪里: chinatown, 
*  distract花在哪里: 

每个子分类有自己的格式

#### OJ

做了哪些题

#### Engineer

*  看书
*  哪些项目
*  博客 
*  练习什么

#### Math

*  哪些书

#### CV

*  哪些书
*  练习

## Event

```json
{
  "name": "getupTime",
  "timestamp": UNIX,
  "unit": "TimestampUNIX",
  "value": 11121871738,
  "labels": [
    {
    }
  ]
}
```

### Getup, Sleep time

*  Use unix timestamp as value, same as timestamp

### Cold

*  上个月cold几次

### Incident

*  injure, not able to sport

## Prometheus format

```golang
TimeSeries{
  Labels: []Label{
      {
        Name:  "__name__",
        Value: "timeEntry",
      },
      {
        Name: "unit",
        Value: "durationInMinute",
      },
      ...
  },
  Samples: []Sample{
      {
          Timestamp: 1577836800000,
          Value:         100.0,
      },
  },
}
```

## Promscale HTTP

```json
{
    "labels":{"__name__": "cpu_usage", "namespace":"dev", "node": "brain"},
    "samples":[
        [1577836800000, 100],
        [1577836801000, 99],
        [1577836802000, 98],
        ...
    ]
}
{
    "labels":{"__name__": "cpu_usage", "namespace":"prod", "node": "brain"},
    "samples":[
        [1577836800000, 98],
        [1577836801000, 99],
        [1577836802000, 100],
        ...
    ]
}
```