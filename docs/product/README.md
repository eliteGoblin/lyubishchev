# Product / Requirements Layer

This folder is the product-altitude source of truth for lyubishchev: WHAT the product does and WHY, never HOW it is coded. Implementation detail belongs in code, commit messages, and engineering design docs (e.g. `docs/requirement/v2_local_first_refactor.md`).

## How this folder works

| File / dir | Purpose |
|---|---|
| `REGISTER.md` | Living index: feature status table, roadmap, committed backlog. Start here. |
| `philosophy.md` | Mission, persona, cross-cutting principles, decision levels, out-of-scope. |
| `features/` | One short spec per feature: what it does, why, settled design questions, honest limitations, status. |
| `decisions/` | ADRs, date-stamped, immutable once accepted. Reversing one means writing a NEW ADR that supersedes it. |
| `ideas.md` | Icebox: speculative, uncommitted ideas. Absorbs `docs/ideas.md`; may never ship. |
| `glossary.md` | Project-specific terms. |

## How agents use it

Architect/dev/e2e agents treat `features/*.md` as the contract for what to build and verify. Feature status values: `planned`, `in-progress`, `shipped`, `deprecated`. A shipped claim must be backed by code and tests.

## Rules

Keep docs short (feature spec ~150 lines max, ADR ~80 max). One paragraph = one line, no hard wrapping. Never delete history: superseded content moves to `docs/archive/` with a note. Legacy docs (`docs/v0.1.0/`, `docs/label_and_tags/`, `docs/requirement/`) stay in place until the owner approves migration.
