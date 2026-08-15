# Local storage (SQLite)

Status: in-progress (roadmap phase 0). Last reviewed: 2026-08-15. No storage code in the repo yet as of this date.

## What

A local SQLite database becomes the canonical store for all time intervals and events. Includes a one-time import of the full Clockify history, so Frank owns his complete record locally.

## Why

Data ownership and independence from a third-party SaaS; the foundation every later phase (CLI ingest, stats, HTML reports) builds on.

## Key design points (settled 2026-08-15)

- Canonical store is local; Clockify becomes one ingest source (ADR-001).
- The existing data-access seam (the owner's term: "TimeIntervalFetcher") is where storage plugs in; report, habit, and notebook layers are unchanged (ADR-002).
- Schema-first: a stable core schema; flexibility comes from JSON label/annotation keys, provenance columns (where each record came from), and a schema version stamp. Evolution contract: new features add keys, not columns; an entity gets its own table only when it gains identity (ADR-004).
- UTC timestamps, stable IDs, correctability are L1 commitments (ADR-006).
- SQLite → Postgres is an L2 swap, deliberately kept possible but not built.

## Honest limitations

- Single-device, single-user by design for now; no sync, no backup story defined yet.

## Open questions

- Ongoing Clockify sync after the one-time import: needed for a transition period, or skipped? Depends on the transition question in [clockify-ingest.md](./clockify-ingest.md).
- Where does the canonical label/tag registry live once data is local? The old requirement "I want my label/tags in control" (centralized, reviewable) has no decided home yet.
