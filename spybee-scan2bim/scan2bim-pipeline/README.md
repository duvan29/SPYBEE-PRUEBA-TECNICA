# scan2bim-pipeline

Spybee Scan2BIM — **Python pipeline** that turns a registered point cloud (E57 / LAS / LAZ) into a
`building.json` (levels, slabs, walls, columns, openings, spaces + per-element confidence), an IFC4
model, and the data the Revit add-in ([`scan2bim-revit`](../scan2bim-revit)) uses to build a native,
georeferenced Revit model.

> Target: ~80 % of a LOD 200 architecture + structure model generated automatically, ~20 % corrected
> by a modeller in Revit (elements flagged `review`). See [docs/context/PROJECT_CONTEXT.md](docs/context/PROJECT_CONTEXT.md).

## Quick start (Windows, PowerShell)

```powershell
# one-time: install uv  ->  https://docs.astral.sh/uv/getting-started/installation/
uv sync --all-groups              # creates .venv with Python 3.12 + all deps (incl. dev)
uv run pre-commit install         # lint/format/large-file guard on every commit
uv run pytest                     # all green before you touch anything
uv run scan2bim doctor            # machine + environment report

# try it on a synthetic building (known ground truth)
uv run scan2bim synth
uv run scan2bim inspect -p synthetic-box
uv run scan2bim prep -p synthetic-box

# real project (cloud copied to ../data/raw/<project>/)
uv run scan2bim init-project -p torre-norte     # then fill ../data/projects/torre-norte.yaml
uv run scan2bim inspect -p torre-norte
uv run scan2bim prep -p torre-norte
```

The data folder is resolved as `--data-root` › `$SCAN2BIM_DATA_ROOT` › `./data` › `../data`.
Point clouds and models **never** go into git.

## Commands

| Command | Status | Task |
|---|---|---|
| `doctor` | ✅ implemented | T1.1 |
| `init-project` | ✅ implemented | T1.2 |
| `synth` | ✅ implemented | T0.5 |
| `schema` | ✅ implemented (writes `schema/building.schema.json` + example) | — |
| `inspect` | ✅ implemented | T1.3 |
| `prep` | ✅ voxel + offset; normals/outliers need open3d | T1.4 |
| `levels`, `slabs` | ⏳ planned | T2.x |
| `export` (JSON / IFC / local cloud) | ⏳ planned | T2.5, T3.x |
| `walls` | ⏳ planned | T4.x |
| `columns`, `openings`, `spaces` | ⏳ planned | T6.x |
| `qa`, `evaluate`, `run-all` | ⏳ planned | T7.x |

## Layout

```
src/scan2bim/
  cli.py            Typer CLI (thin: parses args, calls stages)
  model.py          building.json contract (pydantic) — SINGLE SOURCE OF TRUTH
  config.py         typed config; defaults in resources/default.yaml
  project.py        data/projects/<p>.yaml metadata + overrides
  paths.py          data folder layout
  georef.py         CRS guess, local offset, reprojection (pyproj)
  synthetic.py      synthetic building + ground truth
  io/               streaming readers (E57/LAS/LAZ) and writers
  stages/           one module per pipeline stage
  viz.py            debug PNGs
schema/             generated JSON Schema + example (synced to scan2bim-revit)
tests/              pytest (synthetic data only in CI)
docs/               plan, architecture, algorithms, engineering guidelines, ADRs, sources
```

## Documentation

Start at [docs/README.md](docs/README.md). The execution plan is
[docs/plan/EXECUTION_PLAN.md](docs/plan/EXECUTION_PLAN.md); status lives in [PROGRESS.md](PROGRESS.md).

## License

Proprietary — Spybee. Third-party dependencies keep their own licenses (see
[docs/SOURCES.md](docs/SOURCES.md#licensing-rules)).
