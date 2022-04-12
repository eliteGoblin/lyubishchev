
# DB time

> For timestamp with time zone, the internally stored value is always in UTC (Universal Coordinated Time, traditionally known as Greenwich Mean Time, GMT). An input value that has an explicit time zone specified is converted to UTC using the appropriate offset for that time zone. If no time zone is stated in the input string, then it is assumed to be in the time zone indicated by the system's timezone parameter, and is converted to UTC using the offset for the timezone zone.
When a timestamp with time zone value is output, it is always converted from UTC to the current timezone zone, and displayed as local time in that zone. To see the time in another time zone, either change timezone or use the AT TIME ZONE construct (see Section 9.9.3).

*  DB内部计算，存储全部是UTC
*  DB输入，输出: 需要额外的local timezone信息(没有则用系统默认)
*  输入: 根据输入时区, 转化为UTC
*  输出: DB将UTC转化为local zone: 等于省的自己转换了

[8.5. Date/Time Types](https://www.postgresql.org/docs/9.1/datatype-datetime.html)  

# lyubishchev

*  内部采用UTC
*  默认采用系统时间, 即Local zone, 不用管AEST, AEDT, etc.