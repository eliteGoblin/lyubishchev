
# Data model

*  Annotation
*  Tag
*  Name/desc不重要? 

# Project && Breakdown

*  Project支持层级: math包含LA, 概率，再各个包含子项目, 可以是读书. 因此每个节点是Tree Node? 
   *  Project tree 独立于time data之外, time entry有tag指向直接project, eg `projectID`
   *  project tree node应该关联epic.
*  工具应该与agile project management集成: zenhub, gitlab, etc. 获取more context, 目的:
   *  breakdown of time: 回答: 上周学习时间8hr, 产出是什么? 用产出倒逼输入，最高效的学习方法.
   *  Track progress of goal: burndown; velocity 相关. 

> 就拿1965年8月来说，第一类工作的总时间是136小时45分。其中有包括哪些项目呢？请看吧，一切情况在每月小结中都有说明： 合计136小时45分 ＊ 基本科研 59小时45分 ＊ 分类昆虫学 20小时55分 ＊ 附加工作 50小时25分 ＊ 组织工作： 5小时40分 基本科研又包括了什么内容： ＊ 分类工作 6小时25分 ＊ 杂事： 一小时 ＊ 校对 “达达派”研究： 30分 ＊ 数学： 16小时40分 ＊ 日常参考书： 生物学 。。。 还可以随便拿哪一项继续分析下去，如第六项： 生物学12小时： ＊ 人类的进化，372页（看完，共16小时55分）6小时45分 ＊ 动物没有思想： 91页 2小时 ＊ 贝格尔的手稿 2小时 。。。

# Measure output

*  支持不同类型project的measure方法
*  time entry annotation? 单位: pages, 
*  基本的产出衡量:
   *  read article: take notes.
   *  notes, document, blog
   *  coding: line of code.
   *  how to measure: 
      *  time entry annotation: projectID
      *  output: 每种不同的project, 不同的object schema
*  计算output时，merge同project time entry.

# Software Interface

*  逻辑不依赖与storage implementation: 提供fetch和filter接口: 根据tag/label来filter time entry
*  MVP可以把数据全部load进内存

# Integration

宗旨: 花了xx时间, 产出xx事情.

*  Github: code activity: 贡献多少代码, 什么语言.