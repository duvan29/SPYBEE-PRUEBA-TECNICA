---
description: Compare the automatic model against the reference (manual model or synthetic ground truth) and update metrics
argument-hint: "[project]"
---

Reply in **Spanish**; write files in English.

1. Read `scan2bim-pipeline/docs/quality/EVALUATION_AND_PILOT.md`.
2. Project: `$ARGUMENTS`, or the one in PROGRESS.md.
3. Find the reference in `data/reference/<p>/`:
   - IFC preferred;
   - a synthetic `ground_truth.building.json` also works;
   - only an RVT: give the user Spanish steps to export it to IFC (§1);
   - nothing: run the reference-free evaluation only (deviation + % review).
4. Run `uv run scan2bim evaluate -p <p>`. If it is not implemented yet and the plan has reached Phase 7,
   implement it (task T7.3).
5. Look at the PNGs in `data/out/<p>/debug/eval/`.
6. Add a row to the **Metrics** table in PROGRESS.md: date, short commit hash, metrics.
7. Spanish summary:
   - how close we are to 80/20;
   - which class fails most and why (with image paths);
   - the top 3 improvements.
