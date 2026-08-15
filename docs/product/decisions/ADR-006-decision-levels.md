# ADR-006: Decision levels — commit now (L1), keep swappable (L2), defer (L3)

Date: 2026-08-15. Status: accepted.

## Context

The long-term vision (possible commercialization, web/native UI) tempts premature architecture. The near-term goal is a working daily habit for one user.

## Decision

Three explicit levels:

- L1 — decided now, hard to change later: domain model, storage seam, UTC timestamps, stable IDs, correctability.
- L2 — designed to be swappable later, not built now: SQLite → Postgres, CLI → HTTP API, local chat → in-app chat.
- L3 — deferred entirely: UI technology choice, mobile, multi-user/auth, billing.

## Consequences

- L1 items justify care and review; L2/L3 items must not consume near-term effort.
- Promoting an L3 item (e.g. multi-user) requires a new ADR and owner sign-off.
