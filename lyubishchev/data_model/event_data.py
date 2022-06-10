from typing import List

# each Event must has one type
TYPE: str = "type"
# valid event type values
TYPE_WAKEUP = "wakeup"
TYPE_GETUP = "getup"
TYPE_GOBED = "gobed"
TYPE_UNWELL = "unwell"
TYPE_RECOVER_UNWELL = "recover-unwell"

# type means mutual exclusive
VALID_TYPE: List[str] = [
    TYPE_WAKEUP,
    TYPE_GETUP,
    TYPE_GOBED,
    TYPE_UNWELL,
    TYPE_RECOVER_UNWELL,
]

# Tag: key only label; provide extra info for certain Event

# Tags for type=TYPE_UNWELL or type=TYPE_RECOVER_UNWELL
TAG_COLD: str = "cold"
TAG_INJURED: str = "injured"

VALID_UNWELL_TAGS: List[str] = [
    TAG_COLD,
    TAG_INJURED,
]

# recover-unwell should have exactly same tags with unwell
VALID_RECOVER_UNWELL_TAGS: List[str] = VALID_UNWELL_TAGS


VALID_LABEL_KEY: List[str] = [
    TYPE,
]

VALID_TAG_KEY: List[str] = [*VALID_UNWELL_TAGS]
