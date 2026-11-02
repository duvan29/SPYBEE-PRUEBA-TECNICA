# Manual test checklist (inside Revit)

Claude cannot click inside Revit: it gives these steps to the user (in Spanish) and asks for screenshots
or the log file (`%LOCALAPPDATA%\Spybee\Scan2BIM\logs`). Run the relevant block before merging a change.

## A. Installation (T0.4)
- [ ] `./scripts/install.ps1 -RevitVersion <year>` finishes without errors (Revit closed).
- [ ] Revit asks to trust the add-in once → "Always load".
- [ ] Add-Ins → External Tools shows the three `Spybee:` commands.
- [ ] `Spybee: Hello` shows the add-in version, schema 0.1.0 and the log folder.

## B. Generate model on the synthetic example (T5.2–T5.3)
Use `schema/examples/building.example.json` (or `data/out/synthetic-box/building.json` once `export` exists).
- [ ] New project from the metric architectural template → `Spybee: Generate model` → pick the JSON.
- [ ] Summary dialog: levels 2, walls 5, floors 2; failures only for not-yet-implemented classes.
- [ ] Walls are native (select one → grips, type `Spybee Wall 15 cm` / `10 cm` in Properties).
- [ ] Wall axes centred: measure from a wall face to the axis = thickness / 2.
- [ ] Wall tops stop under the slab above (top offset ≈ −0.12 m).
- [ ] Mark = `W-000x`, Comments = `AUTO conf=1.00`.
- [ ] Views `00_REVIEW` and `Spybee - Level 1` exist.
- [ ] Re-running on the same project does not duplicate levels (it does duplicate walls — expected in v1).

## C. Review marking (T5.3)
- [ ] Edit the JSON: set one wall `"status": "review"`, `"reasons": ["one_face"]` → regenerate in a new project.
- [ ] That wall is red in `00_REVIEW` and in the plan; Comments = `REVIEW conf=… reasons=one_face`.

## D. Coordinates + point cloud (T5.4)
- [ ] Manage → Coordinates → Report Shared Coordinates on a wall corner: E/N ≈ offset + local coordinates.
- [ ] Insert → Point Cloud → `cloud_local.las` (Origin to Origin): the cloud sits on the walls (few cm).
- [ ] If control points exist: their reported shared coordinates match the CSV within a few cm.

## E. Export corrections (T7.4)
- [ ] Move one wall 10 cm, change one wall type, delete one wall, draw one new wall.
- [ ] `Spybee: Export corrections` → dialog: 2 modified, 1 deleted, 1 created; `corrections.json` written next to the JSON.
