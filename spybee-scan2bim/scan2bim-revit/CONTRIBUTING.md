# Contributing

1. Branch from `main` (`feat/T6.4-openings`, `fix/...`), Conventional Commits in English.
2. `dotnet test` green; the add-in builds for the Revit version in use (`./scripts/bootstrap.ps1`).
3. Anything that touches Revit behaviour: run the relevant items of `docs/MANUAL_TEST_CHECKLIST.md` and
   attach a screenshot to the PR.
4. Contract changes come **from the pipeline repo**; here you only run `./scripts/sync-schema.ps1`
   and adapt `BuildingModel.cs` / `ContractInfo`.

See `../scan2bim-pipeline/docs/engineering/GIT_WORKFLOW.md` and `docs/CSHARP_REVIT_GUIDELINES.md`.
