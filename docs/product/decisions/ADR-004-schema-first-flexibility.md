# ADR-004: Schema-first, with flexibility via keys, provenance, and a version stamp

Date: 2026-08-15. Status: accepted.

## Context

Time-tracking needs evolve (new tags, new metrics, output measurement someday). A rigid schema would need constant migrations; a schemaless store would lose the validation the owner requires ("labels/tags must be verified").

## Decision

A stable core schema, with three flexibility mechanisms: JSON label/annotation keys for variable attributes, provenance columns recording where each record came from, and a schema version stamp on the data.

Evolution contract: new features add keys, not columns; an entity gets its own table only when it gains identity of its own.

## Consequences

- Most future features (new tags, output annotations) need no migration.
- Imported Clockify history remains distinguishable from natively logged data.
- Discipline required: resisting the urge to add columns for every new idea.
