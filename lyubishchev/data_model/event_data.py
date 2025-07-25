from typing import List

# event means status change, e.g
#   sleep => wakeup

# each Event must has one type
EVENT_TYPE: str = "event_type"
# valid event type values
TYPE_WAKEUP = "wakeup"
TYPE_GETUP = "getup"
TYPE_BED = "bed"
TYPE_PARTNER_PERIOD = "partner_period"

TYPE_UNWELL = "unwell"
TYPE_RECOVER_UNWELL = "recover_unwell"
# type means mutual exclusive
VALID_TYPE: List[str] = [
    TYPE_WAKEUP,
    TYPE_GETUP,
    TYPE_BED,
    TYPE_PARTNER_PERIOD,
    TYPE_UNWELL,
    TYPE_RECOVER_UNWELL,
]

# Tag: key only label; provide extra info for certain Event

# Tags for type=TYPE_UNWELL or type=TYPE_RECOVER_UNWELL
TAG_COLD: str = "cold"
TAG_INJURED: str = "injured"

VALID_UNWELL_TAGS: List[str] = [
    TAG_COLD,
    # more sickness type can be added here
    TAG_INJURED,
]

# recover-unwell should have exactly same tags with unwell
VALID_RECOVER_UNWELL_TAGS: List[str] = VALID_UNWELL_TAGS


VALID_EVENT_LABEL_KEY: List[str] = [
    EVENT_TYPE,
]

VALID_EVENT_TAG_KEY: List[str] = list(set([*VALID_UNWELL_TAGS]))
