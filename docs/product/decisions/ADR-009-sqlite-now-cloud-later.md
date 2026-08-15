# ADR-009: Persistence — SQLite now; multi-laptop via file sync; cloud DB deferred

Date: 2026-08-15. Status: SUPERSEDED by ADR-010 (same day). The owner rejected any design with a manual sync step: two-laptop use is on the daily logging path, and forgetting to sync blocks or forks the log. Storage moves to a shared-by-default managed cloud Postgres; provider selection in ADR-010.

## Context

The owner asked whether to use Postgres (JSON support), TimescaleDB, or a cloud DB — partly because he works across two laptops. Data volume is tiny (~20 entries/day, thousands of rows/year). Avoid-perfect principle: make the key decision, start using it.

## Decision

SQLite is the store (per ADR-001), and no server or cloud database is adopted now.

- Postgres/Timescale rejected for now: they add an always-on service, credentials, and ops for a dataset a laptop handles trivially; Timescale targets millions of time-series rows.
- Multi-laptop sharing is solved at the FILE level: Litestream v0.5 replication to an object-storage bucket (Cloudflare R2 free tier, ~$0), wrapped as `lyu db pull` (restore-if-newer) / `lyu db push` (replicate), with only one laptop replicating at a time. ULID primary keys are merge-safe across machines by construction.
- File-sync tools (Syncthing, Dropbox) on a live SQLite database are REJECTED as unsafe: WAL checkpoint mid-sync can corrupt the file (sqlite.org/howtocorrupt; adversarial review 2026-08-15).
- Turso free tier (local embedded replica + managed sync, $0) is the pre-validated fallback if the pull/push step proves annoying; rejected as the default on vendor dependency and SDK churn.
- If a served/cloud DB is ever genuinely needed (API, multi-user), the storage seam (ADR-002) and the portable schema (TEXT/JSON columns) make SQLite → Postgres or serverless SQLite (e.g. Turso) an implementation swap, not a redesign.

## Consequences

- Zero ops and zero cost today; nothing blocks the cloud path later.
- The two-laptop workflow needs a sync step until file replication is set up (icebox item, trivial).
