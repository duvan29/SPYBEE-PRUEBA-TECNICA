# Changelog

All notable changes to this project are documented here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-02

### Added
- Repository scaffolding: `uv` project, ruff, mypy, pytest, pre-commit, CI (Windows + Ubuntu).
- `building.json` contract v0.1.0 (`scan2bim.model`) with integrity validation, JSON Schema and example.
- Typed configuration with per-project overrides (`scan2bim.config`, `resources/default.yaml`).
- Readers for E57 / LAS / LAZ (streaming), LAS/LAZ writer.
- Georeferencing helpers: CRS guess, round local offset, pyproj reprojection (horizontal only).
- Synthetic building generator with exact ground truth.
- Stages: `doctor`, `init-project`, `synth`, `schema`, `inspect`, `prep` (voxel + offset; normals with open3d).
- CLI stubs for every other stage, pointing to their task in the execution plan.
