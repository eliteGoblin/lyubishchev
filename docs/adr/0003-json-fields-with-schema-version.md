# Flexible JSON fields, checked at write time, with a per-row schema version

Status: accepted (2026-11-08)

Each time entry and event has fixed columns (`start`, `end` or `timestamp`, `type`, `user_id`, `external_id`) and flexible JSON columns (`labels`, `measures`, `description`). The database does not check the JSON. The code checks it when an entry is written: known keys only, correct value types, `start < end`, no overlap. Readers ignore unknown keys and treat a missing key as "none". Adding or removing a key therefore needs no migration.

Each row carries an integer `schema_version` column, set on every write. A rename or a move of a key is done as "expand then contract": the reader accepts the current version and the one before it; a `migrate` command converts old rows in batches and reports how many changed and how many remain; when zero remain, the next release drops the old reader. There is no per-version reader beyond that window, and no semver inside the JSON.

## Considered options

- Per-row version with one reader per version, kept indefinitely: rejected, because every report must then know every old shape forever.
- Strict relational columns for every label and measure: rejected, because every new key would need a table migration.
