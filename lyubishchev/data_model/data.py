from typing import Dict, List, Union

Annotation = Dict[str, Union[str, int, float]]
Label = Dict[str, str]

# TimeInterval

# TODO: hardcode project value as temporary solution
PROJECT: str = "project"
PROJECT_ENGINEERING: str = "engineering"
PROJECT_COMPUTER_VISION = "computer_vision"
PROJECT_MATH = "math"
PROJECT_USEFUL_READING = "useful_reading"

# each TimeInterval must has one type
TYPE: str = "type"
# valid type values
TYPE_DISPUTE: str = "dispute"
TYPE_DISTRACTED: str = "distracted"
TYPE_EXERCISE: str = "exercise"
TYPE_MEDITATION: str = "meditation"
TYPE_PMO: str = "pmo"
TYPE_RELAX: str = "relax"
TYPE_ROUTINE: str = "routine"
TYPE_SELF_IMPROVING: str = "self-improving"
TYPE_SEX: str = "sex"
TYPE_SLEEP: str = "sleep"
TYPE_WORK: str = "work"

VALID_INTERVAL_TYPES: List[str] = [
    TYPE_DISPUTE,
    TYPE_DISTRACTED,
    TYPE_EXERCISE,
    TYPE_MEDITATION,
    TYPE_PMO,
    TYPE_RELAX,
    TYPE_ROUTINE,
    TYPE_SELF_IMPROVING,
    TYPE_SEX,
    TYPE_SLEEP,
    TYPE_WORK,
]

# Tag: key only label; provide extra info for certain TimeInterval Types
TAG_FAMILY: str = "family"
TAG_HAPPY: str = "happy"
TAG_INTIMACY: str = "intimacy"
TAG_SOCIAL: str = "social"

VALID_RELAX_TAGS: List[str] = [TAG_FAMILY, TAG_HAPPY, TAG_INTIMACY, TAG_SOCIAL]

TAG_GAME: str = "game"
TAG_NEWS: str = "news"
TAG_PORN: str = "porn"
TAG_YOUTUBE: str = "youtube"

VALID_DISTRACTED_TAGS: List[str] = [TAG_GAME, TAG_NEWS, TAG_PORN, TAG_YOUTUBE]

TAG_COOK: str = "cook"
TAG_HOUSEWORK: str = "housework"

VALID_ROUTINE_TAGS: List[str] = [TAG_COOK, TAG_HOUSEWORK]

TAG_DEEP_LEARNING: str = "deep_learning"
VALID_SELF_IMPROVING_TAGS: List[str] = [TAG_DEEP_LEARNING]

VALID_TAGS: List[str] = [
    *VALID_RELAX_TAGS,
    *VALID_ROUTINE_TAGS,
    *VALID_DISTRACTED_TAGS,
    *VALID_SELF_IMPROVING_TAGS,
]

VALID_TIME_INTERVAL_LABEL_KEY: List[str] = [PROJECT, TYPE]
