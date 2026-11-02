# scan2bim-revit — instructions for Claude Code

Read the workspace-level `../CLAUDE.md` first (language policy, workflow, hard rules).
The program plan and PROGRESS.md live in `../scan2bim-pipeline/`. This file adds C#/Revit rules.

## Commands

```powershell
./scripts/bootstrap.ps1 -RevitVersion <year>        # sln + tests + build
dotnet test tests/Spybee.Scan2BIM.Tests/Spybee.Scan2BIM.Tests.csproj
dotnet build src/Spybee.Scan2BIM.Revit/Spybee.Scan2BIM.Revit.csproj -p:RevitVersion=<year>
./scripts/install.ps1 -RevitVersion <year>          # Revit must be CLOSED
./scripts/sync-schema.ps1                           # after the contract changes in the pipeline repo
```

You cannot click inside Revit. For anything that needs Revit, give the user short numbered steps
(in Spanish) and ask for a screenshot or the log file (`%LOCALAPPDATA%\Spybee\Scan2BIM\logs`).
Use docs/MANUAL_TEST_CHECKLIST.md.

## Rules

- **Put logic in Contracts/Core whenever it does not need the Revit API** and unit-test it there.
  The Revit project only translates data ↔ Revit elements.
- Lengths: Revit internal units are FEET → always `RevitUnits.ToInternal(m)` / `RevitUnits.ToMeters(ft)`.
- Numbers ↔ text: always `CultureInfo.InvariantCulture` (Colombian Windows uses a decimal comma).
- Never look Revit elements up by **localised names** (fill patterns, default family/type names change
  with the Revit language). Use built-in parameters, categories, classes or properties.
- One transaction per command; `IFailuresPreprocessor` to collect warnings; roll back on exceptions;
  catch specific exceptions; log everything to the log file; never let an exception escape `Execute`.
- `FilteredElementCollector`: always filter by class/category first; materialise with `ToList()` before
  modifying the document.
- Multi-version: `-p:RevitVersion=<year>` selects the framework (net8 ≥ 2025, net48 ≤ 2024) and defines
  `REVIT<year>` for `#if` blocks. Keep `#if` blocks rare and small.
- Before using an API member you are unsure about, check the docs for THAT Revit year
  (https://www.revitapidocs.com/) or inspect `RevitAPI.dll` (Object Browser) — don't guess.

Full guidelines: docs/CSHARP_REVIT_GUIDELINES.md.
