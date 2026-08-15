# CLI ingest

Status: planned (roadmap phase 1). Last reviewed: 2026-08-15.

## What

Recording time directly from the terminal against the local store. Target verbs: `switch` (close the current interval and open the next in one action — the task-switch primitive), `stop`, `status`, `log` (record a completed interval after the fact), `fix` (correct a past entry), `event` (record a point-in-time event such as getup or bed).

## Why

This is the habit-rebuild feature. The daily habit broke because per-entry logging in Clockify is cumbersome under rapid task switching; a one-line `switch` makes recording cheaper than not recording. Forgot-to-stop and backfill corrections are first-class because they are the normal case, not the exception.

## Key design points (settled 2026-08-15)

- CLI is the API: chat and any future UI are layers that invoke it; no MCP server or chatbot app until the CLI proves insufficient (ADR-003).
- Target UX is chat + timer: saying "I'm doing X" starts recording (ADR-005); in phase 1 the terminal is the interface, in phase 2 an agent translates chat to the same commands.
- Entered labels/tags are validated against the known set; unknown ones are surfaced rather than silently accepted or fatal.

## Honest limitations (anticipated)

- Terminal-only: nothing is recordable away from a computer (mobile is L3-deferred).

## Open questions

- Exact minimum verb set for launch: are all six verbs needed on day one, or do `switch`/`stop`/`status` alone rebuild the habit? BA recommendation: start with the smallest set that covers one full real day.
