# Target Architecture & Roadmap

## Architecture

**Phase 1-3 (personal, no server):**
```
Clockify API ──sync──> CLI (Node.js) ──validate──> SQLite <──read── Jupyter (Python)
                       CLI add/backfill ─────────────┘
```

**Phase 4+ (multi-user, server):**
```
monorepo/
├── packages/domain/       ← shared: validation, matching, habits
├── packages/db/           ← shared: SQLite/PostgreSQL access
├── packages/api-client/   ← CLI uses this to talk to backend
├── apps/cli/              ← personal tool, calls backend API
├── apps/backend/          ← owns DB, auth, permissions
└── apps/web/              ← Next.js frontend

CLI ──api-client──> Backend ──domain──> PostgreSQL
Web ─────────────> Backend ──domain──> PostgreSQL
Jupyter (Python) reads DB directly (personal analysis only)
```

**Principles:**
- Database is source of truth, not Clockify
- `user_id` on every table from day 1 (avoids migration when adding auth)
- Domain logic is a shared package — same validation whether called from CLI, backend, or agent
- CLI accesses DB directly in Phase 1-3 (no server needed), switches to API client in Phase 4+
- Each phase is independently useful; no rewrites between phases
- All product code is TypeScript; Python is only for Jupyter notebooks

## Source of Truth: Gradual Transition

The source of truth shifts over time, not all at once:

| Phase | Source of Truth | DB Role | Add Past Data Via |
|---|---|---|---|
| Now (Clockify+Jupyter) | Clockify | None | Clockify UI |
| Phase 1-2 (DB + CLI) | Clockify | Read-only sync'd mirror | Clockify UI, then `lyu sync` |
| Phase 3+ (local entry) | Database | Primary store | `lyu add` or Clockify -> sync |
| Phase 5+ (web) | Database | Primary store | Web UI, CLI, or Clockify import |

**Why not make DB source of truth immediately?** Because you already have a working Clockify workflow. The DB starts as a performance cache. When you build `lyu add` (direct local entry creation), the DB naturally becomes source of truth and Clockify becomes one optional import source.

**Schema supports both models:** The `source` column on `time_intervals` and `events` distinguishes `"clockify"` (imported) from `"manual"` (locally created). No schema change needed for the transition.

## Category Tree Design

Labels on time intervals are **facts** (what you did, in what context). The category tree is a **report configuration** — how a user chooses to view their data grouped. These are separate concerns.

For the full label/annotation data model, see `topics/core_data_model_review.md`.

### Matching semantics

Category tree leaves are **match patterns** — they can be tags or k=v labels:

| Pattern in tree | Matches | Example |
|---|---|---|
| `"work"` (key only) | All entries with key `work`, any value | `work=""`, `work=cba`, `work=cc` |
| `"work=cba"` (key=value) | Only entries where `work` equals `cba` | `work=cba` only |

Key-only match is a **superset** of k=v match. This enables categories that zoom in/out on the same data.

### Storage: JSON document per user, not relational rows

```sql
category_configs (
    id              TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL REFERENCES users(id),
    name            TEXT NOT NULL DEFAULT 'default',  -- allow multiple views
    tree            TEXT NOT NULL,                      -- JSON document
    version         INTEGER DEFAULT 1,
    updated_at      TEXT NOT NULL,
    UNIQUE(user_id, name)
)
```

The `tree` JSON:
```json
{
  "effective_output": {
    "self_improving": {
      "tech": ["job", "lyubishchev", "oj", "software"],
      "non_tech": ["audible", "reading"]
    },
    "work_all": ["work"]
  },
  "work_detail": {
    "cba": ["work=cba"],
    "cc": ["work=cc"]
  },
  "calm": ["meditation", "walk"],
  "exercise": ["jog", "swim", "anaerobic"],
  "regret": ["pmo", "numb", "dispute", "video", "game", "internet", "novel"],
  "routine_all": ["cook", "self_routine", "housework", "meal"],
  "intangible": ["friends", "family", "lisha", "dating"],
  "sex_all": ["sex", "mbate"],
  "solitude": ["karaoke"],
  "sleep_all": ["night_sleep", "nap"]
}
```

