# SQLite is the source of truth; Clockify is an import source only

Status: accepted (2026-11-08)

The app owns its data in a local SQLite database from day 1. Clockify history is imported once in full, and the import can be repeated safely while Clockify is still used for logging (dedup on `source` + `source_id`). The chat and the UI write only to SQLite and never call the Clockify write API. We chose this because owning the data is a core goal of the vision, and writing to two systems would need sync and conflict handling for no lasting benefit. The schema stays PostgreSQL-compatible for the later multi-user move.
