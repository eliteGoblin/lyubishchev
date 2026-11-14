# Core Data Model

## Two Concepts: Labels + Annotations

| Concept | Type | Purpose | Queryable |
|---|---|---|---|
| **Labels** | `dict[str, str]` | What you did + context about it | Yes — filter, match, categorize |
| **Annotations** | `dict[str, str]` | Supplementary info | No — display only |

## Labels: Unified Metadata

A label is a key-value pair. A **tag** is a label where value is empty (`""`). Both live in the same dict.

```
{"jog": ""}                          ← tag: what you did
{"work": "cba"}                      ← label: what you did + specifics
{"jog": "", "project": "lyubishchev"} ← mixed: activity tag + property label
```

### Why one dict, not separate types

Tags and k=v labels need the same operations: store, filter, categorize. Splitting them would mean two storage paths, two query paths, two category matching paths — for no benefit. A tag is just a label where the user chose not to provide a value.

### Progressive detail

Users can start vague and get specific over time, on the same key:

```
work              → "I worked" (no detail)
work=cba          → "I worked on CBA"
work=cc           → "I worked on CC"
```

All three are valid. No schema change, no migration. The same key (`work`) supports both tag and label usage.

## Matching Semantics

Two match patterns, one mechanism:

| Match pattern | Meaning | Matches |
|---|---|---|
| `work` (key only) | "any entry with key `work`" | `work=""`, `work=cba`, `work=cc` |
| `work=cba` (key=value) | "only entries where work is cba" | `work=cba` only |

**Key-only match is a superset.** It includes all entries with that key regardless of value. This means:
- Filtering by `work` gives you everything work-related
- Filtering by `work=cba` narrows to one specific type of work
- The user doesn't have to decide upfront how specific they'll be — the model supports both

## Category Tree

Categories group labels into reporting views. Leaves in the category tree are match patterns — they can be tags or k=v labels.

```json
{
  "exercise": ["jog", "swim", "anaerobic"],
  "work_all": ["work"],
  "work_detail": {
    "cba": ["work=cba"],
    "cc": ["work=cc"]
  },
  "calm": ["meditation", "walk"]
}
```

How this works:
- `"exercise"` contains `"jog"` → matches any entry with key `jog` (tag match)
- `"work_all"` contains `"work"` → matches `work=""`, `work=cba`, `work=cc` (key match = all)
- `"work_detail.cba"` contains `"work=cba"` → matches only `work=cba` (exact match)

**Categories can zoom in and out on the same underlying data** — `work_all` for the big picture, `work_detail` for breakdown. Same labels, different category views.

### Mental model

Think of it as a lens:

```
Data:       work=cba  work=cc  work  jog  swim  meditation
              │         │       │     │    │       │
Lens 1:     └─── work_all ────┘     │    │       │
(broad)                              └ exercise ┘  └ calm ┘

Lens 2:     ┌cba┐  ┌cc┐  ┌other┐
(detailed)  └────work_detail────┘    └ exercise ┘  └ calm ┘
```

Same data, different category configs. The user can have multiple named configs (already supported in the DB schema via `category_configs` table with `UNIQUE(user_id, name)`).

## UI Considerations

### Input: natural for both patterns

| User action | Input | Stored as |
|---|---|---|
| Quick tag | `jog` | `{"jog": ""}` |
| Tag with detail | `work=cba` | `{"work": "cba"}` |
| Tag without detail | `work` | `{"work": ""}` |
| Multiple | `jog project=lyubishchev` | `{"jog": "", "project": "lyubishchev"}` |

Users don't need to think about "is this a tag or a label" — they type a word, optionally add `=value`. The system handles both.

### CLI examples

```bash
lyu add jog 7:00-8:00                    # tag
lyu add work=cba 9:00-12:00              # label with value
lyu add work 13:00-14:00                 # same key, no value — still valid

lyu filter work                           # all work entries
lyu filter work=cba                       # only CBA work
```

### AI agent backfill

```
Agent: "Monday 9-12 is untracked. You usually work=cba on Monday mornings (70%).
        Was this CBA work?"
User:  "yeah"
Agent: → adds entry with label {"work": "cba"}
```

The agent can suggest at the specificity level that pattern data supports — `work` if patterns are vague, `work=cba` if patterns are clear.

### Category editor (future web UI)

When a user configures category trees:
- Drag `work` into a category → captures all work entries
- Drag `work=cba` into a category → captures only CBA work
- Both are valid leaf nodes in the tree
- The UI should show that `work` is broader than `work=cba`

## Annotations

Non-queryable metadata. Never used for filtering or categorization.

```
{"description": "morning run in the park", "clockify_id": "abc123", "source": "clockify"}
```

| Use case | Annotation key | Value |
|---|---|---|
| Human note | `description` | Freeform text (absorbs current `extra_info`) |
| Import tracking | `source` | `"clockify"`, `"csv"`, `"manual"` |
| Dedup on import | `source_id` | External system ID |

## Event Model

Events use the same label + annotation structure, with `event_type` as a first-class field:

```
Event:
  event_type: "wakeup" | "bed" | "unwell" | ...   ← promoted from labels
  labels:     {"cold": ""}                          ← sub-tags (sparse, most events have {})
  annotations: {"description": "..."}               ← same as TimeInterval
  timestamp:  Arrow
```

`event_type` is not a label because:
- Every event must have exactly one type — it's structural, not metadata
- It's extracted and checked in multiple places — a field is cleaner than a dict lookup
- Labels on events are optional sub-tags (e.g., `cold` on an `unwell` event)

## Summary

| Principle | Detail |
|---|---|
| **Two concepts** | Labels (queryable) + Annotations (non-queryable) |
| **Tags are labels** | `value=""` means "key exists, no specifics" |
| **Key match = superset** | `work` matches all work; `work=cba` matches only CBA |
| **One dict, one query path** | No separate types, no branching logic |
| **Progressive detail** | Same key supports vague → specific without migration |
| **Categories use match patterns** | Leaves can be tags or k=v — zoom in or out |
| **Annotations absorb extra_info** | Plus source tracking for imports |
| **event_type is a field** | Not a label — it's structural |
