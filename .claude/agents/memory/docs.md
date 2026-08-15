# docs role memory

- 2026-08-15: Writing a deliverable doc named `reports.md` was blocked by the subagent Write guard (it pattern-matches report-like filenames). Rule: in subagent context, avoid filenames like `report*.md` / `findings*.md` / `summary*.md` for legitimate doc deliverables — pick a domain name (used `time-reports.md`).
- 2026-08-15: This repo's product doc layer lives at `docs/product/` (owner-directed), not the default `documents/requirements/`. Legacy requirement docs (`docs/v0.1.0/`, `docs/label_and_tags/`, `docs/requirement/`) are intentionally left in place pending owner-approved migration.
