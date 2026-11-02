# ADR-0003: building.json versioning

- Status: Accepted
- Date: 2026-11-02

## Context

Two codebases evolve the contract; silent incompatibilities would corrupt models.

## Decision

SemVer `SCHEMA_VERSION` declared in the file and in the schema (`x-schema-version`). Same MAJOR = compatible.
MINOR changes are additive and optional. Python rejects unknown fields (strict producer); C# ignores them
(tolerant consumer). A test fails when the schema file is out of sync with model.py.

## Consequences

+ Clear compatibility rule; forward-compatible add-in.
- Discipline needed: bump, regenerate, sync.
