from typing import Any

from lyubishchev.data_model.time_interval import TimeInterval
from lyubishchev.report.constants import (
    CALM,
    EFFECTIVE_OUTPUT,
    EXERCISE,
    INTANGIGLE,
    OTHER,
    REGRET,
    ROUTINE_ALL,
    SELF_IMPROVING,
    SELF_IMPROVING_NONTECH,
    SELF_IMPROVING_TECH,
    SEX_ALL,
    SOLITUDE,
    WORK_ALL,
)
from lyubishchev.report.report import get_match_dict
from lyubishchev.report.report_utils import prune_dict, sum_dict_values
from lyubishchev.search import Match


def aggregate_time_interval_by_label_minutes(
    time_intervals: list[TimeInterval], labels: list[str]
) -> dict[str, int]:
    """
    Aggregate duration for each label
    Args:
        labels: real labels for aggregate duration in minutes, e.g for work_all ["work", "job"]

    Returns:
        {
            "work": 12,
            "job": 5,
        }
    """
    res = {}
    for label in labels:
        res[label] = sum(
            time_interval.duration_minutes
            for time_interval in Match.from_dict({label: None}).match(time_intervals)
        )
    return res


def get_time_interval_aggregation_dict_tree(
    total_time_minutes: int,
    time_intervals: list[TimeInterval],
) -> dict[str, Any]:
    """
    Aggregate time intervals by labels and return a dict tree,
        where each leaf node is a label and value is a duration in minutes
        Non leaf node means "virtual label"(e.g. "self_improving", just to group and tree structure real labels)
    Args:
        total_time_minutes: used for "other" label, to see how much time is not covered by recorded time intervals
        time_intervals: list of time intervals to aggregate
    Return:
    Hierarchy of effective_output:
    {
        "calm": {
            "walk": 10,
            "meditation": 20,
        },
        "effective_output": {
            "self_improving": {
                "tech": {
                    "lyubishchev": 3,
                    "oj": 4,
                    "software": 5,
                },
                "non_tech": {
                    "bibliotherapy": 1,
                    "linkedin": 2,
                    "audible": 6,
                }
            },
            "work_all": {
                "work": 55,
                "job": 9,
            },
        },
        "exercise": {
            "swim": 20,
            "job": 10,
        },
        "intangible": {
            "lisha": 30,
        } ,
        "regret": {
            "internet": 30,
        },
        "routine_all": {
            "self_routine": 80,
            "housework": 20,
        },
        "solitude": {
            "novel": 30,
        },
        "sex_all": {
            "sex": 34,
        },
        "other": 90,
    }
    """

    res = {
        CALM: aggregate_time_interval_by_label_minutes(
            time_intervals=time_intervals, labels=list(get_match_dict(CALM).keys())
        ),
        EFFECTIVE_OUTPUT: {
            SELF_IMPROVING: {
                SELF_IMPROVING_TECH: aggregate_time_interval_by_label_minutes(
                    time_intervals=time_intervals,
                    labels=list(get_match_dict(SELF_IMPROVING_TECH).keys()),
                ),
                SELF_IMPROVING_NONTECH: aggregate_time_interval_by_label_minutes(
                    time_intervals=time_intervals,
                    labels=list(get_match_dict(SELF_IMPROVING_NONTECH).keys()),
                ),
            },
            WORK_ALL: aggregate_time_interval_by_label_minutes(
                time_intervals=time_intervals,
                labels=list(get_match_dict(WORK_ALL).keys()),
            ),
        },
        EXERCISE: aggregate_time_interval_by_label_minutes(
            time_intervals=time_intervals,
            labels=list(get_match_dict(EXERCISE).keys()),
        ),
        INTANGIGLE: aggregate_time_interval_by_label_minutes(
            time_intervals=time_intervals,
            labels=list(get_match_dict(INTANGIGLE).keys()),
        ),
        REGRET: aggregate_time_interval_by_label_minutes(
            time_intervals=time_intervals,
            labels=list(get_match_dict(REGRET).keys()),
        ),
        ROUTINE_ALL: aggregate_time_interval_by_label_minutes(
            time_intervals=time_intervals,
            labels=list(get_match_dict(ROUTINE_ALL).keys()),
        ),
        SEX_ALL: aggregate_time_interval_by_label_minutes(
            time_intervals=time_intervals,
            labels=list(get_match_dict(SEX_ALL).keys()),
        ),
        SOLITUDE: aggregate_time_interval_by_label_minutes(
            time_intervals=time_intervals,
            labels=list(get_match_dict(SOLITUDE).keys()),
        ),
    }
    res[OTHER] = total_time_minutes - sum_dict_values(res)
    # clean up: remove empty dict and 0 values
    prune_dict(res)
    return res
