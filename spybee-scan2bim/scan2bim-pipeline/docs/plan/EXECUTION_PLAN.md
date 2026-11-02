# Execution plan — Scan2BIM MVP

**How to use (Claude):** take the first unchecked task → read everything under **Read** → implement →
verify against **Done when** (numbers + LOOK at the PNGs) → tick it, log it in `PROGRESS.md`, commit →
at 🎯 milestones stop and show the user (summary in Spanish).

**Repos:** `[P]` = scan2bim-pipeline (Python), `[R]` = scan2bim-revit (C#), `[U]` = needs the user (Revit, data, decisions).

**Principle:** end-to-end and ugly first, then good. Every phase leaves something the team can see.
Algorithms: pass on the synthetic building (exact ground truth) → then the real cloud.

Estimated effort is in working days with Claude Code; regular buildings and clean clouds go faster.

---

## Phase 0 — Workspace and toolchain (day 0–1)

- [x] **T0.0 Scaffolding** — delivered with the kit (see PROGRESS.md log).

- [ ] **T0.1 `[U]` Workspace in place**
  - Unzip to a short path (`C:\spybee\scan2bim`), cloud in `data/raw/<p>/`, optional manual model in `data/reference/<p>/`.
  - **Done when:** `data/raw/<p>/` contains a `.e57`/`.las`/`.laz` (export from proprietary formats if needed).
  - **Read:** workspace `README.md`, `engineering/ENVIRONMENT_SETUP_WINDOWS.md` §5.

- [ ] **T0.2 `[P][R][U]` Git and GitHub**
  - `git init -b main` in each repo, first commit (`chore: initial scaffolding`). If the user wants: create two
    private GitHub repos, push, protect `main` (PR + green CI required).
  - **Done when:** both repos have a first commit; remotes configured if requested.
  - **Read:** `engineering/GIT_WORKFLOW.md`.

- [ ] **T0.3 `[P]` Python environment on Windows**
  - Install `uv`; `uv sync --all-groups`; `uv run pre-commit install`; `uv run pytest`; `uv run ruff check src tests`; `uv run mypy src`.
  - If an import fails (open3d / pye57 wheels), try Python 3.11 (`uv python pin 3.11`) before anything else.
  - **Done when:** all green on Windows; `uv run scan2bim doctor` output pasted in PROGRESS.md.
  - **Read:** `engineering/ENVIRONMENT_SETUP_WINDOWS.md`, `engineering/PYTHON_GUIDELINES.md`.

- [ ] **T0.4 `[R][U]` C# build — first compile ever**
  - Install .NET SDK 8; `./scripts/bootstrap.ps1 -RevitVersion <year>` in `scan2bim-revit`.
  - **Expect compile errors** (the code was written without Revit): fix them one by one, checking each API member
    in the Revit API docs for that year. Keep behaviour as specified in `docs/REVIT_ADDIN_SPEC.md`.
  - `./scripts/install.ps1`; the user runs checklist A (Hello).
  - Then enable `TreatWarningsAsErrors` and add `dotnet format --verify-no-changes` to CI.
  - **Done when:** `dotnet test` green, add-in builds for the installed Revit, `Spybee: Hello` works (screenshot).
  - **Read:** `scan2bim-revit/CLAUDE.md`, `scan2bim-revit/docs/CSHARP_REVIT_GUIDELINES.md`, `MANUAL_TEST_CHECKLIST.md` §A.

- [ ] **T0.5 `[P]` Synthetic sanity check on Windows**
  - `uv run scan2bim synth`, `inspect -p synthetic-box`, `prep -p synthetic-box` (with normals → verifies open3d).
  - **Done when:** PNGs show the 12 × 8 m box with the interior wall and the column; `prep` reports `normals=True`.

- [ ] **T0.6 `[R][U]` Revit smoke test with the example contract**
  - The user runs `Spybee: Generate model` on `scan2bim-revit/schema/examples/building.example.json` (checklist B).
  - **Done when:** 2 levels, 5 native walls, 2 floors; wall tops under the slab; `00_REVIEW` view exists.

🎯 **M0 — Toolchain ready:** both repos green on Windows; native walls appear in Revit from a JSON.

---

## Phase 1 — Cloud intake (day 1–2)

- [ ] **T1.1 `[P]` Machine report** — `scan2bim doctor` → PROGRESS.md "Test project" table (PC row).
- [ ] **T1.2 `[P][U]` Project metadata**
  - `uv run scan2bim init-project -p <p>`; ask the user ONE grouped question (Spanish) for the fields of
    `data/projects/<p>.yaml` (storeys, floor-to-floor, CRS, scanner, state, Revit version, reference model).
  - **Done when:** the YAML is filled; unknowns listed under "open questions" in PROGRESS.md.
- [ ] **T1.3 `[P]` `inspect` on the real cloud** (already implemented — verify and tune)
  - **Done when:** `out/<p>/cloud_report.md` + 4 PNGs; dimensions, z-peaks and CRS guess are plausible and
    confirmed by the user. If an E57 is too big for RAM, follow the CloudCompare pre-decimation path.
  - **Read:** `architecture/GEOREFERENCING_AND_CRS.md`.
- [ ] **T1.4 `[P]` `prep` on the real cloud** (implemented — verify, tune, harden)
  - Voxel 1 cm, outlier removal + normals (open3d). If the working cloud exceeds ~150 M points or RAM, raise
    `prep.voxel_size` (1.5–2 cm) in the project overrides — record the decision.
  - **Done when:** `work/<p>/cloud_work.laz`, `normals.npz`, `georef.json`; time + peak RAM logged; PNG checked.

🎯 **M1 — Cloud validated:** the team confirms the cloud report (storeys, size, coordinates).

---

## Phase 2 — Levels and slabs (day 2–3)

- [ ] **T2.1 `[P]` Geometric checks** (`levels` stage, part 1)
  - Levelness (floor normals vs z, warn > 0.5°); dominant wall direction (azimuth histogram mod 90°).
  - **Done when:** `debug/levels/azimuth_hist.png` has a clear peak; synthetic dominant direction = 0° ± 0.5°.
  - **Read:** `algorithms/DETECTION_ALGORITHMS.md` §1.
- [ ] **T2.2 `[P]` Levels**
  - z-histogram of horizontal points, peaks, floor vs ceiling classification, level elevations.
  - **Done when:** synthetic: 2 levels + roof within 1 cm of ground truth; real: count and floor-to-floor match the
    metadata within ±3 cm; `debug/levels/z_peaks.png`.
  - **Read:** §2.
- [ ] **T2.3 `[P]` Per-storey split** — `work/<p>/floors/F01.laz…` + one plan PNG per storey; no empty storey.
- [ ] **T2.4 `[P]` Slabs**
  - Outline (concave hull or raster contour), simplification, orthogonalisation, holes; measured thickness.
  - **Done when:** synthetic: IoU ≥ 0.95 with ground-truth outline, thickness ± 1 cm; real: PNG per slab looks right.
  - **Read:** §3.
- [ ] **T2.5 `[P]` `export` v0 — building.json**
  - Assemble levels + slabs into a `Building` (model.py validates it), deterministic IDs, generator info
    (version, git hash, config hash), georef from `georef.json`.
  - **Done when:** `out/<p>/building.json` validates; test round-trips it.
  - **Read:** `architecture/BUILDING_JSON_CONTRACT.md`.

## Phase 3 — First IFC (day 3)

- [ ] **T3.1 `[P]` IFC4 writer (IfcOpenShell)**
  - Project/site/building/storeys/slabs in **metres**; `IfcMapConversion` + `IfcProjectedCRS` when georeferenced;
    `Pset_SpybeeScan2BIM` (SpybeeId, Confidence, Status). Verify API names with `help()` for the installed version.
  - **Done when:** `out/<p>/model.ifc` re-opens with ifcopenshell; entity counts match building.json.
  - **Read:** `architecture/GEOREFERENCING_AND_CRS.md` §IFC, `SOURCES.md` (IfcOpenShell).
- [ ] **T3.2 `[P]` Local cloud for Revit** — `out/<p>/cloud_local.las` (2.5 cm, local coordinates); bbox matches building.json.
- [ ] **T3.3 `[U]` Visual check in Revit** — link `model.ifc` + insert `cloud_local.las` origin-to-origin; screenshot.

🎯 **M2 — First demo:** slabs and levels sit on the cloud inside Revit.

---

## Phase 4 — Walls (day 4–6) — the heart of the MVP

**Read for all tasks:** `algorithms/DETECTION_ALGORITHMS.md` §4. Reference implementation worth reading
first: Cloud2BIM (MIT) — see `SOURCES.md`.

- [ ] **T4.1 `[P]` Slices** — per storey: main slice 1.0–1.5 m, check slices 0.5–0.9 and 1.6–2.0 m; vertical-normal points only. PNG per storey.
- [ ] **T4.2 `[P]` Face detection** — option A (3D RANSAC planes + 1D DBSCAN) or B (2D raster + line segments). PNG with faces.
- [ ] **T4.3 `[P]` Pair faces → axis + thickness** — one-face walls get the default thickness and `review` (`one_face`).
- [ ] **T4.4 `[P]` Regularisation** — snap to dominant direction (±3°), merge collinear, close L/T joints, thickness to catalogue. Before/after PNG.
- [ ] **T4.5 `[P]` Heights + vertical continuity** — height to slab soffit; discard furniture/parapets; log counts.
- [ ] **T4.6 `[P]` Walls into building.json + IFC**
  - **Done when (synthetic):** all 10 walls found, axis error ≤ 1 cm, thickness exact, no extras, door gap not merged.
  - **Done when (real):** PNG per storey reviewed with the user; if a reference exists, preliminary wall P/R logged.

🎯 **M3 — Walls:** per-storey images + IFC in Revit; review with the user what is missing / extra.

## Phase 5 — Native Revit from the real building (day 7–8)

- [ ] **T5.1 `[R][U]`** `Generate model` on the real building.json (levels, walls, floors) — checklist B.
- [ ] **T5.2 `[R][U]`** Review marking validated — checklist C (a `review` wall is red, Comments correct).
- [ ] **T5.3 `[R][U]`** Shared coordinates + point cloud — checklist D (control point within a few cm if available).
- [ ] **T5.4 `[R]`** Fix whatever T5.1–T5.3 revealed; log decisions (e.g. template, level reuse).

🎯 **M4 — Second demo:** the modeller opens a native RVT over the cloud and navigates it.

## Phase 6 — Columns, openings, spaces (day 9–11)

- [ ] **T6.1 `[P]` Columns** — free-standing (clusters → min-area rectangle / circle, height check); embedded (wall bumps) as `review`. Synthetic: both columns found, size ± 1 cm. §5.
- [ ] **T6.2 `[P]` Openings** — per-wall (u, z) raster, rectangular holes, see-through confirmation, door/window by sill. Synthetic: door + window per storey, size ± 3 cm. §6.
- [ ] **T6.3 `[P]` Spaces** — raster with walls drawn, doors closed, flood fill, polygons + seeds + areas. Synthetic: 4 spaces, area ± 2 %. §7.
- [ ] **T6.4 `[R][U]`** Revit: columns (family + types per section), openings (v1 `NewOpening`), rooms (`NewRoom`) — `REVIT_ADDIN_SPEC.md` §7–9.

🎯 **M5 — Complete LOD 200 architecture + structure model** of the test building.

## Phase 7 — Confidence, QA, evaluation, one command (day 12–13)

- [ ] **T7.1 `[P]` Confidence** — coverage + residual + consistency − reason penalties; calibrate threshold so `auto` precision ≥ 95 % (when a reference exists). §8.
- [ ] **T7.2 `[P]` `qa`** — `out/<p>/qa.html`: per-element RMS / % within 2 and 5 cm / coverage, heatmap per storey, control-point errors.
- [ ] **T7.3 `[P]` `evaluate`** — vs `data/reference/<p>/` (IFC) or synthetic ground truth: P/R per class, axis/thickness errors → `eval.json` + PROGRESS metrics row. `quality/EVALUATION_AND_PILOT.md` §1–3.
- [ ] **T7.4 `[R]` Export corrections — all classes** (walls done; add floors, columns, openings, rooms) — checklist E.
- [ ] **T7.5 `[P]` `run-all`** — raw → building.json + IFC + local cloud + QA in one command, timings per stage, resumable.

## Phase 8 — Pilot with operations (day 14–15)

- [ ] **T8.1 `[U]`** A modeller who did not build the tool corrects the generated RVT to "deliverable LOD 200", **with a stopwatch** (review red / fix silent errors / add missing).
- [ ] **T8.2 `[R][P]`** Export corrections → correction rate per class, hours per 1,000 m², **silent errors**; compare with historical manual hours / third-party invoice.
- [ ] **T8.3 `[P]`** `out/<p>/pilot_report.md`: metrics, top-5 failures with images, next 3 improvements, go/no-go for Phase 9+.

🎯 **M6 — MVP result:** did we reach 80/20? With which numbers, and what next.

---

After the MVP: `ROADMAP.md` (more buildings, ML segmentation, **Spybee platform integration**, progress
monitoring, MEP).
