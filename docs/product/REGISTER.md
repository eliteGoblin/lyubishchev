# Register

Mission: see [philosophy.md](./philosophy.md). Last updated: 2026-08-15 (bootstrap).

## Feature status

| Feature | Spec | Status | Notes |
|---|---|---|---|
| Clockify ingest | [features/clockify-ingest.md](./features/clockify-ingest.md) | shipped | Being demoted from system-of-record to one ingest source (ADR-001) |
| Notebook reports | [features/time-reports.md](./features/time-reports.md) | shipped | Day / week / month views; requires notebook server (known pain) |
| Habit tracking | [features/habits.md](./features/habits.md) | shipped | Getup, bed, and interval-based habits with scores |
| Local storage (SQLite) | [features/local-storage.md](./features/local-storage.md) | in-progress | Roadmap phase 0; no code in repo yet as of 2026-08-15 |
| CLI ingest | [features/cli-ingest.md](./features/cli-ingest.md) | planned | Roadmap phase 1; the habit-rebuild feature |

## Roadmap (committed, sequenced)

| Phase | Deliverable | Status |
|---|---|---|
| 0 | SQLite storage + Clockify history import | in-progress |
| 1 | CLI ingest: `switch` / `stop` / `status` / `log` / `fix` / `event` | planned |
| 2 | Chat ingest via agent + `lyu stats` terminal report | planned |
| 3 | Static HTML report generation | planned |
| 4 | UI refinement (React; also serves owner's upskilling goal) | planned |

## Decisions

See [decisions/](./decisions/) — ADR-001..007, all dated 2026-08-15.

## Related documents

- Engineering design for the local-first refactor: `docs/requirement/v2_local_first_refactor.md` (owned by engineering; not present in every checkout).
- Legacy requirement docs: `docs/v0.1.0/`, `docs/label_and_tags/`, `docs/requirement/support_bedtime_habit.md` — partially stale, kept until migration is approved (see drift notes in the 2026-08-15 BA report).

## Icebox

Speculative ideas live in [ideas.md](./ideas.md); the original `docs/ideas.md` is preserved untouched.
