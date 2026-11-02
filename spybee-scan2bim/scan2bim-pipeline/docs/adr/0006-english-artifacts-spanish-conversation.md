# ADR-0006: English artefacts, Spanish conversation

- Status: Accepted
- Date: 2026-11-02

## Context

The team is Colombian; code and docs should follow industry practice and be shareable with any engineer or
vendor.

## Decision

Everything written to the repositories is in English: code, comments, docs, PROGRESS.md, commits, PRs,
reports. Claude Code talks to the user in Spanish and summarises results in Spanish.

## Consequences

+ Consistent, searchable, vendor-friendly codebase; users still get explanations in their language.
- Some user-facing Revit names (types, views) are English; can be localised later via configuration.
