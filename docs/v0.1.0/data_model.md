
# v0.1.0 data model

Every time series is uniquely identified by its metric name and optional key-value pairs called labels.

A custom metric is identified by a unique combination of a metric’s name and tag values (including the host tag).

```json
TimeEntry {
    "metadata": {
        "version": "v0.1.0", # semver
        "entryType": "duration", # duration or event
        "annotations": {
            "key1": "value1",
            "key2": 2
        },
        "labels": {
            "key1": "value1", # label value should be strings, bool
            "key2": "value2",
            "key3": true
        }
    },
    "extraInfo": "blah",
    "timestamp": 1112233,
    "value": 15 # DurationSecs for duration; 0 for duration.
}
```

# annotation && label design

*  Annotation for extra data; labels for filtering.

For duration type: 

## label

*  `project` string
*  `isEffective` boolean：对应柳牛的有效时间
*  `durationType`: string
   *  dispute
   *  distracted
   *  exercise
   *  family
   *  meditation
   *  pmo
   *  relax
   *  routine: necessary things for living
   *  selfImprovement
   *  sex: tag together with family?
   *  social
   *  work
