---
description: Execute the next pending task of the execution plan (or the given task id, e.g. /next T4.2)
argument-hint: "[task id, e.g. T4.2]"
---

Reply in **Spanish**; write code, docs and PROGRESS.md in English.

1. Read `scan2bim-pipeline/PROGRESS.md` and `scan2bim-pipeline/docs/plan/EXECUTION_PLAN.md`.
2. Pick the task:
   - `$ARGUMENTS`, if given;
   - otherwise the first unchecked `- [ ]` task whose prerequisites are done.
3. Read everything under the task's **Read**, plus the `CLAUDE.md` of the repo(s) it touches (`[P]` pipeline,
   `[R]` revit).
4. Tell the user in Spanish (2–4 lines) what you will do and the "Done when" criterion.
5. Implement:
   - algorithms: synthetic ground truth test first, then the real cloud;
   - Revit behaviour: give numbered Spanish steps from `scan2bim-revit/docs/MANUAL_TEST_CHECKLIST.md` and
     ask for a screenshot or the log.
6. Verify:
   - pipeline: `uv run pytest`, `uv run ruff check src tests`, `uv run mypy src`;
   - C#: `dotnet test`;
   - **open and look at the debug PNGs**;
   - check "Done when" with numbers.
7. If it passes:
   - tick `- [x]`;
   - add a PROGRESS.md log entry (done / numbers + PNG paths / issues / consulted sources);
   - update "Current status";
   - update CHANGELOG.md if user-visible;
   - commit with a Conventional Commit message.
8. If it does not pass after reasonable attempts: log the blocker, propose a simplification, ask the user.
9. **🎯 milestone:** stop and present the results in Spanish. Otherwise say which task is next and ask whether
   to continue. If the user already asked for several tasks in a row, continue until the next milestone.
