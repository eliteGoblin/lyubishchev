
# MVP

*  版本号: 0.1.0
*  仅包含最基础, 核心的功能，数据结构; 
*  原则: Most simple and stupid solution, focus自己的需求; 不要顺便加上不相干的需求: 如学习Prometheus, TimescaleDB, etc.

## Background

Purpose: 统计个人时间利用, 分类; 及时间产出;

*  Customer: only me
*  Audience: developer(me)

How it works: 
1.  Frank通过某种Interface记录时间, 存储. 
1.  Frank运行本分析工具, 得出时间分析报告. 

Running on Python3.

## Definition

*  Project: where each atomic work belong, 对应于Kanban中的Epic.
*  Billable: 根据自己的life ultimate goal, 提升自己的时间: 即是否在学习
   *  被动学习: 读书
   *  主动学习: blog, 练习demo, take notes.

## Use case

*  Frank记录时间, 通过某个interface.
*  Frank用工具分析时间记录, 得出一系列指标/信息, 粒度为一天

### Record

Frank可以为time entry 加入不同的label, 表明time entry属性: 

*  区分属于哪个project, 支持工作的project; ProjectID? 可以先手动hardcode project metadata, 如关联zenhub的哪个epic.
*  为什么要有project而不是像其他label:  
   *  Project需支持层级关系
   *  Project需要关联更多的metadata: 如zenhub epic, 以取得进一步信息. 
   *  Project需要衡量output: 产出的信息, 可以从别处取得: something worth measure output => create a project for it

Time entry type: 

类型排他标签, 只能有一种类型

*  区分是否是有效个人主动学习时间: self-improvement
*  区分是否是在工作
*  区分是否是routine: 维持day to day life, 基本需要.
*  区分exercise time
*  区分sex
*  区分meditation time
*  区分distracted time
*  区分是否是relax
*  区分PMO: 真正有m才算
*  区分Dispute
*  Support附加额外信息, 如何relax, 可以是: 聊天, walk, shopping, 
   *  是否区分让自己truely happy的?  tag recreation.
   *  感觉去circular quay, bondi walk 和 去逛Chinatown不是一个级别的, 如何区分. 用额外的tag. 见`Extra Type`

Extra Type:
比如relax可以标记为: 
*  Social
*  Family
*  Intimacy(without sex)
*  Recreation: 让自己truely happy的事情
*  并不是严格层级的结构: 比如work也可以标记为`social`
Distracted可标记为:
*  News
*  Porn
*  Game
*  Youtube

? tag可以是松散的? 比如只有tag key, 还是严格定义 key=value.  允许仅定义tag key(等同于miss tag value, treat like empty string""?)

### Event

除了Time Duration, 应支持event, 即没有duration, one-off事件: 

*  起床，睡觉timestamp.
*  Happiness metric: (也可以用tag实现 happy1, happy2 happy3, etc.?)
*  吃饭吃了100g protein.? 将来再说

### 基本Summary: 

Time investment: 

*  Project时间分配
*  billable比例: 相当于柳牛的"有效时间": 
> 柳比歇夫非常有兴致统计自己每日时间清单里真正用于工作的有效时间长度，这是从3个半小时到5个半小时之间浮动的一个值。柳比歇夫发现，即便是自己这样珍惜和擅长利用时间的人，能够做出如此高产成果的人，每天用于有效工作的时间也很难超过5小时
> 了不起！每天有5小时13分钟搞纯学术工作，天天如此。整整一年没有休假，没有节假日！5小时的纯工作时间，这可是一个客观的数字。
*  Exercise time
*  Sex duration
*  Social time
*  Recreation/relax time

参考:   
pie chart.   
<img src="https://raw.githubusercontent.com/eliteGoblin/images/master/blog/img/picgo/20220531192958.png" alt="20220531192958" style="width:500px"/> 

柱状图

<img src="https://raw.githubusercontent.com/eliteGoblin/images/master/blog/img/picgo/20220531192932.png" alt="20220531192932" style="width:500px"/>    

柳比歇夫sample:   
<img src="https://raw.githubusercontent.com/eliteGoblin/images/master/blog/img/picgo/20220531211100.png" alt="20220531211100" style="width:500px"/>


### 状态指标曲线图

*  每日起床时刻，睡觉时刻曲线
*  每日睡眠时长曲线
*  每日Billable曲线
*  每日运动
*  每日relax, recreation time.

### Time

*  End User: 可以设置local time, 比如设置时区，展示给用户的是本地时间, 当前为悉尼时间. 
*  Debug: 是否中间也显示 local time? 

# Ref

*  [Weekly Review Template](./weekly_review.md)
*  [Your 2022 Guide to Writing a Software Requirements Specification (SRS) Document](https://relevant.software/blog/software-requirements-specification-srs-document/)  