# ADR-005: Target UX is chat + timer, with task-switch and correction as first-class

Date: 2026-08-15. Status: accepted.

## Context

The daily habit broke because logging cost more attention than the tasks being logged, especially when switching tasks rapidly. Real life also includes forgetting to stop a timer.

## Decision

The target recording experience: saying "I'm doing X" starts recording. A single task-switch primitive (`lyu switch`) closes the current interval and opens the next. Forgot-to-stop and backfill corrections (`fix`, `log`) are first-class capabilities, not afterthoughts.

## Consequences

- Recording one moment of life costs one short line.
- The data model must support editing past entries safely (stable IDs, correctability — L1).
- Success measure is behavioral: the daily habit holds.
