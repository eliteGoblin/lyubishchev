from dataclasses import dataclass

import arrow
from arrow import Arrow

from lyubishchev.data_model.core import InvalidLabelTag, Label, Metadata
from lyubishchev.data_model.timeinterval_data import (
    PROJECT,
    TYPE,
    TYPE_DISTRACTED,
    TYPE_RELAX,
    TYPE_ROUTINE,
    TYPE_SELF_IMPROVING,
    VALID_DISTRACTED_TAGS,
    VALID_INTERVAL_TYPES,
    VALID_PROJECTS,
    VALID_RELAX_TAGS,
    VALID_ROUTINE_TAGS,
    VALID_SELF_IMPROVING_TAGS,
    VALID_TAGS,
    VALID_TIME_INTERVAL_LABEL_KEY,
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

    def __init__(self) -> None:
        self.metadata = Metadata()
        self.extra_info = ""
        self.timestamp = arrow.now()
        self.duration_minutes = 0


def validate_time_interval_label_and_tag(  # pylint: disable=too-many-branches
    label: Label,
) -> None:

    """
    throw InvalidLabelTag if TimeInterval label, tag validation fail
    """
    if TYPE not in label:
        raise InvalidLabelTag(f"key {TYPE} missing in TimeInterval")
    if label[TYPE] not in VALID_INTERVAL_TYPES:
        raise InvalidLabelTag(f"invalid type value {label[TYPE]} in TimeInterval")

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
        if label_key not in VALID_TAGS:
            raise InvalidLabelTag(f"invalid tag key {label_key}")
        # check if tag match type
        type_value: str = label[TYPE]
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
        else:
            raise InvalidLabelTag(
                f"tag {label_key} must be specified with valid type, or pls add it in data.py"
            )

        raise InvalidLabelTag(f"invalid tag value {value} for type {TYPE}")
