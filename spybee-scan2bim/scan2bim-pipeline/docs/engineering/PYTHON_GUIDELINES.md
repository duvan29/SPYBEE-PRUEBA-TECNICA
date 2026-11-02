# Python guidelines

## Project setup

- **src layout** (`src/scan2bim`): tests always run against the package, not loose files.
- **uv** for environments, locking and running:
  - commit `pyproject.toml` + `uv.lock`;
  - `.python-version` pins 3.12;
  - fall back to 3.11 only if a wheel is missing on Windows.
- **Dependencies**:
  - runtime goes in `[project.dependencies]`, dev tools in `[dependency-groups].dev`;
  - add new ones with `uv add <pkg>` / `uv add --dev <pkg>`;
  - check the licence before adding anything (SOURCES.md → Licensing rules).
- **Tooling**:
  - ruff (lint + format, line length 100);
  - mypy (typed defs required);
  - pytest + coverage;
  - pre-commit (ruff, whitespace, YAML/TOML/JSON checks, **large-file guard 1 MB**, schema sync).
- **CI**: GitHub Actions on Windows and Ubuntu. Synthetic data only; real clouds never leave the PC.

## Code structure

- **Pure core, thin runner.**
  - Algorithms are functions on numpy arrays with explicit parameters (no I/O, no globals, no config objects
    deep inside).
  - Stage runners do the I/O, logging and PNGs.
- **Typed data.**
  - pydantic models at boundaries (contract, config, project metadata) with `extra="forbid"`;
  - dataclasses for internal results;
  - `NDArray[np.float64]` annotations for arrays.
- **Configuration.** Every tunable lives in `resources/default.yaml` and the matching pydantic section;
  projects override in `data/projects/<p>.yaml`.
- **CLI.** Typer, thin: parse arguments, resolve paths, call `run_<stage>`, print where the output is.
- **Imports.** Heavy or optional libraries (`open3d`, `pye57`, `ifcopenshell`, `pyproj`) are imported inside the
  function that uses them, so CLI start-up stays fast and tests can skip cleanly.
- **Errors.** Specific exceptions with actionable messages ("Export an E57 from …").
- **Logging.** `scan2bim.log.get_logger`, never `print` in library code; `log.stage()` gives timings + peak RAM.

## Point cloud specifics

- **Memory:** stream in chunks; down-sample before accumulating; estimate memory before loading
  (points × bytes per point vs free RAM); `del` big arrays early.
- **Precision:** float64 for world coordinates, float32 for local ones (after the offset).
- **Vectorise:** use numpy broadcasting, `np.unique`, `np.bincount`, KD-trees (`scipy.spatial.cKDTree` /
  open3d). Never write Python loops over points. If a loop over elements is unavoidable, keep the per-element
  work vectorised.
- **Determinism:** seeded RNG (`np.random.default_rng(seed)`, seeds in config), sorted outputs, stable IDs, so
  the same input gives the same `building.json`.
- **Debug PNGs** for every stage, headless matplotlib (`viz.py`), at most ~2000 px, metre axes.

## Testing

- **Unit tests** for pure functions use tiny hand-made geometry (an L-shaped wall pair, a slab with a hole).
- **Stage tests** run on the synthetic building with explicit tolerances against the ground truth.
- Mark tests that need real data with `@pytest.mark.realdata` (they never run in CI) and slow ones with
  `@pytest.mark.slow`.
- **Contract tests:** the schema file must equal `json_schema()`, the example must validate, and each
  integrity rule has a negative test.
- A bug found on real data gets a minimal synthetic reproduction as a regression test whenever possible.

## Performance budget (5,000 m² building, office PC)

`prep` ≤ 20 min, every other stage ≤ 10 min, `run-all` ≤ 90 min. Measure with `log.stage()`; profile with
`python -m cProfile -o out.prof` + snakeviz, or `py-spy`, before optimising.

## Notebooks

Allowed only in `notebooks/` for exploration, with outputs stripped before commit. Anything reused becomes a
function in `src/` with a test.
