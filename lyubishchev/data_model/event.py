from dataclasses import dataclass

import arrow
from arrow import Arrow

from lyubishchev.data_model.core import InvalidLabelTag, Label, Metadata
from lyubishchev.data_model.event_data import *


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
    throw InvalidLabelTag
    """
    # check required fields
    if TYPE not in label:
        raise InvalidLabelTag("key {key} missing".format(key=TYPE))
    if label[TYPE] not in VALID_TYPE:
        raise InvalidLabelTag("invalid type value {value}".format(value=label[TYPE]))

    # check tags
    for label_key, value in label.items():
        if value != "":
            # it's a label(not a tag): check label key is valid
            if label_key not in VALID_LABEL_KEY:
                raise InvalidLabelTag(
                    "invalid label key {key}".format(
                        key=label_key,
                    )
                )
            continue
        else:
            # if it's a tag(value empty string), check if valid tag names.
            if label_key not in VALID_TAG_KEY:
                raise InvalidLabelTag(
                    "invalid tag key {tag}".format(
                        tag=label_key,
                    )
                )
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
