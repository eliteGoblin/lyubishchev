# ADR-010: Neon serverless Postgres is the canonical store

Date: 2026-08-15. Status: accepted (supersedes ADR-009 / amends ADR-001's "local SQLite").

## Context

The owner rejected any storage design with a manual sync step: he logs from two laptops interchangeably, and a forgotten sync would block or fork the daily log — a hard fail for a habit tool. Budget up to $20/mo; cold starts of a few seconds acceptable; Postgres preferred for the future webapp. Research compared AWS RDS (~$14), GCP Cloud SQL (~$11), Azure Flexible Server (~$16), Aurora Serverless (15 s resume — rejected), Neon (~$0–5, 0.3–0.5 s resume, true Postgres).

## Decision

Neon serverless Postgres (project region ap-southeast-2), connected via `LYUBISHCHEV_DATABASE_URL` from the environment. Shared by default: both laptops, the CLI, the agent, notebooks, and any future webapp read the same database. Schema per ADR-008, with label/annotation as JSONB. Connectivity verified 2026-08-15 (PostgreSQL 18.4).

## Consequences

- No sync mechanism exists anywhere in the system; nothing to forget.
- Cost ~$0–5/mo at current volume; the same database carries the future webapp (no migration event ever).
- Logging requires network — accepted; a weekly `pg_dump` to a local file is the data-ownership insurance.
- The Phase 0 SQLite storage module is reworked to Postgres behind the same fetcher seam; SQLite remains a possible offline/test backend, not canonical.
