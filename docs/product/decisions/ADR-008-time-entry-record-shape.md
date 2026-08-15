# ADR-008: Time-entry record shape — free text, validated labels, open annotations

Date: 2026-08-15. Status: accepted (confirmed by owner in design session).

## Context

The owner wants one record that answers three questions without future redesign: where did time go (statistics), what did I do (narrative), what did the time produce (outputs). Outputs may be numbers or free text; an LLM can summarize free text on demand. Not every entry has a project.

## Decision

One time entry = when + three parts with distinct contracts:

- `extra_info` — free text, "what I did". Read by humans and the LLM; never queried by SQL.
- `label` — key=value pairs from a CLOSED, validated vocabulary (e.g. `type=work`, `project=math`). Statistics is `sum(duration) group by label`. Unknown keys are rejected. Project is just an optional label key.
- `annotation` — key=value pairs, OPEN set, never validated (e.g. `pages=30`, links). Optional enrichment; entries with only text + labels are complete.

The distinction is contract, not structure: label = the dimension time is bucketed by (strict, so stats never lie); annotation = the payload the time produced (free, so recording is never blocked).

## Consequences

- Daily logging burden stays minimal: time + 1-2 labels + a sentence.
- A typo can never silently create a new statistics bucket (validation), and spontaneous outputs are never rejected (open annotations).
- Free-text outputs are first-class: LLM extraction replaces upfront schema design for output measurement.
- A predefined project registry (autocomplete/validation list) can be added later without schema change.
