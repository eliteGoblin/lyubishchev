

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

# 模块划分

*  数据库: 核心data model, 稳定，简洁的, 提供最基本的TSDB功能
*  Trend: 基于数据(目前基于全部数据库), 画trendline, 之后可改为基于导出数据; 
*  Report: 
  +  数据导出csv
  +  Report生成: Jupyter? or markdown?

## Monitor

*  尚不清楚是否通过Prometheus, 再到Grafana; 还是直接Grafana: 暂定, 
    +  能用Prometheus的就用PromQL, 主要学习用. 
    +  不能的直接SQL

TODO: 