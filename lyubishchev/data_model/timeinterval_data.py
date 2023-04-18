from typing import List

# each TimeInterval must has one type
TIME_INTERVAL_TYPE: str = "type"
# valid type values
TYPE_CONNECTION: str = "connection"
TYPE_DISPUTE: str = "dispute"
TYPE_DISTRACTED: str = "distracted"
TYPE_EXERCISE: str = "exercise"
TYPE_MEDITATION: str = "meditation"
TYPE_NUMB: str = "numb"  # avoid feeling
TYPE_PMO: str = "pmo"
TYPE_RELAX: str = "relax"
TYPE_ROUTINE: str = "routine"
TYPE_SELF_IMPROVING: str = "self-improving"
TYPE_SEX: str = "sex"
TYPE_SLEEP: str = "sleep"
TYPE_WALK: str = "walk"
TYPE_WORK: str = "work"


VALID_INTERVAL_TYPES: List[str] = [
    TYPE_CONNECTION,
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
    TYPE_WALK,
    TYPE_WORK,
    TYPE_NUMB,
]

# Tag: key only label; provide extra info for certain TimeInterval Types

# Tags for type=distracted
TAG_GAME: str = "game"
TAG_NEWS: str = "news"
TAG_PORN: str = "porn"
TAG_YOUTUBE: str = "youtube"

VALID_DISTRACTED_TAGS: List[str] = [TAG_GAME, TAG_NEWS, TAG_PORN, TAG_YOUTUBE]

# Tags for type=routine
# TAG_KITCHEN means time spent in kitchen, cook, clean etc
TAG_KITCHEN: str = "kitchen"
TAG_HOUSEWORK: str = "housework"

VALID_ROUTINE_TAGS: List[str] = [TAG_KITCHEN, TAG_HOUSEWORK]

# Tags for type=self-improving
# TAG_READING apply to:
#   Kindle, non-CS good book
#   Articles, blogs
TAG_READING: str = "reading"
# TAG_DEEP_LEARNING can apply to:
#   Hard subject like math, or
#   Actively learning: OJ, output notes, blogs, demo projects; distinguish of plain reading
TAG_DEEP_LEARNING: str = "deep-learning"
TAG_REVIEW: str = "review"  # review, plan
VALID_SELF_IMPROVING_TAGS: List[str] = [TAG_READING, TAG_DEEP_LEARNING, TAG_REVIEW]

# Tags for type=relax
TAG_FAMILY: str = "family"
TAG_HAPPY: str = "happy"
TAG_INTIMACY: str = "intimacy"
TAG_SOCIAL: str = "social"

VALID_RELAX_TAGS: List[str] = [
    TAG_FAMILY,
    TAG_HAPPY,
    TAG_INTIMACY,
    TAG_SOCIAL,
    TAG_READING,  # reading could be either relax or self-improving; so valid for both types
]

TAG_CODING: str = "coding"  # coding, creative work
TAG_DEVOPS: str = "devops"  # architecture, automation, operation, configuration
TAG_COLLABORATION: str = "collaboration"  # discuss requirements, brainstorming, pair
TAG_HELP: str = "help_other"  # help, coach
VALID_WORK_TAGS: list[str] = [
    TAG_CODING,
    TAG_DEVOPS,
    TAG_COLLABORATION,
    TAG_HELP,
    TAG_SOCIAL,
]

# Tags for sex
TAG_MASTERBATE: str = "masterbate"
VALID_SEX_TAGS: List[str] = [TAG_MASTERBATE]

VALID_TIME_INTERVAL_TAGS: List[str] = list(
    set(
        [  # remove potential duplicate tags from types, e.g reading
            *VALID_RELAX_TAGS,
            *VALID_ROUTINE_TAGS,
            *VALID_DISTRACTED_TAGS,
            *VALID_SELF_IMPROVING_TAGS,
            *VALID_SEX_TAGS,
        ]
    )
)

VALID_TIME_INTERVAL_LABEL_KEY: List[str] = [TIME_INTERVAL_TYPE]