Leaves are arrays of match patterns (tags or k=v labels). Non-leaves are nested objects. A user can have multiple named configs (e.g., `"default"` for overview, `"work_focus"` for work breakdown) viewing the same underlying data differently.

### Why JSON document, not adjacency list

| Approach | Drag-and-drop | Query subtree | Multi-user | Versioning |
|---|---|---|---|---|
| Adjacency list (parent_id rows) | Update parent_id + sort_order per node | Recursive CTE | One table, filter by user_id | Complex (track each row) |
| JSON document (one row per user) | Replace whole document | Load whole tree (fast, it's small) | One row per user config | Trivial (keep old rows, bump version) |

The tree is always loaded and saved as a unit. The frontend renders the whole tree for drag-and-drop. Individual SQL queries into the tree aren't needed. JSON is simpler for this pattern.

### How it works in practice

1. **First run / new user:** Seed `category_configs` from a default template (same as current hardcoded tree)
2. **CLI:** `lyu categories` shows the tree. `lyu categories edit` opens in editor.
3. **Web UI:** Renders tree as draggable nodes. Save = PUT the whole JSON doc.
4. **Domain layer:** Loads user's tree, builds `Match` objects from it (same logic as today, data-driven)
5. **Multiple views:** A user could have `"default"` and `"work_focus"` configs with different groupings of the same underlying data.

## Database Schema (SQLite-compatible, PostgreSQL-ready)

```sql
users (
    id              TEXT PRIMARY KEY,   -- "default" for single-user
    email           TEXT,
    timezone        TEXT NOT NULL,      -- IANA name
    created_at      TEXT NOT NULL       -- ISO8601
)

category_configs (
    id              TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL REFERENCES users(id),
    name            TEXT NOT NULL DEFAULT 'default',
    tree            TEXT NOT NULL,       -- JSON: full category hierarchy
    version         INTEGER DEFAULT 1,
    updated_at      TEXT NOT NULL,
    UNIQUE(user_id, name)
)

time_intervals (
    id              TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL REFERENCES users(id),
    timestamp       TEXT NOT NULL,      -- ISO8601
    duration_minutes INTEGER NOT NULL,
    labels          TEXT NOT NULL,       -- JSON: {"jog":"","project":"lyubishchev"}
    annotations     TEXT DEFAULT '{}',  -- JSON: {"description":"...","clockify_id":"..."}
    source          TEXT NOT NULL,       -- "clockify", "csv", "manual"
    source_id       TEXT,               -- dedup key from import source
    UNIQUE(user_id, source, source_id)
)

events (
    id              TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL REFERENCES users(id),
    timestamp       TEXT NOT NULL,
    event_type      TEXT NOT NULL,       -- "wakeup","getup","bed",...
    labels          TEXT NOT NULL,       -- JSON: {"cold":""} (sub-tags)
    annotations     TEXT DEFAULT '{}',  -- JSON: {"description":"..."}
    source          TEXT NOT NULL,
    source_id       TEXT,
    UNIQUE(user_id, source, source_id)
)

day_records (
    id              TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL REFERENCES users(id),
    date            TEXT NOT NULL,       -- YYYY-MM-DD
    wakeup_ts       TEXT NOT NULL,
    getup_ts        TEXT NOT NULL,
    bed_ts          TEXT NOT NULL,
    last_night_sleep_minutes INTEGER NOT NULL,
    is_valid        INTEGER DEFAULT 1,
    UNIQUE(user_id, date)
)

import_sources (
    id              TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL REFERENCES users(id),
    source_type     TEXT NOT NULL,       -- "clockify"
    config          TEXT,                -- JSON: API keys, etc.
    last_sync_at    TEXT
)
```

**Key decisions:**
- `TEXT` for timestamps/IDs = SQLite + PostgreSQL compatible
- `labels` as JSON = flexible, no schema change for new activities. Tags (`value=""`) and properties (`key=value`) in one dict (see `topics/core_data_model_review.md`)
- `annotations` as JSON = non-queryable metadata (replaces `extra_info`). Holds descriptions, source IDs, notes
- `source` + `source_id` = dedup on re-import, supports gradual source-of-truth transition
- `day_records` references intervals/events by `user_id + date range`, not FKs
- `category_configs` replaces hardcoded `get_match_dict()` -- JSON tree, not relational rows

## Roadmap

### Phase 1: Node.js CLI + Clockify Sync
- Node.js CLI (TypeScript monorepo: `packages/domain/`, `packages/db/`, `apps/cli/`)
- SQLite database with schema above
- `lyu sync` — fetch Clockify API → validate → write to SQLite (incremental)
- `lyu last 7` — terminal reports (tables, summaries)
- `user_id = "default"` hardcoded
- Clockify remains source of truth; DB is sync'd mirror
- Jupyter reads same SQLite for personal analysis
- Existing Python code serves as reference/spec for TS domain logic

### Phase 2: CLI Local Entry + Agent
- `lyu add work=cba 9:00-12:00` — validate → write directly to SQLite
- `lyu start work=cba` — timer mode, writes entry on stop
- `lyu backfill` — AI-assisted gap filling (see Agent Tool Design below)
- Category tree from `category_configs` table (seeded from default)
- Both Clockify sync and local entries coexist (`source` column distinguishes)
- Gradually stop using Clockify UI as CLI becomes primary input

### Phase 3: Remove Clockify
- Final full import: all Clockify history → SQLite
- Remove Clockify dependency (import adapter stays for anyone who wants it)
- CLI is sole entry point, DB is sole source of truth
- Data model and tool interfaces are stable at this point
- Goals & targets: `lyu status` shows progress (exercise 2/3 this week, etc.)

### Phase 4: Backend + Auth
- API server (Next.js API routes or standalone Node/Express)
- Owns DB — auth, permissions, user management via JWT
- CLI switches from direct SQLite → API client (`packages/api-client/`)
- CLI and backend share `packages/domain/` — same validation logic
- SQLite → PostgreSQL when multi-user is needed

### Phase 5: Web Frontend
- Next.js (App Router) — frontend + API routes in one app
- Drag-and-drop category tree editor
- Interactive charts (Recharts/Nivo — replaces Jupyter for product visualization)
- User registration, onboarding
- Native time entry UI
- Billing
- Jupyter stays as personal data lab, reads same DB

## Language Strategy

**TypeScript from Phase 1. Python only for Jupyter notebooks.**

The DB decouples the two languages. CLI (TS) writes validated data to SQLite. Jupyter (Python) reads from the same SQLite for personal analysis. No cross-language function calls needed.

```
TypeScript (product)              SQLite              Python (personal)
├── CLI                  ──write──>  │  <──read──  Jupyter notebooks
├── Domain logic (shared)            │              (pandas, plotly)
├── Agent (Claude SDK)               │
├── Backend (Phase 4+)               │
└── Web frontend (Phase 5)           │
```

**Why TS from the start:**
- CLI needs domain logic (validation, matching) — must share language with domain package
- All Phase 1-3 components (CLI, domain, agent) share one language, import directly
- No migration/rewrite phase — build TS domain logic once, informed by existing Python as reference
- Existing Python tests serve as acceptance criteria for the TS implementation

**What stays Python:**
- Jupyter notebooks — reads DB directly, pandas + plotly for ad-hoc analysis
- Existing Python domain code — becomes reference/spec, not production code

**Clockify transition (no dual-write needed):**
- During transition: keep using Clockify UI for input, `lyu sync` pulls into SQLite
- `lyu add` writes directly to SQLite (new entries skip Clockify, `source="manual"`)
- Both coexist in DB via `source` column
- Final sync: import all Clockify history, stop using Clockify

## Agent Tool Design: LLM Orchestrates, Tools Compute

### Principle

```
LLM (orchestrator)
  CAN:  understand intent, pick next tool, interpret results,
        handle ambiguity, ask clarifying questions, format output
  CANNOT: calculate, remember data, validate, do date math,
          query DB, write entries
  RULE: never generate a fact it didn't get from a tool result
        │
        │ structured calls + structured returns
        ▼
Deterministic Tools (precise, testable, auditable)
  All date math, all queries, all validation,
  all writes, all business rules.
  Return structured data, never prose.
```

Why: letting the LLM do everything (e.g., "fill my gaps for the past month") leads to hallucination. The LLM has no memory of what you did — only your data does.

### Tool Inventory

Tools accept and return **labels** (`dict[str, str]`) — the unified format for both tags and k=v properties (see `topics/core_data_model_review.md`). Examples: `{"jog": ""}`, `{"work": "cba"}`, `{"work": "", "project": "lyubishchev"}`.

**Discovery tools (read-only):**

| Tool | Input | Output |
|---|---|---|
| `find_gaps` | `start_date, end_date` | `[{date, gap_start, gap_end, duration_min}]` |
| `get_day_summary` | `date` | Tracked entries (with labels) + gaps + coverage % |
| `get_patterns` | `weekday, time_range` | Historical frequency per label pattern |
| `list_known_labels` | (none) | All label keys and values seen in data + category config |
| `get_week_overview` | `week_offset` | Per-day coverage %, gap count |

**Mutation tools (require user confirmation):**

| Tool | Input | Output |
|---|---|---|
| `validate_entry` | `start, end, labels` | Pass/fail + reasons |
| `add_entry` | `start, end, labels, annotations` | Entry ID or validation error |
| `batch_validate` | `list of proposals` | Per-entry pass/fail |
| `batch_add` | `list of validated proposals` | Per-entry result |

Note: no separate "activity" parameter — the activity IS the label. `{"jog": ""}` or `{"work": "cba"}`. The tool doesn't need to distinguish between tags and k=v labels.

**LLM orchestration (no data computation):**

| Responsibility | Example |
|---|---|
| Parse natural language | "I worked on CBA in the morning" → `{labels: {"work": "cba"}, start: "09:00", end: "12:00"}` |
| Pick next action | Gaps found → call `get_patterns` → suggest most likely label |
| Handle ambiguity | Pattern says 80% `work=cba`, 15% `work=cc` → ask user |
| Progressive workflow | One gap at a time, not 30 days at once (prevents context loss) |
| Present tool results | Format structured data as readable summary |
| Respect "I don't remember" | Skip gap, move on — never fabricate |

### Backfill Workflow Example

```
User: "help me fill gaps for last 2 weeks"

1. LLM → find_gaps("2026-03-23", "2026-04-06")
   Tool: [{date: "03-24", gaps: [{14:00-16:30, 150min}]}, ...]

2. LLM → get_week_overview(-1), get_week_overview(-2)
   Tool: coverage per day, worst days flagged

3. LLM to user: "8 days with gaps. Worst: March 24 (62%).
   March 24, 2:00-4:30pm is untracked."

4. LLM → get_patterns("Monday", "14:00-16:30")
   Tool: {"work=cba": 65%, "reading": 20%, untracked: 15%}

5. LLM to user: "You usually do work=cba Mon afternoons (65%). Was this CBA work?"

6. User: "yeah"

7. LLM → validate_entry("2026-03-24T14:00", "2026-03-24T16:30", {"work": "cba"})
   Tool: {valid: true}

8. LLM to user: "Add work=cba 2:00-4:30pm March 24? [y/n]"

9. User: "y" → LLM → add_entry(...) → next gap
```

### Reliability Rules

1. **LLM never generates facts** — only restates tool results
2. **All date/time math in tools** — no LLM arithmetic
3. **Pattern suggestions, not assumptions** — tool says 65%, LLM asks, doesn't assert
4. **Progressive, not batch** — one gap at a time prevents context loss
5. **Validation before every write** — existing 6 validators catch bad data
6. **User confirms every mutation** — human in the loop
7. **"I don't know" is valid** — skip gaps, don't fabricate

### What Already Exists in Codebase

- 6 validators in `data_model/day.py` → reuse for `validate_entry`
- `ClockifyFetcher` + `parse_and_generate_day_records()` → basis for `get_day_summary`
- `DayRangeReport` metrics → basis for `get_patterns`
- `Match` tree in `search/search.py` → category matching for `list_known_labels`
- `get_match_dict()` → valid activity categories

New tools to build: `find_gaps`, `get_patterns`, `get_week_overview`, `batch_validate`, and the DB write layer (Phase 1 prerequisite).

## AI Agent Framework Decision

**Decision: Claude Agent SDK (or bare Claude API) for Phase 1-4. Re-evaluate at Phase 5.**

### Context

The project needs AI capabilities for:
1. Chat-based time entry parsing ("I jogged at 7am then worked until noon" → structured entries)
2. Backfill assistant (find gaps in tracked time, suggest entries)
3. Insight bot over personal data

Frameworks evaluated: Claude Agent SDK, Google ADK, direct Claude API.

### Why not Google ADK now

- Google ADK is Gemini-first; Claude model support is via adapters, not native
- Its value (Vertex AI scaling, A2A multi-agent protocol, multi-model routing) only matters at multi-user commercial scale (Phase 5+)
- Adds framework complexity for problems we don't have yet — same reasoning as SQLite-before-PostgreSQL
- The AI framework landscape will look different by Phase 5; investing heavily now risks lock-in to a framework that may not be the right choice later

### Why Claude Agent SDK / bare API now

- Native Claude integration, simplest path
- The AI needs are single-agent tool-calling patterns, not multi-agent orchestration
- The agent is: system prompt + 3-4 tools (`add_time_entry`, `list_gaps`, `query_day`, `confirm_entries`) — ~100 lines of orchestration regardless of framework
- Already fluent with Claude ecosystem (Claude Code CLI)

### Architecture for framework independence

```
Agent framework (thin, replaceable)
    │
    ├── Tools = plain Python functions
    │       │
    │       └── Domain layer (DayRecord, validation, DB)  ← durable value
    │
    └── Model = Claude API call (swappable)
```

**Key principle:** Tools are plain Python functions with no framework dependency. The domain layer stays framework-agnostic. Swapping from Claude SDK to Google ADK (or whatever is mature at Phase 5) is a day of plumbing work, not an architecture change.

### When to re-evaluate

- Phase 5 (Web API + multi-user): evaluate Google ADK, LangGraph, or whatever is mature
- If multi-agent orchestration becomes a real need (not speculative)
- If cost optimization requires routing different tasks to different models (e.g., Haiku for simple parsing, Opus for insight generation)

## Appendix: Database Engine Comparison

| Criteria | SQLite | PostgreSQL | TimescaleDB (PG extension) |
|---|---|---|---|
| **Deploy complexity** | Zero (file on disk) | Server process, config | PG + extension install |
| **Multi-user** | Single-writer, no auth | Full MVCC, roles, RLS | Same as PG |
| **JSON support** | `json_extract()`, basic | JSONB, indexable, rich operators | Same as PG |
| **Time-series queries** | Manual indexing | Composite index `(user_id, timestamp)` fast | Hypertables auto-partition by time, faster range scans at scale |
| **Aggregation** | Standard SQL | Window functions, materialized views | Continuous aggregates (auto-refreshing materialized rollups) |
| **Data volume sweet spot** | < 10M rows | < 10B rows | > 100M rows with high write throughput |
| **Your data volume** | ~11K rows/user/year | Same | Same |

**When each makes sense for this project:**

- **SQLite (Phase 1-4):** Personal use, zero ops. 11K rows/year is nothing. Composite index on `(user_id, timestamp)` gives sub-millisecond queries.
- **PostgreSQL (Phase 5+):** Multi-user web service. Handles millions of users at this data density. JSONB for labels and category trees. Row-level security for tenant isolation.
- **TimescaleDB (if ever):** Only justified if you add high-frequency automated tracking (GPS every minute, app usage every second, screen time polling). At 30 entries/day/user, PostgreSQL with proper indexes is identical in performance. TimescaleDB's continuous aggregates would be nice for pre-computing weekly/monthly rollups at 100K+ users, but that's a one-hour migration (`CREATE EXTENSION timescaledb; SELECT create_hypertable(...)`) when the time comes. Don't pay the operational complexity before the data volume demands it.

**Recommendation:** SQLite now -> PostgreSQL at Phase 5 -> TimescaleDB extension if/when high-frequency tracking or 100K+ users materialize. The schema is the same across all three.
