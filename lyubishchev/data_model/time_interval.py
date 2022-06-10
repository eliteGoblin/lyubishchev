from dataclasses import dataclass

import arrow
from arrow import Arrow

from lyubishchev.data_model.core import InvalidLabelTag, Label, Metadata
from lyubishchev.data_model.timeinterval_data import *


@dataclass
class TimeInterval:
    """TimeInterval object is for tracking a time interval, with additional labels and annotations"""

    metadata: Metadata
    extra_info: str
    timestamp: Arrow
    duration_minutes: int

    def __init__(self) -> None:
        self.metadata = Metadata()
        self.extra_info = ""
        self.timestamp = arrow.now()
        self.duration_minutes = 0


def validate_time_interval_label_and_tag(label: Label) -> None:

    """
    throw InvalidLabelTag
    """
    # check required fields
    if TYPE not in label:
        raise InvalidLabelTag("key {key} missing".format(key=TYPE))
    if label[TYPE] not in VALID_INTERVAL_TYPES:
        raise InvalidLabelTag("invalid type value {value}".format(value=label[TYPE]))

    if PROJECT in label:
        project_value: str = label[PROJECT]
        if project_value == "" or project_value not in VALID_PROJECTS:
            raise InvalidLabelTag(
                "invalid project value {value}".format(value=project_value)
            )

    # check tags
    for label_key, value in label.items():
        if value != "":
            # it's a label(not a tag): check label key is valid
            if label_key not in VALID_TIME_INTERVAL_LABEL_KEY:
                raise InvalidLabelTag(
                    "invalid label key {key}".format(
                        key=label_key,
                    )
                )
            continue
        else:
            # if it's a tag(value empty string), check if valid tag names.
            if label_key not in VALID_TAGS:
                raise InvalidLabelTag(
                    "invalid tag key {tag}".format(
                        tag=label_key,
                    )
                )
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
                "tag {tag} must be specified with valid type, or pls add it in data.py".format(
                    tag=label_key
                )
            )

        raise InvalidLabelTag(
            "invalid tag value {value} for type {typ}".format(
                value=value,
                typ=TYPE,
            )
        )
