from dataclasses import dataclass
from typing import Any, List

import arrow
from arrow import Arrow

from lyubishchev.data_model.core_data_structure import InvalidLabelTag, Label, Metadata
from lyubishchev.data_model.timeinterval_data import (
    PROJECT,
    TIME_INTERVAL_TYPE,
    TYPE_DISTRACTED,
    TYPE_RELAX,
    TYPE_ROUTINE,
    TYPE_SELF_IMPROVING,
    TYPE_WORK,
    VALID_DISTRACTED_TAGS,
    VALID_INTERVAL_TYPES,
    VALID_PROJECTS,
    VALID_RELAX_TAGS,
    VALID_ROUTINE_TAGS,
    VALID_SELF_IMPROVING_TAGS,
    VALID_TIME_INTERVAL_LABEL_KEY,
    VALID_TIME_INTERVAL_TAGS,
    VALID_WORK_TAGS,
)


@dataclass
class TimeInterval:
    """
    TimeInterval object is for tracking a time interval,
    with additional labels and annotations
    """

    metadata: Metadata
    extra_info: str
    timestamp: Arrow
    duration_minutes: int

    def __init__(self, **kwargs: Any) -> None:
        self.metadata = Metadata()
        self.extra_info = ""
        self.timestamp = arrow.utcnow()
        self.duration_minutes = 0

        valid_keys: List[str] = [
            "metadata",
            "extra_info",
            "timestamp",
            "duration_minutes",
        ]
        for key in valid_keys:
            if kwargs.get(key) is not None:
                setattr(self, key, kwargs.get(key))


def validate_time_interval_label_and_tag(  # pylint: disable=too-many-branches
    label: Label,
) -> None:

    """
    throw InvalidLabelTag if TimeInterval label, tag validation fail
    """
    if TIME_INTERVAL_TYPE not in label:
        raise InvalidLabelTag(f"key {TIME_INTERVAL_TYPE} missing in TimeInterval")
    if label[TIME_INTERVAL_TYPE] not in VALID_INTERVAL_TYPES:
        raise InvalidLabelTag(
            f"invalid type value {label[TIME_INTERVAL_TYPE]} in TimeInterval"
        )

    if PROJECT in label:
        project_value: str = label[PROJECT]
        if project_value == "" or project_value not in VALID_PROJECTS:
            raise InvalidLabelTag(f"invalid project value {project_value}")

    # check tags
    for label_key, value in label.items():
        if value != "":
            # it's a label(not a tag): check label key is valid
            if label_key not in VALID_TIME_INTERVAL_LABEL_KEY:
                raise InvalidLabelTag(f"invalid label key {label_key}")
            continue
        # if it's a tag(value empty string), check if valid tag names.
        if label_key not in VALID_TIME_INTERVAL_TAGS:
            raise InvalidLabelTag(f"invalid tag key {label_key}")
        # check if tag match type
        type_value: str = label[TIME_INTERVAL_TYPE]
        if type_value == TYPE_RELAX:
            if label_key in VALID_RELAX_TAGS:
                continue
        elif type_value == TYPE_DISTRACTED:
            if label_key in VALID_DISTRACTED_TAGS:
                continue
        elif type_value == TYPE_ROUTINE:
            if label_key in VALID_ROUTINE_TAGS:
                continue
        elif type_value == TYPE_SELF_IMPROVING:
            if label_key in VALID_SELF_IMPROVING_TAGS:
                continue
        elif type_value == TYPE_WORK:
            if label_key in VALID_WORK_TAGS:
                continue
        else:
            raise InvalidLabelTag(
                f"tag {label_key} must be specified with valid type, or pls add it in timeinterval_data.py"
            )

        raise InvalidLabelTag(
            f"invalid tag value {value} for type {TIME_INTERVAL_TYPE}"
        )
