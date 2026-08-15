# ADR-002: The existing data-access abstraction is the storage seam

Date: 2026-08-15. Status: accepted.

## Context

Reports, habits, and notebooks already consume data through one fetch abstraction (the owner's term: "TimeIntervalFetcher") rather than talking to Clockify directly.

## Decision

That existing abstraction is the official seam where storage backends plug in. The report / habit / notebook layers are unchanged when the store moves from Clockify to SQLite (and later, if ever, to Postgres).

## Consequences

- The local-first refactor is contained: swap the source, keep the consumers.
- The seam is an L1 commitment (hard to change); backends behind it are L2 (swappable).
