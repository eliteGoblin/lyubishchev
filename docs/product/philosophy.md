# Philosophy

## Mission

A personal time-and-metric tracking system implementing Alexander Lyubishchev's time-statistics method. The guiding idea, in the owner's words: "花了xx时间, 产出xx事情" — time spent should be traceable to output produced.

Near-term goal: rebuild Frank's daily logging habit and own his data locally. Long-term possibility: commercialize as a multi-user product with a web/native UI — explicitly deferred (see Decision levels, L3).

## Persona

One user today: Frank — "user and CEO". He is both the customer and the developer. Every near-term requirement is judged by whether it helps Frank log his day with near-zero friction and see honest weekly statistics.

## The pain being solved

Clockify (a third-party SaaS) is currently both the UI and the data store. Per-entry logging there is cumbersome, especially with rapid task switching, and the daily habit broke. Reports require running a Jupyter notebook server. The data lives outside Frank's control.

## Cross-cutting principles

- Local-first: the canonical data store is local and owned by Frank. External services are ingest sources, not the system of record.
- CLI is the API: every capability is reachable from the command line; richer interfaces (chat, UI) are layers on top, not parallel systems.
- Correctability is first-class: humans forget to stop timers; fixing and backfilling entries must be as easy as recording them.
- Schema-first with flexibility: a stable core schema, with flexible label/annotation keys for evolution. New features add keys, not columns; an entity gets its own table only when it gains identity.
- Tags stay in the owner's control and flexible: adding/removing a tag must not require broad changes; unknown tags are surfaced, not fatal (carried over from the label/tags requirements).
- UTC timestamps and stable IDs throughout; display in the user's local timezone (currently Sydney).
- Feature discipline: few features, good foundation. The critical path is "log a day, query a week" — anything not serving it waits.

## Decision levels

- L1 — decided now, hard to change: domain model, storage seam, UTC timestamps, stable IDs, correctability.
- L2 — swappable later by design: SQLite → Postgres, CLI → HTTP API, local chat → in-app chat.
- L3 — deferred entirely: UI technology, mobile, multi-user/auth, billing.

## Out of scope (for now)

Multi-user, authentication, billing, mobile apps, device sync, MCP server / standalone chatbot app, agile-tool integrations, output measurement. These live in `ideas.md` until deliberately promoted.
