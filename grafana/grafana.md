
## Config

*  Host: `timescaledb:5432`
*  Database: `postgres`
*  User/Pass: `postgres`, `password`

## Data model

每个数据点2 fields:

*  time
*  value

用TimescaleDB时先验证数据点: 

```sql
SELECT time_bucket('1 day', event_log.time) AS "time",
sum(value)
FROM event_log 
GROUP BY 1
ORDER BY 1;
```

Note:

*  Grafana需要列名为`time`, 与event_log的`time`重叠(由`Promscale`自动生成); 如果 `GROUP BY time`还是以 `event_log.time`来group, 由于每个timestamp都不一样，相当于没有group; 因此以column index来group.

## Filter by tags

```sql
WITH label_detail_table AS (
    SELECT time, value, jsonb(labels) AS label_detail from event_log
)
SELECT time_bucket('1 day', time) AS "time", sum(value) as routine_sum
FROM label_detail_table
WHERE
    label_detail_table.label_detail->>'type' = 'routine'
GROUP BY 1
ORDER BY 1;
```

增加time filter where 语句`$__timeFilter("time")`

### Time Series


```sql
# fill gap with timerange
WITH label_detail_table AS (
    SELECT time AT TIME ZONE 'AEST' AS "time", value, jsonb(labels) AS label_detail from event_log
)
SELECT
 time_bucket_gapfill('1 day', time, $__timeFrom(), $__timeTo()) AS "time",
 COALESCE(sum(value), 0) as sum_work
FROM label_detail_table
WHERE
    label_detail_table.label_detail->>'type' = 'work' AND
    $__timeFilter("time")
GROUP BY 1
ORDER BY 1;
```

### Single Stat

```sql
WITH label_detail_table AS (
    SELECT time AT TIME ZONE 'AEST' AS "time", value, jsonb(labels) AS label_detail from event_log
)
SELECT
 time AS "time",
 COALESCE(value, 0) as value
FROM label_detail_table
WHERE
    label_detail_table.label_detail->>'type' = 'work' AND
    $__timeFilter("time")
ORDER BY 1;
```

## Ref

[PostgreSQL data source](https://grafana.com/docs/grafana/latest/datasources/postgres/)


