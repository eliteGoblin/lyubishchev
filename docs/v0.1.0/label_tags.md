

# label

## projectName

*  projectName 唯一识别项目
*  Naming: 小写字母结合 `-`
*  project可存储metadata, 对应如zenhub的epic. (projectName关联zenhub epic ID)

##  intervalType

*  required field
*  排他标签, 表明interval 类型
*  value只有一个(而非array), 表明一段时间只有一个基本类型(主题)

可选值: 

*  self-improving
*  work
*  routine
*  exercise
*  sex
*  meditation
*  distracted
*  relax
*  pmo
*  dispute

## Tags 

Tags = key only (value=="")

一般搭配: 

*  `intervalType==relax`, tag可以是:
   *  social: 朋友， 同事. 
   *  family: family时光，如一起dinner, talking. 
   *  intimacy: 无sex的举动
   *  recreation: 做truely happy的事: fine-dinning, walking, 音乐会等
*  `intervalType==distracted`:
   *  news
   *  porn: no m, just watching. 如果是失去控制: 连续watch, 然后m 标记为pmo.
   *  game
   *  youtube

# annotation

v0.1.0 不实现