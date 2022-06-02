
# v0.1.0 data model

Every time series is uniquely identified by its metric name and optional key-value pairs called labels.

A custom metric is identified by a unique combination of a metric’s name and tag values (including the host tag).

```json
TimeInterval {
    "metadata": {
        "version": "v0.1.0", # semver
        "annotations": {
            "key1": "value1",
            "key2": 2
        },
        "labels": {
            "key1": "value1", # label value should be strings, bool
            "key2": "value2",
            "key3": true
            "social": "" # empty value used as tag here (key only)
        }
    },
    "extraInfo": "blah",
    "timestamp": 1112233,
    "value": 15 # DurationSecs for duration; 0 for event.
}

Event {
    "metadata": {
        "version": "v0.1.0", # semver
        "annotations": {
            "key1": "value1",
            "key2": 2
        },
        "labels": {
            "key1": "value1", # label value should be strings, bool
            "key2": "value2",
            "key3": true
            "social": "" # empty value used as tag here (key only)
        }
    },
    "extraInfo": "blah",
    "timestamp": 1112233
}
```

*  Label key value 都是string, 主要用于filter
*  Annotation key为string, value可以为valid JSON value