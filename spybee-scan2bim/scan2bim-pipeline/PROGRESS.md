# Progress — Spybee Scan2BIM MVP

> Program-level status for BOTH repositories (pipeline + revit). Claude updates this file at the end
> of every task. Always in English.

## Current status

- **Current phase:** 0 — Setup
- **Last completed task:** T0.0 (scaffolding delivered with the kit; verified on Linux with synthetic data)
- **Next task:** T0.1
- **Last session:** —

## Test project

*Filled during `/kickoff`.*

| Field | Value |
|---|---|
| Project name (folder) | |
| Cloud files (path, format, size) | |
| Points / scans | |
| Scanner and registration software | |
| Georeferenced? CRS (EPSG) / vertical | |
| Storeys and floor-to-floor height | |
| Building state (shell / finishing / occupied) | |
| Reference model (RVT / IFC) available? | |
| Revit version | |
| PC: CPU / RAM / GPU / free disk | |

## Metrics

*Updated by `/evaluate`. Definitions in docs/quality/EVALUATION_AND_PILOT.md.*

| Date | Commit | Walls P/R | Slabs P/R | Columns P/R | Openings P/R | Wall axis err (median) | % review | Compute time |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## Log

<!-- One entry per task:
### YYYY-MM-DD — T#.# Task name
- Done:
- Result (numbers, PNG paths):
- Issues / follow-ups:
-->

### 2026-11-02 — T0.0 Scaffolding (delivered with the kit)
- Done: pipeline repo (contract, config, IO, georef, synthetic generator, `inspect`, `prep`, CLI stubs,
  tests, CI, pre-commit); revit repo (Contracts, Core, Revit add-in skeleton with levels/walls/floors,
  review marking, xUnit tests, install scripts).
- Result: pipeline — 34 tests green, ruff + mypy clean (Linux, Python 3.13). Synthetic end-to-end
  `synth → inspect → prep` OK (2.16 M points, offset [4880000, 2066000, 2600], peaks at
  z = -0.003 / 2.471 / 2.59 / 5.084 as expected).
- Issues / follow-ups: the C# solution has **not been compiled yet** (no .NET SDK / Revit in the
  build environment) → first C# task T0.4 builds and fixes it. open3d normals not exercised
  (no graphics libs in the build environment) → verify in T1.4.

## Decisions

See also docs/adr/.

| Date | Decision | Why |
|---|---|---|
| 2026-11-02 | Two repos: Python pipeline + C# Revit add-in, contract = building.json | ADR-0001 |
| 2026-11-02 | Geometric-first MVP, ML later with own weights | ADR-0002 |

## Blockers and open questions for the team

- [ ] 
