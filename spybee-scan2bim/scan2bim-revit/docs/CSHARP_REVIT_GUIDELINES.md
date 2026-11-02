# C# / Revit API guidelines

## Repository and build

- **Layered solution**: `Contracts` (data) → `Core` (pure logic) → `Revit` (API glue). Tests target
  Contracts + Core only; aim to move every non-Revit decision into Core so it is testable.
- **SDK pinning** with `global.json`; **central package management** (`Directory.Packages.props`);
  shared settings in `Directory.Build.props` (nullable on, latest C#, analyzers, deterministic builds).
  Enable `TreatWarningsAsErrors` once the first build is clean (T0.4).
- **Multi-version Revit**: `-p:RevitVersion=<year>` → net8.0-windows for 2025+, net48 for ≤ 2024; output in
  `bin/<Config>/Revit<year>/`; `REVIT<year>` compile constant for the rare version-specific code
  (e.g. `ElementId.Value` from 2024 vs `IntegerValue` before).
- **Revit references**: local install with `Private=false` (never copy RevitAPI.dll). For CI builds of the
  add-in without Revit, switch to the `Nice3point.Revit.Api.RevitAPI` / `RevitAPIUI` reference packages
  (pick the version matching the Revit year on nuget.org; mark them `PrivateAssets="all"` and exclude runtime).
- **Install** by copying the build to a private folder under `%APPDATA%\Autodesk\Revit\Addins\<year>\Spybee.Scan2BIM\`
  and writing the `.addin` manifest that points there (scripts/install.ps1). Revit must be closed.
- netstandard2.0 projects: avoid APIs missing there (`HashCode`, `Math.Clamp`, `Index/Range`, `init`, records,
  `string.Contains(char)`); keep them dependency-light.

## Code style

- `.editorconfig` is the source of truth: PascalCase members, `_camelCase` private fields, braces always,
  block-scoped namespaces, `var` only when the type is obvious.
- Nullable reference types on; treat Revit API returns as possibly null (`get_Parameter(...)?.Set(...)`).
- Public types and members get XML doc comments when the intent is not obvious.
- **Culture**: always `CultureInfo.InvariantCulture` for number ↔ string (Colombian Windows formats 0.15 as "0,15").
- No magic numbers for tolerances: named constants or settings.

## Revit API practices

- **Units**: internal length unit is the foot. Convert at the boundary (`RevitUnits`), never in between.
- **Transactions**: one per command (`TransactionMode.Manual`); `ReadOnly` for commands that do not modify.
  Use `TransactionGroup` if a command needs several steps the user should undo at once.
- **Failures**: attach an `IFailuresPreprocessor` to delete warnings and count them; let errors roll back.
- **Exceptions**: catch specific types (`Autodesk.Revit.Exceptions.*`, `ContractException`, `IOException`);
  log with stack trace; return `Result.Failed` with a helpful `message`. Never let exceptions escape `Execute`.
- **Collectors**: filter by class/category first (`OfClass`, `OfCategory`) — quick filters before slow ones;
  `ToList()` before modifying the document; never iterate the whole database without a filter.
- **Localisation**: never find elements by default names (`"<Solid fill>"`, `"Level 1"`, family names). Use
  built-in parameters, `BuiltInCategory`, `IsSolidFill`, `WallKind.Basic`, etc.
- **Regenerate** after creating hosts (walls) and before hosted elements / rooms.
- **Coordinates**: build geometry near the internal origin; georeference only through shared coordinates
  (`ProjectLocation.SetProjectPosition`). Never model at CTM12 magnitudes (> 32 km from origin degrades precision).
- **No UI in builders**: `ModelBuilder` and friends must not call `TaskDialog`/dialogs — the commands do. This
  keeps the door open to APS Design Automation.
- **Logging**: every command logs start, inputs, counts and failures to the log file.

## Testing

- Unit tests (xUnit) for Contracts/Core: contract fixtures are **linked** from `schema/` (synced from the pipeline).
- Inside Revit: `docs/MANUAL_TEST_CHECKLIST.md` (screenshots attached to the PR). Optional later:
  Revit test frameworks (e.g. ricaun.RevitTest) for automated in-Revit tests.

## References

- Revit API docs per year: https://www.revitapidocs.com/
- Autodesk Revit API developer guide: https://help.autodesk.com/view/RVT/2025/ENU/?guid=Revit_API_Revit_API_Developers_Guide_html
- The Building Coder (Jeremy Tammik): https://thebuildingcoder.typepad.com/
- Revit SDK samples (shipped with the Revit SDK download)
- Nice3point Revit templates and API packages: https://github.com/Nice3point
- APS Design Automation for Revit: https://aps.autodesk.com/en/docs/design-automation/v3/developers_guide/overview/
