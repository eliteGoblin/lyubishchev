# Clockify ingest

Status: shipped (role changing). Last reviewed: 2026-08-15.

## What

Fetches Frank's time intervals and events (getup, bed, etc.) from the Clockify SaaS, where they are currently recorded, and turns them into the internal data model (intervals, events, labels/tags) that reports and habits consume.

## Why

Clockify was the original recording UI and store. All historical data lives there, so it remains valuable as a source even after the product stops depending on it.

## Direction (decided 2026-08-15, ADR-001)

Clockify is demoted from system-of-record to one ingest source: a one-time history import into the local store, plus optional ongoing sync while the transition lasts.

## Honest limitations

- Per-entry logging in Clockify is cumbersome, especially with rapid task switching — this is the pain that broke the daily habit.
- Requires API credentials and network access; data is held by a third party until the history import ships.

## Open questions

- During the transition, does Frank keep logging in Clockify (needing ongoing sync) or switch to the CLI immediately after phase 1? Owner to decide.
