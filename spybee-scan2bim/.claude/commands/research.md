---
description: Research a technical topic the right way (installed version first, official docs, licence check) and record the sources
argument-hint: "<topic or question>"
---

Topic: $ARGUMENTS

Follow `scan2bim-pipeline/docs/SOURCES.md` → "How to research":

1. **Local first.** Check the installed version (`uv pip show <pkg>`, Revit year) and inspect the API locally:
   `uv run python -c "import x; help(x.y)"`, `inspect.signature`, package source, Revit Object Browser.
2. **Official docs for that version** (tables in SOURCES.md), using the web tools if available. Then primary
   sources (paper, author repo + LICENSE), then secondary ones (blogs, forums) for gotchas.
3. **Never include client data** in queries: no coordinates, names or addresses.
4. If code reuse is considered, **check the licence** against the table in SOURCES.md.
5. If an API detail matters, verify it with a tiny local experiment or test.
6. Record the result:
   - durable references go in SOURCES.md → tables or the consulted-sources log;
   - task-specific ones go in the current PROGRESS.md entry;
   - add a one-line link in the code where the logic depends on it.
7. Answer the user in **Spanish**: what you found, how sure you are, what you recommend, and the sources (links).
