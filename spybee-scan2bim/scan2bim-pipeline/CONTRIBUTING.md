# Contributing

1. Branch from `main`: `feat/T4.3-wall-pairing`, `fix/prep-e57-memory`, `docs/...`.
2. Small commits in English using [Conventional Commits](https://www.conventionalcommits.org/):
   `feat(walls): pair opposite faces into axes (T4.3)`.
3. Before pushing: `uv run ruff check --fix src tests && uv run ruff format src tests && uv run mypy src && uv run pytest`.
4. Open a PR using the template; CI must be green; one approval.
5. Update `PROGRESS.md` and, for user-visible changes, `CHANGELOG.md`.

Details: [docs/engineering/GIT_WORKFLOW.md](docs/engineering/GIT_WORKFLOW.md) and
[docs/engineering/PYTHON_GUIDELINES.md](docs/engineering/PYTHON_GUIDELINES.md).
