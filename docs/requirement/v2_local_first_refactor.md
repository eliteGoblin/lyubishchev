# v2 Refactor: Local-First Time Logging

Status: DRAFT (high-level direction, 2026-08-15). Goal: rebuild the daily logging habit, own the data locally, and make CLI + chat (agent) the primary interface for both ingest and query.

## Problem with current state

- Clockify is the only ingest UI and the only data store. The data lives in a SaaS; every report run re-fetches over HTTP; logging requires the Clockify app/web UI, which adds friction and broke the daily habit.
- Reports live only in Jupyter notebooks; getting a quick answer ("how much time on math last week?") requires starting a notebook server.

## Target architecture

```
ingest sources                canonical store            consumers
--------------                ---------------            ---------
CLI (typer)  ──┐
chat/agent ────┤──► validate ──► SQLite (single file) ──► CLI stats (table + terminal chart)
Clockify sync ─┘   (existing        time_entry, event  ──► Jupyter notebooks (existing, unchanged)
                   data_validator)                     ──► generated local HTML report (plotly, later)
```

Key decisions:

1. **SQLite is the canonical store.** One file, zero server, queryable by pandas directly, trivially backed up (synced dir or a private git repo). Postgres/cloud DB is deliberately NOT built — single user, single machine, no concurrency need.
2. **The existing `TimeIntervalFetcher` ABC is the seam.** Add a `SqliteFetcher` implementation; the report/habit/notebook layers do not change. Clockify becomes one ingest source among several instead of the system of record.
3. **The CLI is the API.** Chat ingest = Claude Code (or any agent) invoking the CLI via a repo skill/CLAUDE.md instructions. No MCP server, no chatbot app is built until the CLI proves insufficient (YAGNI).
4. **Data model stays.** `TimeInterval`/`Event` with label/annotation dicts already fit; labels serialize to JSON columns (or a tag table if query performance ever requires it — not now).

## Decision levels (from 2026-08-15 discussion)

Frank is the core user now, but commercialization (multi-user product, native/web UI) is a possible future. Therefore: invest in the DATA and INTERFACE layers; defer everything user-facing. Decisions are ranked by cost-to-change-later:

- **L1 — decide now, expensive to change later:** domain model (TimeInterval/Event + label taxonomy), storage seam (`TimeIntervalFetcher` + a writer interface), timestamps always UTC ISO-8601 with timezone handled at the edge, stable entry IDs, entries are correctable after the fact (edit/backfill is a first-class operation, not an anomaly).
- **L2 — designed to swap, but not built now:** SQLite → Postgres/cloud (same interfaces), CLI → HTTP API service (CLI commands become endpoints), local agent chat → in-app chat.
- **L3 — deferred entirely:** UI technology (React/native), mobile, multi-user/auth, sync between devices, billing.

Feature discipline: few features, good foundation, quick value. Anything not on the critical path of "log a day, query a week" waits.

## Target UX (informs data design, built incrementally)

Frank switches tasks quickly and found per-entry logging in Clockify cumbersome. The end-state UI is **chat + timer**: tell the agent "I'm doing X" and it starts recording; corrections ("I forgot to stop", "actually that started at 2pm") are normal operations. KISS version now, as CLI primitives:

- `lyu switch "<desc>" [--project ...]` — the core primitive for rapid task switching: closes the running interval (if any) and starts a new one. One command per context switch.
- `lyu stop` — close the running interval.
- `lyu status` — show the running timer.
- `lyu fix` / `lyu log` — backfill or correct: adjust the end time of a forgotten timer, insert a missed interval after the fact.
- Data consequence: the running timer is CLI state (a small state table or file), NOT an open row in the canonical `time_interval` table — canonical history only ever contains closed, validated intervals. This keeps the fetcher/report layers simple and makes forgot-to-stop a state-repair problem, not a data-integrity problem.
- Chat = the agent invoking these same commands; shell aliases/shortcuts for one-keystroke switching.

## Ingest paths

- `lyu log "<desc>" --type work --project math --duration 45m [--start ...]` — after-the-fact entry (Lyubishchev's own method: record after each work block).
- `lyu start` / `lyu stop` — live timer (optional, phase 2).
- `lyu event bed|getup|...` — daily events already modeled by the habit layer.
- Chat: "I spent 2h on linear algebra this morning" → agent parses, runs `lyu log`, echoes back the stored entry for confirmation.
- `lyu sync clockify --from ... --to ...` — one-off history import + optional ongoing sync while Clockify (mobile app) is still used for capture away from the desk.

## Query / visualization paths

- `lyu stats --last 7d [--project math]` — table + terminal bar chart (rich/plotext), answers the daily "where did my time go" question in one command.
- Chat: agent runs `lyu stats`/SQL against the SQLite file and explains.
- Notebooks keep working via `SqliteFetcher` (no HTTP, faster).
- Later: `lyu report week --html` renders the notebook charts (plotly `to_html`) to a static local page — replaces the notebook-server workflow.

## Phases

| Phase | Deliverable | Definition of done |
|---|---|---|
| 0 | Schema + `SqliteFetcher` + `lyu sync clockify` history import | Full Clockify history in a local .db; existing WeekReport notebook renders from it identically |
| 1 | `lyu log` / `lyu event` ingest with validation | A full day can be logged from the CLI alone |
| 2 | Chat ingest (repo skill for agent) + `lyu stats` terminal report | "how much time on X" answered in chat and in one CLI command |
| 3 | Static HTML report generation | Weekly review without starting Jupyter |
| 4 | UI refinement (input UX, richer viz, maybe React) | Deferred; only after the habit is re-established |

## What to log (habit-first guidance)

Start minimal — friction is what killed the habit. Core record = categorized time interval (existing label taxonomy) + the two anchor events (getup/bed). Output measurement (pages, notes, LOC — see ideas.md) and project-tree/agile integration are explicitly deferred to after the habit sticks.

## Open questions

- Keep Clockify mobile app as a capture device long-term (sync-based design supports it), or go CLI-only? Depends on how much logging happens away from the desktop.
- Backup strategy for the .db file: synced folder vs. private git repo with daily commit.
