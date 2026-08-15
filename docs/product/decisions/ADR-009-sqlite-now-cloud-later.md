# ADR-009: Persistence — SQLite now; multi-laptop via file sync; cloud DB deferred

Date: 2026-08-15. Status: accepted.

## Context

The owner asked whether to use Postgres (JSON support), TimescaleDB, or a cloud DB — partly because he works across two laptops. Data volume is tiny (~20 entries/day, thousands of rows/year). Avoid-perfect principle: make the key decision, start using it.

## Decision

SQLite is the store (per ADR-001), and no server or cloud database is adopted now.

- Postgres/Timescale rejected for now: they add an always-on service, credentials, and ops for a dataset a laptop handles trivially; Timescale targets millions of time-series rows.
- Multi-laptop sharing is solved at the FILE level when it becomes a real pain: synced file (Syncthing) or Litestream replication to object storage (~$0). ULID primary keys are merge-safe across machines by construction.
- If a served/cloud DB is ever genuinely needed (API, multi-user), the storage seam (ADR-002) and the portable schema (TEXT/JSON columns) make SQLite → Postgres or serverless SQLite (e.g. Turso) an implementation swap, not a redesign.

## Consequences

- Zero ops and zero cost today; nothing blocks the cloud path later.
- The two-laptop workflow needs a sync step until file replication is set up (icebox item, trivial).
