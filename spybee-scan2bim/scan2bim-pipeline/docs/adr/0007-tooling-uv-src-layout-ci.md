# ADR-0007: Python tooling: uv, src layout, ruff, mypy, pytest, pre-commit, CI

- Status: Accepted
- Date: 2026-11-02

## Context

Reproducible environments on Windows workstations and CI, with low friction for a small team.

## Decision

uv with pyproject.toml + uv.lock, src layout, ruff (lint + format), mypy, pytest with synthetic fixtures,
pre-commit (incl. a 1 MB large-file guard), GitHub Actions on Windows + Ubuntu. C#: global.json, central
package management, Directory.Build.props, xUnit, CI on Windows for Revit-free projects.

## Consequences

+ One command to set up (`uv sync`), fast checks, no accidental point clouds in git.
- uv is newer than pip/conda; fallback documented (Python 3.11 pin).
