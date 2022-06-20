from typing import List

# PROJECT is for measuring output, similar to EPIC, and better to link with one
PROJECT: str = "project"
# PROJECT_ENGINEERING includes all efforts devoted to improve programing skills:
#  architecting, monitoring
#  coding, language
PROJECT_SOFTWARE_ENGINEERING: str = "software-engineering"
PROJECT_COMPUTER_VISION = "computer-vision"
PROJECT_MATH = "math"
PROJECT_GIS = "gis"

# hard code valid projects for now, later we could link it to EPIC
VALID_PROJECTS: List[str] = [
    PROJECT_SOFTWARE_ENGINEERING,
    PROJECT_COMPUTER_VISION,
    PROJECT_MATH,
    PROJECT_GIS,
]

# each TimeInterval must has one type
TIME_INTERVAL_TYPE: str = "type"
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

# Tags for type=relax
TAG_FAMILY: str = "family"
TAG_HAPPY: str = "happy"
TAG_INTIMACY: str = "intimacy"
TAG_SOCIAL: str = "social"
TAG_YOUTUBE: str = "youtube"

VALID_RELAX_TAGS: List[str] = [
    TAG_FAMILY,
    TAG_HAPPY,
    TAG_INTIMACY,
    TAG_SOCIAL,
    TAG_YOUTUBE,
]

# Tags for type=distracted
TAG_GAME: str = "game"
TAG_NEWS: str = "news"
TAG_PORN: str = "porn"

VALID_DISTRACTED_TAGS: List[str] = [TAG_GAME, TAG_NEWS, TAG_PORN, TAG_YOUTUBE]

# Tags for type=routine
# TAG_KITCHEN means time spent in kitchen, cook, clean etc
TAG_KITCHEN: str = "kitchen"
TAG_HOUSEWORK: str = "housework"

VALID_ROUTINE_TAGS: List[str] = [TAG_KITCHEN, TAG_HOUSEWORK]

# Tags for type=self-improving
# TAG_DEEP_LEARNING can apply to:
#   Hard subject like math, or
#   Actively learning: OJ, output notes, blogs, demo projects; distinguish of plain reading
TAG_DEEP_LEARNING: str = "deep-learning"
TAG_REVIEW: str = "review"  # review, plan
VALID_SELF_IMPROVING_TAGS: List[str] = [TAG_DEEP_LEARNING, TAG_REVIEW]

VALID_TAGS: List[str] = [
    *VALID_RELAX_TAGS,
    *VALID_ROUTINE_TAGS,
    *VALID_DISTRACTED_TAGS,
    *VALID_SELF_IMPROVING_TAGS,
]

VALID_TIME_INTERVAL_LABEL_KEY: List[str] = [PROJECT, TIME_INTERVAL_TYPE]
