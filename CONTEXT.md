# Lyubishchev

Personal time statistics in the style of Alexander Lyubishchev: a record of where time went and what it produced, read back as reports over any range.

## Language

### Foundation

**TimeEntry**:
A span of time `[start, end)` with exactly one type, optional labels, optional measures and an optional description.
_Avoid_: time interval, activity, entry, Clockify entry

**Event**:
A moment in time with exactly one type, optional labels and an optional description.
_Avoid_: marker, timestamp event

**Type**:
The one word that says what a TimeEntry was (jog, work, read) or what an Event was (wakeup, getup, bed, unwell, done). Every TimeEntry and Event has exactly one, from a user-managed list.
_Avoid_: activity, tag, category, event_type

**Label**:
A key with an optional value that adds context to a TimeEntry or Event, such as `project=lyu`, `book=deep_work` or `partner`. A label is never the type. Keys come from a user-managed list; values are free but reused.
_Avoid_: tag, property, attribute

**Measure**:
A named number on a TimeEntry that reports add up, such as `chapters: 2` or `km: 5`. Duration is not a measure; it comes from start and end.
_Avoid_: metric, count, output

**Description**:
Free text on a TimeEntry or Event, kept for reading and for narrative summaries. Never counted or matched.
_Avoid_: note, extra_info, annotation

### Helpers

**Subject**:
The record behind a short label value: its kind (book, project, course), its key (`deep_work`) and its full title and details.
_Avoid_: project record, book record, reference

**Category**:
A named node of a CategoryTree. It holds either child categories or a rule; a rule is a list of patterns that select TimeEntries by type (and later by label).
_Avoid_: node, group, bucket

**CategoryTree**:
A user's named tree of categories that groups TimeEntries for reports. Editing it regroups history; it never changes a TimeEntry.
_Avoid_: match dict, taxonomy, label tree

### Derived

**Day**:
The biological day from a wakeup Event to the next bed Event, with its TimeEntries, Events, sleep, coverage, gaps and status. Computed, not recorded.
_Avoid_: calendar day, DayRecord

**Gap**:
A span inside a Day with no TimeEntry.
_Avoid_: hole, untracked time, missing

**Coverage**:
The share of a Day's length that TimeEntries cover.

**Report**:
Totals over a date range per category, type, label or measure, the finished items, and an optional narrative built from descriptions.

## Current state

Last updated: 2026-11-14. Sources: Claude Code sessions for this repo from 2026-11-01 to 2026-11-11, the ADRs, and the repo docs. Items marked "not verified" were not checked against code or a later session.

### What the project is

Lyubishchev is a personal time tracker in the style of Alexander Lyubishchev. It is being rebuilt as a web app with a chat. The user logs time by chatting, and reads statistics on a web page. Later goals from the vision (`docs/requirements/0_vision_brainstorm.md`): own the user's data, add AI insight, and allow more users with their own accounts. The main pain today is that logging time in Clockify is slow, so days are backfilled late and with effort.

### Decisions made (all on 2026-11-08 unless stated)

- Rebuild as one local web app with SQLite and a chat, not a CLI first (decided 2026-11-07). This changes the April 2026 roadmap, which put the web app in a late phase.
- [ADR 0001](docs/adr/0001-sqlite-is-source-of-truth.md): SQLite is the source of truth. Clockify is an import source only. The import can be repeated without duplicates.
- [ADR 0002](docs/adr/0002-typescript-monorepo-python-archived.md): TypeScript monorepo with Next.js. The Python code moves to `archive/python/` as read-only reference.
- [ADR 0003](docs/adr/0003-json-fields-with-schema-version.md): JSON fields for labels, measures and description. They are checked when written. Each row has a schema version.
- Domain model: TimeEntry and Event are the foundation. Both have exactly one Type. Terms are defined above.
- A Day has a status (complete or incomplete, with reasons) and is never rejected. Only an overlap or `start >= end` blocks a write.
- Method: light domain-driven design, ports and adapters, ADRs for key decisions.
- Multi-user seams: `user_id` on every table, a `CurrentUser` port that returns a default user, and `userId` passed to every use case. No auth code in the MVP.
- MVP UI: two pages. Log page: a timer bar for the current activity, the chat in a narrow panel, and a list of today's entries with a date picker. Gaps show as red dashed rows. Stats page: tabs Time stat (Daily, Weekly, Month) and Habits, with a pie chart, a sleep line chart and hours-per-day bars. Scope rule from Frank: keep the MVP small and add nothing he did not ask for.
- UI feedback is done on an Excalidraw sketch and a published Claude artifact mock. Figma is not used for now.

### What was built

- Docs only: the three ADRs, this glossary, and the design docs in `docs/requirements/` and `topics/`.
- Latest UI design: Claude design artifact "Lyubishchev UI Mock" (https://claude.ai/artifact/RxiHGsjwjEtUjPtH7P3ADy, last updated 2026-11-08; private, owner only). Its source (Log and Stats artboards, example data only) is saved in [`docs/design/ui-mock/`](docs/design/ui-mock/) on 2026-11-14.
- No TypeScript code exists yet. `apps/` and `packages/` are not in the repo, and the Python code has not been moved to `archive/python/` (checked 2026-11-14 by listing the repo root).
- The old Python code and the Python CI still exist in place. `CLAUDE.md` still describes the Python system and is stale for the new direction.

### In progress

- UI design on the mock. The last open items on 2026-11-08: the meaning of the grey box that Frank drew under the entry list, and the Stats mock may show an older version (reload).
- The design grill (`clarify`) had 8 questions in round 1. Q1 to Q4 are accepted. Q5 (stats page content), Q6 (chat scope) and Q7 (use an Anthropic API key and the Sonnet model) were proposed. Whether Frank accepted them is not verified. Q8 (multi-user seams) was agreed.

### Open questions and next steps

- Confirm Q5 to Q7 and finish the Stats and Log mock.
- Set up the monorepo layout from ADR 0002 and move the Python code to `archive/python/`.
- Port the domain code (validators, day parser, habits) to TypeScript, using the Python tests as the spec.
- Build the Clockify import with dedup on `source` and `source_id`.
- Build the chat tools with a confirm step before every write.
- Update `CLAUDE.md` to match the new layout.
- Not verified: the Category and report details beyond the glossary. A Day has a status, but its exact reasons are not defined in the docs.
- Earlier work: the April 2026 design docs were written in sessions that no longer exist. The Ubuntu VM has an older repo copy (2025-08-17) and no related sessions.
