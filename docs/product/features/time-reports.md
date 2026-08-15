# Time reports

Status: shipped. Last reviewed: 2026-08-15.

## What

Analytical views of how time was spent, at day, week, and month granularity, rendered in Jupyter notebooks: time breakdown by category (self-improvement, work, routine, exercise, relax, distracted, ...), sleep and getup/bed curves, effective-time totals in the Lyubishchev spirit, and highlights.

## Why

Recording without review is pointless: the Lyubishchev method depends on regularly confronting honest statistics ("每月小结"). The weekly view answers the critical-path question "query a week".

## Key design points (settled)

- A "day" is bounded by getup and bed events, not by calendar midnight; sleep credited to a day includes the previous night plus daytime naps.
- Reports consume data only through the storage seam, so they are unaffected when the store changes (ADR-002).

## Honest limitations

- Requires starting a notebook server and manually re-running cells — high friction for a daily/weekly ritual. Phases 2 (terminal `lyu stats`) and 3 (static HTML) exist to remove this.
- Display timezone is effectively fixed to Sydney.

## Open questions

- What is the minimum content of `lyu stats` that satisfies "query a week"? Not yet specified.
