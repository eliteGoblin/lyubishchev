# ADR-001: SQLite becomes the canonical local store; Clockify demoted to ingest source

Date: 2026-08-15. Status: accepted.

## Context

Clockify (SaaS) is both the recording UI and the data store. The data is not owned locally, logging friction broke the daily habit, and reporting depends on external availability.

## Decision

A local SQLite database is the canonical store for all time data. Clockify becomes one ingest source: a one-time full-history import, plus optional ongoing sync during the transition.

## Consequences

- Frank owns his complete record locally; the product works offline.
- Every later phase (CLI ingest, stats, HTML reports) builds on this store.
- Migration effort: history import must be trustworthy (provenance recorded per entry).
- Open: whether ongoing Clockify sync is needed during the transition — owner to decide.
