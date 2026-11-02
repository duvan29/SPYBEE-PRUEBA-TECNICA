# Git workflow (both repositories)

## Repositories

| Repo | Content | Default branch |
|---|---|---|
| `scan2bim-pipeline` | Python pipeline, contract, plan, PROGRESS, docs, ADRs | `main` |
| `scan2bim-revit` | C# Revit add-in | `main` |

Both repos are private and live under the Spybee GitHub organisation. The `data/` folder is never versioned:
back it up to object storage or a NAS. No Git LFS for clouds.

## Branches and commits

- **Branches:** `main` is protected (PR + green CI required). Work on short-lived branches:
  `feat/T4.3-wall-pairing`, `fix/prep-e57-memory`, `docs/georef`, `chore/ci`.
- **Commits:** Conventional Commits in English, one logical change per commit, task id when relevant.
  Examples:
  - `feat(walls): pair opposite faces into axes (T4.3)`
  - `fix(prep): guard E57 reads against free RAM`
  - `docs(contract): document opening.offset_along`
  - `chore(ci): add dotnet format check`
- **Pull requests:** use the template; link the task; attach 1–2 debug PNGs or Revit screenshots;
  squash-merge.
- **Claude Code:** commits locally after each task. It pushes or opens PRs **only when the user asks**.

## Versioning and releases

- SemVer per repo (`pyproject.toml` version / `Directory.Build.props` `Version`).
- Tags `vX.Y.Z` after each milestone (M0–M6), with a CHANGELOG entry.
- The contract has its own version (`SCHEMA_VERSION`), independent from package versions.

## Cross-repo changes (contract)

1. PR in `scan2bim-pipeline`: model.py, regenerated `schema/`, bumped `SCHEMA_VERSION`, tests, docs.
2. PR in `scan2bim-revit`: `scripts/sync-schema.ps1`, update `BuildingModel.cs` / `ContractInfo`, tests.
3. Cross-link the two PRs; merge the pipeline first, then the Revit repo.

## What never goes into git

Point clouds (`.e57`, `.las`, `.laz`, `.rcp`…), Revit/IFC models, client data, secrets and API keys
(use environment variables / a secret manager), and build outputs. The pre-commit large-file guard
(1 MB) and the `.gitignore` files enforce most of this.
