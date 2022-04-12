
# 新的 MVP

*  每周Review: 数据总结
*  export as lib: 外部生成周报, 月报. 
*  先不必考虑持久化: cache是优化,可单独加一层, 每次手动抓取全量数据. 


# Archived

基于同一的model: 

*  任意时间段 trend lines, 大致数据
  +  最近表现怎么样
  +  和之前相比怎么样
  +  Lines: 
    +  getup/sleep
    +  time duration

*  生成任意时间段: detailed breakdown report: 
  +  以周/月/年单位review
  +  重复各类都花了多少时间? 有overlap也无所谓.
  +  各时间都干了什么

NEXT: 

*  大方向: 优化当前的weekly review; 同时iterate新的架构. refactor.

*  数据质检: 定期运行: 有问题马上提示? 
*  数据提取,存储: filter: 用Postgres/Timescale; 
  +  持久化为本地数据, cache
  +  提供TSDB的基本功能, 很多通过SQL能完成
*  数据导出: 导出为csv, 数据点
  +  单独模块: 基于数据库，想导出什么导出什么: 如getup time.
  +  每一个导出csv都可以是单独的模块
*  Python: visualization: 定制xy, 输出图片; markdown 或者jupyter: 配合导出的数据 
  +  单独模块: 周/月/年总结统一为一个模板
  +  基于输入的数据, 生成report, check in to github.

思考: 

*  Trend和Report: 两者冲突吗? 能否用Report代替Trend?
*  Report显然更灵活: 比如当前相比过去20 month moving avg.

分治法: 分离`trend`和`review report`功能
*  Grafana trend line不要改: 或者暂时没必要
  +  增加getup, sleep; 
  +  解决数据持久化问题 or 
    +  解决从头开始导入数据? 
*  `Review report`: 

痛点: 
*  数据问题, 频繁导入失败的多: validation规则一直在变
*  无法轻易修改数据: 只能删除重新导入
*  本质是规则和数据record的匹配: validation规则改变，导致之前的数据无法过validation.

暂定还是删除所有+

## info

*  编一个辅助info desc生成器: 本地填表: 辅助生成info desc: 模板
  +  模板版本号: parser必须兼容; 
  +  编程: xx小时, xx行code, type infra
  +  跑步: xx小时, xx miles
*  模板支持汇总: 
  +  分散的项目, 比如
    +  看书: 今天1.3hr, 50-70 page; 昨天1.2hr, 20-40pages, 两天汇总为: 2.5hr, 40pages or chapter? 分解为子问题
    +  跑步: 统计xx miles

## Report

月度report: 

```
就拿1965年8月来说，第一类工作的总时间是136小时45分。其中有包括哪些项目呢？请看吧，一切情况在每月小结中都有说明： 合计136小时45分
＊  基本科研 59小时45分
＊  分类昆虫学 20小时55分
＊  附加工作 50小时25分
＊  组织工作： 5小时40分
基本科研又包括了什么内容： 
＊  分类工作 6小时25分
＊  杂事： 一小时
＊  校对 “达达派”研究： 30分
＊  数学： 16小时40分
＊  日常参考书： 生物学
。。。
还可以随便拿哪一项继续分析下去，如第六项： 生物学12小时：
＊  人类的进化，372页（看完，共16小时55分）6小时45分
＊  动物没有思想： 91页 2小时
＊  贝格尔的手稿 2小时
```

> 这些总结要用多少时间？详细的每月小结要耗费1.5到3个小时，统共菜这些。再加上制定下个月的计划用1小时。合计是2.5到4个小时，而每个月的预算又300小时。1%， 至多2%。因为每月小结是依据每日的记录，而每日的记录只用几分钟，不会更多。仿佛是那么轻巧容易，谁能这样班都可以办到。。。几乎是习惯成自然了－－像给表上弦一样。
年度总结耗费的时间要多一些：十七八个小时，也就是说：要花几天的功夫。作年度总结，要求进行自我分析，自我研究：效率有什么变化，什么没有完成，为什么。。。

## General ideas

*  如何审计: 花了多少时间在哪个project, 产出是多少, 生成另外report? 可以, 
  +  其实关键，最需要看到的是report => 
    +  目前: 半自动: grafana监控: 粘贴数据. 
    +  最终目标, 自动生成review report, 不必人工去改(用pyplot)
    +  本质是在挖掘自己的数据: 用pyplot似乎更合适点;
  +  Monitoring可以每天一看, report以周，月，季度为单位, 详细列出花了多少时间，产出了多少事项. 
*  以Timescale为核心，formalize time series data: 根据时间范围，取出自己的data model

*  增加个人日记: 存在另一个数据库表中: 学习曾国藩review, daily review?

*  Enable draw trend lines with selected date range
*  Key metrics:
    +  Sleep time/wakeup time trend
    +  Billable trend
    +  Sports trend
    +  Routine daily
*  Atm: a complement to Clockify tool, replace it gradually
*  Don't think too much, over complicated; breakdown 
*  Explore how to manage different release using Zenhub
*  No need to store it in MVP

## 如何衡量产出

*  代码: 代码行数
*  读书: 不同类别, 书目， 页数  

## MVP v0.1.0 


