# FAQ

## Q: How user rename a tag? 

Tag属于business logic的一部分; storage implementation应该依赖于business logic.

Model层只关心string tag. Model不关心数据持久化的事情， 只管拿到数据. 

存储时可借助内部TagID对应TagName. 

## Naming convention

* Naming: 小写字母结合 `-`

## How to version control

* 采用Metadata version
* 增加新字段: +1 minor
* Breaking change: +1 major

# label

## projectName

*  Optional
*  projectName 唯一识别项目
*  project可存储metadata, 对应如zenhub的epic. (projectName关联zenhub epic ID)

##  Type

*  required field
*  排他标签, 表明interval 类型
*  value只有一个(而非array), 表明一段时间只有一个基本类型(主题)

可选值: 

*  dispute
*  distracted
*  exercise
*  meditation
*  pmo
*  relax
*  routine
*  self-improving
*  sex
*  sleep: 包括日间nap, 和夜晚sleep
*  work
## Tags 

Tags = key only (value=="")

### 搭配intervalType, 提供extra info的

* `intervalType==relax`, tag可以是:
   *  social: 朋友， 同事. 
   *  family: family时光，如一起dinner, talking. 
   *  intimacy: 无sex的举动
   *  happy: 做truely happy的事: fine-dinning, walking, 音乐会等
* `intervalType==distracted`:
   * news
   * porn: no m, just watching. 如果是失去控制: 连续watch, 然后m 标记为pmo.
   * game
   * youtube
* `intervalType==routine`:
  * cook
  * housework
* `interval_type==self-improving`:
  * deep: math, computer vision

# annotation

v0.1.0 不实现


# Design


# 如何validate schema

*  Option 1: JSON schema


## Option 2: 自己实现: 方便定制化规则

Tag name是business logic的一部分. 

Tag用const表示, support检查storage tag和business code定义的tag是否一致.  确保Business code tag 集合包含storage backend的. 


# Task

1.  support检查storage tag和business code定义的tag是否一致 