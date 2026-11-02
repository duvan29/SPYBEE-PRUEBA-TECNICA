# scan2bim-pipeline — instructions for Claude Code

Read the workspace-level `../CLAUDE.md` first (language policy, workflow, hard rules).
This file adds the Python-specific rules.

## Commands

```powershell
uv sync --all-groups                 # install / update env
uv run pytest                        # tests (must stay green)
uv run ruff check --fix src tests    # lint
uv run ruff format src tests         # format
uv run mypy src                      # types
uv run scan2bim <command> -p <project>
uv run scan2bim schema               # after ANY change to model.py
```

## How to add or implement a stage (pattern)

1. Read the task in `docs/plan/EXECUTION_PLAN.md` and its algorithm section in
   `docs/algorithms/DETECTION_ALGORITHMS.md`.
2. Create `src/scan2bim/stages/<stage>.py` with a pure core and a thin runner:
   - pure functions on numpy arrays (no I/O, no globals): easy to unit test;
   - `run_<stage>(paths, cfg, meta) -> <Stage>Result` that reads inputs from `work/`, calls the core,
     writes `work/<stage>.json` and `out/debug/<stage>/*.png`, and logs counts/timings with
     `log.stage(...)`.
3. Parameters go in `resources/default.yaml` + the matching pydantic section in `config.py`.
4. Wire the CLI command in `cli.py` (replace the `_not_implemented` call).
5. Tests:
   - unit tests of the pure functions with tiny hand-made geometry;
   - a stage test on the synthetic building comparing against the ground truth
     (`reference/<p>/ground_truth.building.json`) with explicit tolerances.
6. Run on the real cloud, LOOK at the PNGs, record numbers in `PROGRESS.md`.

## Code rules

- Python ≥ 3.11, full type hints, `from __future__ import annotations` in library modules
  (not in `cli.py`: Typer needs runtime annotations).
- numpy vectorisation; KD-trees from scipy/open3d; never loop in Python over millions of points.
- Import heavy/optional libs (`open3d`, `pye57`, `ifcopenshell`, `pyproj`) inside the function that
  needs them, so the CLI starts fast and tests can skip cleanly.
- float64 until the offset is subtracted; float32 for local clouds.
- No `print` in library code — use `scan2bim.log.get_logger(__name__)`.
- Errors: raise specific exceptions with an actionable message (what to do next).
- Determinism: seeded RNGs (`np.random.default_rng(seed)`), sorted outputs, stable IDs.
- Contract changes: edit `model.py` → `uv run scan2bim schema` → bump `SCHEMA_VERSION`
  (MINOR additive, MAJOR breaking) → copy `schema/` to `../scan2bim-revit/schema/`
  (`../scan2bim-revit/scripts/sync-schema.ps1`) → update docs/architecture/BUILDING_JSON_CONTRACT.md.

Full guidelines: `docs/engineering/PYTHON_GUIDELINES.md`.
