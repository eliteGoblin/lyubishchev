from dataclasses import dataclass

import arrow
from arrow import Arrow

from lyubishchev.data_model.core import InvalidLabelTag, Label, Metadata
from lyubishchev.data_model.event_data import (
    TYPE,
    TYPE_RECOVER_UNWELL,
    TYPE_UNWELL,
    VALID_LABEL_KEY,
    VALID_RECOVER_UNWELL_TAGS,
    VALID_TAG_KEY,
    VALID_TYPE,
    VALID_UNWELL_TAGS,
)


@dataclass
class Event:
    """Event object is for tracking a one-off event, with additional labels and annotations"""

    metadata: Metadata
    extra_info: str
    timestamp: Arrow

    def __init__(self) -> None:
        self.metadata = Metadata()
        self.extra_info = ""
        self.timestamp = arrow.now()
        self.duration_minutes = 0


def validate_event_label_and_tag(label: Label) -> None:

    """
    throw InvalidLabelTag in event label and tag validation fail
    """
    if TYPE not in label:
        raise InvalidLabelTag(f"key {TYPE} missing in event")
    if label[TYPE] not in VALID_TYPE:
        raise InvalidLabelTag(f"invalid type value {label[TYPE]} in event")

    # check tags
    for label_key, value in label.items():
        if value != "":
            # it's a label(not a tag): check label key is valid
            if label_key not in VALID_LABEL_KEY:
                raise InvalidLabelTag(f"invalid label key {label_key}")
            continue
        # if it's a tag(value empty string), check if valid tag names.
        if label_key not in VALID_TAG_KEY:
            raise InvalidLabelTag(f"invalid tag key {label_key}")
        # check if tag match type
        type_value: str = label[TYPE]
        if type_value == TYPE_UNWELL:
            if label_key in VALID_UNWELL_TAGS:
                continue
        elif type_value == TYPE_RECOVER_UNWELL:
            if label_key in VALID_RECOVER_UNWELL_TAGS:
                continue
        else:
            raise InvalidLabelTag(
                f"tag {label_key} must be specified with valid event type"
            )

        raise InvalidLabelTag(f"invalid tag value {value} for type {TYPE}")
