# Spybee Scan2BIM — workspace

Goal: **give the pipeline a point cloud and get back a native, georeferenced Revit model** (levels,
slabs, walls, columns, openings, spaces) where the modeller only fixes what is flagged in red.
Target: ~80 % automatic, ~20 % corrections (LOD 200 architecture + structure).

The work is done by **Claude Code** on this PC, guided by the files in this folder. The team reviews the
results at each milestone. Claude talks to you in Spanish; everything it writes (code, docs, progress) is
in English.

## Contents

| Path | What |
|---|---|
| `CLAUDE.md` | Standing instructions for Claude Code (language policy, workflow, hard rules) |
| `.claude/commands/` | `/kickoff`, `/next`, `/evaluate`, `/status`, `/research` |
| `data/` | Point clouds and outputs — never committed (see `data/README.md`) |
| `scan2bim-pipeline/` | **Repo 1 — Python**: pipeline + plan + PROGRESS.md + docs + building.json contract |
| `scan2bim-revit/` | **Repo 2 — C#**: Revit add-in that builds the native model from building.json |

What is already built (delivered with this kit):
- **Python**: contract + JSON Schema, config, E57/LAS/LAZ streaming readers, georeferencing/reprojection,
  synthetic building with ground truth, `doctor`, `inspect`, `prep`; 34 tests, ruff + mypy clean, CI.
- **C#**: Contracts + Core libraries with xUnit tests, Revit add-in with `Hello`, `Generate model`
  (levels, walls, floors, review marking, views, shared coordinates) and `Export corrections` (walls).
  ⚠️ Not compiled yet — that is the first C# task (T0.4).

## Getting started (tomorrow)

1. Unzip to a **short path without spaces**, e.g. `C:\spybee\scan2bim\`.
2. Copy the point cloud to `data\raw\<project>\` (e.g. `data\raw\torre-norte\`). Never edit it.
   Proprietary formats (`.rcp`, `.fls`, `.lgs`): also export an **E57** from the scanner software
   (`scan2bim-pipeline/docs/engineering/ENVIRONMENT_SETUP_WINDOWS.md`).
3. If the hand-made Revit model of the same building exists, put it in `data\reference\<project>\`
   (+ an IFC export of it). It lets us measure how good the automation is.
4. Install Git, Claude Code, `uv` and the .NET SDK 8 (links in the environment doc).
5. Open a terminal in this folder and run `claude`, then type **`/kickoff`**.
6. In later sessions type **`/next`**. Check progress anytime in `scan2bim-pipeline/PROGRESS.md` or with `/status`.

Have at hand: Revit version, number of storeys and floor-to-floor height, whether the cloud is
georeferenced (and in which system, e.g. CTM12 / EPSG:9377), scanner + software used, building state
(shell / finishing / occupied).

## Repositories on GitHub

Create two **private** repos (e.g. `spybee/scan2bim-pipeline`, `spybee/scan2bim-revit`), then in each folder:

```powershell
git init -b main; git add .; git commit -m "chore: initial scaffolding"
git remote add origin <url>; git push -u origin main
```

Claude can do this in task T0.2 when you ask it to.

## Plan at a glance

| Days | Visible result |
|---|---|
| 0–1 | Both repos green on Windows, `Hello` in Revit, cloud report |
| 2–3 | 🎯 Levels + slabs as IFC over the cloud |
| 4–6 | 🎯 Walls detected (per-storey images) |
| 7–8 | 🎯 **Native Revit** with levels, walls, floors over the cloud |
| 9–11 | Columns, openings, spaces |
| 12–13 | Confidence, QA report, evaluation, one end-to-end command |
| 14–15 | 🎯 Pilot: a modeller corrects with a stopwatch → do we reach 80/20? |

After the MVP: more buildings, ML segmentation, and the **Spybee platform interface** (upload → automatic
processing → review → download). See `scan2bim-pipeline/docs/plan/ROADMAP.md`.
