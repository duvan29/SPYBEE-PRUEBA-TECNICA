---
description: First session — toolchain on Windows, both repos green, first look at the point cloud
---

This is the **first session** of the Spybee Scan2BIM MVP. Reply to the user in **Spanish**; write every file
in English.

1. Read `CLAUDE.md`, `README.md`, `scan2bim-pipeline/CLAUDE.md`, `scan2bim-revit/CLAUDE.md`,
   `scan2bim-pipeline/PROGRESS.md`, `scan2bim-pipeline/docs/context/PROJECT_CONTEXT.md`,
   `scan2bim-pipeline/docs/plan/EXECUTION_PLAN.md` and
   `scan2bim-pipeline/docs/engineering/ENVIRONMENT_SETUP_WINDOWS.md`.
2. Greet the user in Spanish and explain in about 5 lines what today's session covers:
   Phase 0, then Phase 1 if time allows.
3. Check what is installed: git, uv, dotnet, Revit (which years), CloudCompare. List what is missing with
   links, and **ask before installing** anything heavy.
4. Ask **one grouped question** (Spanish) for the project data that is still missing:
   - project folder name;
   - Revit version;
   - number of storeys and floor-to-floor height;
   - CRS and vertical reference, if known;
   - scanner and registration software;
   - building state;
   - whether a hand-made reference model exists.

   Unknowns go to the open questions in PROGRESS.md.
5. Execute **T0.2 → T0.6** in order, following the session loop in `CLAUDE.md`. Expect T0.4, the first C#
   compile, to need fixes.
6. If time remains, continue with **T1.1 → T1.4** on the real cloud. If the cloud is in a format Python cannot
   read (`.rcp`, `.rcs`, `.fls`, `.lgs`), stop and give the export instructions (environment doc §5).
7. Finish with:
   - a Spanish summary: what works, the cloud report (key numbers), PNG paths, blockers, next task;
   - PROGRESS.md updated (English);
   - commits made.

$ARGUMENTS
