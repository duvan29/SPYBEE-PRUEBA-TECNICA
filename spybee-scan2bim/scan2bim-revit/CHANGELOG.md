# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-02

### Added
- Solution layout: Contracts (netstandard2.0), Core (netstandard2.0), Revit add-in (net8/net48 by `RevitVersion`), xUnit tests.
- building.json contract mirror (schema 0.1.0), loader with version check, integrity validator.
- Core: axis math, unit helpers, culture-invariant type naming and review labels, walls corrections diff.
- Revit: `Hello`, `Generate model` (levels, walls, floors, review marking, `00_REVIEW` view, plans, shared coordinates), `Export corrections` (walls).
- Scripts: bootstrap, install/uninstall, schema sync. CI for the Revit-free projects.

### Known gaps
- Not compiled yet (no .NET SDK / Revit in the scaffolding environment) — task T0.4.
- Columns, openings and rooms are TODO (T6.4).
