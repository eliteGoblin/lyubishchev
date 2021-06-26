

<img src="https://raw.githubusercontent.com/eliteGoblin/images/master/blog/img/picgo/20210604081422.png" alt="20210604081422" style="width:500px"/>

## Data Collect

标准化为JSON: 

```json
{
  "name": "timeEntry",
  "timestamp": UNIX,
  "unit": "durationInMinute",
  "value": 20,
  "labels": [
    {
      "userName": "frank.sun",
      "type": "routine", # selfimproving, etc
      "category": "I",
      "billable": true,
      "project": "",
      "info": "type=book,task=奇特的一生"
    }
  ]
}
```

*  标准Python client, 输出到Promscale, 最终落在Timescale.
*  TimeEntry和Event的区别在于value: duration和timestamp(或者其他value: 统计cold次数, pmo次数， 为int).
    +  Event的timestamp为统一时间, 保证x轴均匀分布，一天的中间? Value不同

## Monitor

*  尚不清楚是否通过Prometheus, 再到Grafana; 还是直接Grafana: 暂定, 
    +  能用Prometheus的就用PromQL, 主要学习用. 
    +  不能的直接SQL