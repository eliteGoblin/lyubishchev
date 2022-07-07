from dataclasses import dataclass
from typing import Any, List

import arrow
from arrow import Arrow

from lyubishchev.data_model.core import InvalidLabelTag, Label, Metadata
from lyubishchev.data_model.event_data import (
    EVENT_TYPE,
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

    def __init__(self, **kwargs: Any) -> None:
        self.metadata = Metadata()
        self.extra_info = ""
        self.timestamp = arrow.utcnow()

        valid_keys: List[str] = ["metadata", "extra_info", "timestamp"]
        for key in valid_keys:
            if kwargs.get(key) is not None:
                setattr(self, key, kwargs.get(key))


def validate_event_label_and_tag(label: Label) -> None:

    """
    throw InvalidLabelTag in event label and tag validation fail
    """
    if EVENT_TYPE not in label:
        raise InvalidLabelTag(f"key {EVENT_TYPE} missing in event")
    if label[EVENT_TYPE] not in VALID_TYPE:
        raise InvalidLabelTag(f"invalid type value {label[EVENT_TYPE]} in event")

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
        type_value: str = label[EVENT_TYPE]
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

        raise InvalidLabelTag(f"invalid tag value {value} for type {EVENT_TYPE}")
