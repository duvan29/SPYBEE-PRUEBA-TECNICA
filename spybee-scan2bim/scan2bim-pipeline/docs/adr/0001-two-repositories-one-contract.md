# ADR-0001: Two repositories, one contract

- Status: Accepted
- Date: 2026-11-02

## Context

Scan-to-BIM needs heavy point-cloud processing (Python ecosystem: numpy, Open3D, IfcOpenShell) and native
Revit authoring (C#, Revit API, Windows-only, version-specific builds).

## Decision

Two repositories: `scan2bim-pipeline` (Python) and `scan2bim-revit` (C#). The only interface is
`building.json`, owned by `scan2bim-pipeline/src/scan2bim/model.py`; its JSON Schema and example are synced
to the Revit repo. The pipeline repo also hosts the program plan, PROGRESS.md, docs and ADRs.

## Consequences

+ Each repo uses its native tooling, CI and release cadence; Revit-free logic is testable anywhere.
+ The Revit side can later run in APS Design Automation unchanged.
- Contract changes need two coordinated PRs (process in BUILDING_JSON_CONTRACT.md).
