# Spybee Scan2BIM workspace — instructions for Claude Code

## Language policy (non-negotiable)

- **Talk to the user in Spanish** (Colombian, plain language). Briefly explain technical terms in Spanish.
  Every task ends with a short Spanish summary: what was done, the numbers, where to look, what's next.
  When the user must do something in Revit, give numbered steps in Spanish and include the Spanish UI
  names in parentheses (e.g. "Add-Ins (Complementos) → External Tools (Herramientas externas)").
- **Write everything else in English**: code, comments, docstrings, identifiers, commit messages, PR
  descriptions, documentation, PROGRESS.md, reports, logs, file names.

## What this is

Spybee (construction tech, Colombia) does Scan-to-BIM by scanning with LiDAR and modelling everything by
hand in Revit (weeks to months). This workspace builds the **MVP of an automated pipeline**:

`point cloud (E57/LAS/LAZ) → Python detects levels, slabs, walls, columns, openings, spaces → building.json
→ IFC4 + native Revit model (C# add-in) → the modeller fixes only what is flagged REVIEW`

Target: ~80 % automatic / ~20 % corrections, LOD 200 architecture + structure. Context:
`scan2bim-pipeline/docs/context/PROJECT_CONTEXT.md`.

## Workspace layout

```
spybee-scan2bim/                 <- open Claude Code HERE
├── CLAUDE.md                    (this file)
├── .claude/commands/            /kickoff /next /evaluate /status /research
├── data/                        point clouds + outputs (NEVER in git) - see data/README.md
├── scan2bim-pipeline/           repo 1: Python pipeline. Owns the plan, PROGRESS.md, docs, ADRs and
│                                the building.json contract (model.py -> schema/)
└── scan2bim-revit/              repo 2: C# Revit add-in (Contracts, Core, Revit, Tests)
```

Each repo has its own `CLAUDE.md` with language-specific rules — read it before touching that repo.

## Session loop

1. Read `scan2bim-pipeline/PROGRESS.md` and find the **first unchecked task** in
   `scan2bim-pipeline/docs/plan/EXECUTION_PLAN.md` (or the one the user names).
2. Read every document the task lists under **Read**, plus the CLAUDE.md of the repo you will touch.
3. Tell the user in Spanish (2–4 lines) what you will do and the acceptance criterion.
4. Implement in small steps. Algorithms: make them pass on the **synthetic building** (exact ground truth)
   first, then run them on the real cloud.
5. Verify: tests + lint + types green; **open and look at the debug PNGs** (Read tool); check the
   acceptance criterion with numbers. Never mark a task done without looking at its images.
6. Record: tick the task, add a PROGRESS.md log entry (English), update CHANGELOG.md if user-visible,
   commit with a Conventional Commit message (`feat(walls): ... (T4.3)`).
7. At milestones (🎯) stop, show results (Spanish summary + file paths) and wait for the user's OK.
8. Blocked for more than ~1 hour of attempts: log it in PROGRESS.md, propose a simpler path, ask the user.

Priority: **speed with visible results**. End-to-end first, then improve. Do not over-engineer.

## Hard rules

- `data/raw/` is **read-only**. Never modify, move or delete anything there.
- Never load a whole point cloud blindly: stream in chunks, down-sample, check free RAM first.
- Units: metres in Python and in building.json; Revit internal units are **feet** (convert at the boundary).
- Coordinates: read in float64; subtract a round offset (CTM12 values are millions of metres); work local.
- **Never rotate the cloud.** The dominant wall direction is only used for regularisation.
- `building.json` is the contract between repos. It is owned by `scan2bim-pipeline/src/scan2bim/model.py`.
  Change flow: model.py → `uv run scan2bim schema` → bump SCHEMA_VERSION → `scan2bim-revit/scripts/sync-schema.ps1`
  → update C# `BuildingModel.cs`/`ContractInfo` → docs.
- Parameters live in config (`resources/default.yaml` + per-project overrides), never hard-coded.
- **Licensing**: only commercially usable dependencies and code (MIT, BSD, Apache-2.0, LGPL as a library).
  Never use CC BY-NC weights or datasets (Sonata, Utonia, SpatialLM, OneFormer3D, ScanNet, Structured3D…).
- **Client data stays on this machine**: never upload clouds/models, and never paste client coordinates,
  names or addresses into web searches or external services, unless the user explicitly allows it.
- Ask before installing heavy software (CUDA, Visual Studio, multi-GB packages).
- Do not push to remotes or open PRs unless the user asks.

## Researching external sources

Follow `scan2bim-pipeline/docs/SOURCES.md` → "How to research" (or run `/research <topic>`):
official docs for the **installed** version first; verify API signatures locally (`help()`, `dir()`,
Revit Object Browser) before relying on them; check the licence before reusing any code; cite the source
in a code comment when the logic is non-obvious and list consulted sources in the PROGRESS.md entry.

## Commands

| Command | Use |
|---|---|
| `/kickoff` | First session: environment, both repos green, first look at the cloud |
| `/next [T#.#]` | Execute the next pending task (or the given one) |
| `/evaluate [project]` | Compare against the manual reference model, update metrics |
| `/status` | Short status in Spanish |
| `/research <topic>` | Consult external sources the right way and record them |
