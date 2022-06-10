# Event label

## type 

* wakeup: 已清醒, 不准备睡的时刻
* getup: 起床时间
* gobed: 准备入睡时间
* unwell: 身体不适导致状态下降
  * tag: cold
  * tag: injured
* recover-unwell: same tag from unwell; tag needs to match as a pair: unwell => recover


Note:

*  实现时可借助clockify wakeup 的duration: wakeup + duration = getup time.

## Implementation notes

Diff compared to TimeInterval:

* No duration field

## Self Validation

*  label TYPE is mandatory
*  validate label type's value