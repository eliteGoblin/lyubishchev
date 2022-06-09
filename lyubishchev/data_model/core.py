from dataclasses import dataclass

from lyubishchev.data_model.data import *


class InvalidLabelTag(Exception):
    """Exception raised when missing required labels, invalid label or label and tag not matching the"""

    pass


@dataclass
class Metadata:
    version: str  # semver, e.g v0.1.0
    annotation: Annotation
    label: Label

    def __init__(self) -> None:
        self.version = ""
        self.annotation = {}
        self.label = {}

    def validate(self) -> None:
        """
        throw InvalidLabelTag
        """
        raise NotImplementedError("not implemented!")


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
        if value != "":  # it's a label, not a tag
            if label_key not in VALID_TIME_INTERVAL_LABEL_KEY:
                raise InvalidLabelTag(
                    "invalid label key {key}".format(
                        key=label_key,
                    )
                )
            continue
        else:  # tag is valueless(empty string) label
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
