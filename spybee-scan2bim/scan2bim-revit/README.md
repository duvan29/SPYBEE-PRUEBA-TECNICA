# scan2bim-revit

Spybee Scan2BIM — **Revit add-in (C#)** that reads the `building.json` produced by
[`scan2bim-pipeline`](../scan2bim-pipeline) and creates a **native, georeferenced Revit model**:
levels, walls, floors (and next: columns, openings, rooms). Elements the pipeline is unsure about are
marked `REVIEW` and drawn in red in the `00_REVIEW` view, so the modeller only fixes those.

> ⚠️ Status: scaffolding delivered without access to Revit or the .NET SDK — **the solution has not
> been compiled yet**. Task **T0.4** (docs/plan in the pipeline repo) builds it, fixes compile errors
> and runs the smoke test.

## Solution layout

| Project | Target | Depends on Revit? | Purpose |
|---|---|---|---|
| `src/Spybee.Scan2BIM.Contracts` | netstandard2.0 | No | C# mirror of the building.json contract + loader + validator |
| `src/Spybee.Scan2BIM.Core` | netstandard2.0 | No | Geometry helpers, type naming, review labels, corrections diff |
| `src/Spybee.Scan2BIM.Revit` | net8.0-windows (Revit 2025+) / net48 (≤ 2024) | **Yes** | External commands, model builder |
| `tests/Spybee.Scan2BIM.Tests` | net8.0 | No | xUnit tests for Contracts + Core (run in CI) |

Keeping all logic that does not need Revit in Contracts/Core makes it unit-testable on any machine and
reusable later in Autodesk Platform Services **Design Automation** (Revit in the cloud).

## Quick start (Windows, PowerShell)

```powershell
# prerequisites: .NET SDK 8+, Revit installed (e.g. 2025)
./scripts/bootstrap.ps1 -RevitVersion 2025   # creates the .sln, runs tests, builds the add-in
./scripts/install.ps1  -RevitVersion 2025    # close Revit first; installs for the current user
```

In Revit: **Add-Ins (Complementos) → External Tools (Herramientas externas)**:

| Command | What it does |
|---|---|
| `Spybee: Hello` | Installation check (shows versions + log folder) |
| `Spybee: Generate model` | Pick `building.json` → native levels / walls / floors, Mark + Comments, `00_REVIEW` view, plans per level, shared coordinates |
| `Spybee: Export corrections` | Pick the original `building.json` → writes `corrections.json` (walls in v1) |

Logs: `%LOCALAPPDATA%\Spybee\Scan2BIM\logs`.

## Contract sync

The Python repo owns the contract. After it changes:

```powershell
./scripts/sync-schema.ps1        # copies schema/ from ../scan2bim-pipeline and runs the tests
```

If the MAJOR/MINOR version changed, update `ContractInfo.SupportedSchemaVersion` and `BuildingModel.cs`.

## Docs

- [docs/REVIT_ADDIN_SPEC.md](docs/REVIT_ADDIN_SPEC.md) — what each command must do, API notes
- [docs/CSHARP_REVIT_GUIDELINES.md](docs/CSHARP_REVIT_GUIDELINES.md) — coding standards and Revit API best practices
- [docs/MANUAL_TEST_CHECKLIST.md](docs/MANUAL_TEST_CHECKLIST.md) — what to verify by hand inside Revit
- Program plan, progress and ADRs live in the pipeline repo: `../scan2bim-pipeline/docs/`.

## License

Proprietary — Spybee.
