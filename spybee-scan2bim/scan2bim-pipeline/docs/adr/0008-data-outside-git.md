# ADR-0008: Data outside git, synthetic data in CI

- Status: Accepted
- Date: 2026-11-02

## Context

Point clouds are tens to hundreds of GB and belong to clients.

## Decision

A shared `data/` folder outside both repositories (raw read-only, projects, reference, work, out). Never in git
(no LFS). CI uses only the synthetic building generator; real-data tests are marked `realdata` and run locally.
Client data is never uploaded or used in web queries without explicit permission; training on client scans
requires a contract clause.

## Consequences

+ Small repos, privacy by default, reproducible CI.
- Real-data regressions depend on local runs; back up data/ separately.
