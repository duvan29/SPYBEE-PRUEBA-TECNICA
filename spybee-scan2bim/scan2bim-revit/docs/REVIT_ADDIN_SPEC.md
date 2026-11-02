# Revit add-in specification

**Why an add-in instead of importing the IFC?** Revit's IFC import produces hard-to-edit elements (often
DirectShapes). Modellers need **native walls, floors and columns** they can fix with the usual grips, so
the add-in reads `building.json` and creates elements through the Revit API.

## Commands

| Command | Status | Task |
|---|---|---|
| `Spybee: Hello` | written | T0.4 |
| `Spybee: Generate model` — levels, wall/floor types, walls, floors, marking, views, shared coordinates | written, not compiled | T5.2–T5.4 |
| `Generate model` — columns, openings, rooms | TODO | T6.4 |
| `Spybee: Export corrections` — walls | written, not compiled | T7.4 |
| `Export corrections` — floors, columns, openings, rooms | TODO | T7.4 |

## Generate model — order of operations (one transaction)

1. Load + validate `building.json` (`BuildingJson.Load`, `BuildingValidator.Validate`); refuse incompatible MAJOR versions.
2. **Levels** — reuse a template level at the same elevation (±1 cm) instead of duplicating; rename; unique names.
3. **Types** — `TypeFactory`: single-layer `Spybee Wall {cm} cm` / `Spybee Floor {cm} cm` duplicated from the first basic type.
4. **Walls** — `Wall.Create(doc, line, typeId, baseLevelId, height, baseOffset, flip:false, structural:false)`;
   top constraint = `top_level`, top offset = base elevation + base offset + height − top elevation (≈ −slab thickness).
   The location line must be **Wall Centerline** (`WALL_KEY_REF_PARAM == 0`); report if the template differs.
5. **Floors** — `Floor.Create(doc, loops, floorTypeId, levelId)` (Revit 2022+); holes = extra loops; `FLOOR_HEIGHTABOVELEVEL_PARAM` = `top_offset`.
6. `doc.Regenerate()`.
7. **Columns (T6.4)** — load/locate a structural column family (rect + round) — if missing, ask the user to load
   one (`doc.LoadFamily`). Duplicate a type per section (`TypeNaming.RectColumn`). Dimension parameter names vary
   by family and language (`b`, `h`, `Width`, `Depth`, `Ancho`, `Profundidad`, `Diameter`, `Diámetro`): try the
   candidates, log which one matched. `NewFamilyInstance(point, symbol, baseLevel, StructuralType.Column)`,
   `FAMILY_TOP_LEVEL_PARAM`, rotate with `ElementTransformUtils.RotateElement` about a vertical axis.
8. **Openings (T6.4)** — v1: `doc.Create.NewOpening(wall, bottomLeft, topRight)` with points on the host axis
   (`AxisMath.PointAlong`) at absolute z = base + sill and base + sill + height. v2: door/window families
   (`NewFamilyInstance(point, symbol, hostWall, level, StructuralType.NonStructural)`), types per width × height.
9. **Rooms (T6.4)** — `doc.Create.NewRoom(level, new UV(x, y))` at each `seed`; log failures (open boundaries).
10. **Marking** — `ALL_MODEL_MARK` = Spybee id; `ALL_MODEL_INSTANCE_COMMENTS` = `AUTO conf=…` / `REVIEW conf=… reasons=…`.
11. **Views** — `00_REVIEW` (3D) and `Spybee - <level>` plans; REVIEW elements overridden in red (solid fill looked
    up by `IsSolidFill`, never by its localised name).
12. **Shared coordinates** — if `georef.crs` is not local/unknown:
    `ActiveProjectLocation.SetProjectPosition(XYZ.Zero, new ProjectPosition(E, N, Z, angle))` with E/N/Z = offset.
13. Summary dialog + log (created per class, failures, warnings suppressed).

## Point cloud in Revit (manual in the MVP)

Insert → Point Cloud → `data/out/<p>/cloud_local.las` (already in local coordinates) → **Auto – Origin to Origin**.
If Revit does not index LAS/E57 directly, convert it with ReCap to RCP without moving the origin.
Automation later: `PointCloudType.Create(doc, "rcp", path)` + `PointCloudInstance.Create(doc, typeId, Transform.Identity)`.

## Export corrections

Collect walls (later: floors, columns, openings, rooms) → match by Mark → `CorrectionsDiff` (Core) →
`corrections.json` next to `building.json`. Thresholds: axis shift > 2 cm, thickness > 5 mm, height > 2 cm.
Correction rate = (modified + deleted + created) / (generated + created). **Silent errors** = AUTO elements the
modeller still had to fix — the most important trust metric.

## Later (post-MVP)

- Shared parameters `Spybee_Id`, `Spybee_Confidence`, `Spybee_Status` + a view filter (instead of per-element overrides).
- Dockable "Review" pane: list sorted by confidence, zoom to element, mark as fixed.
- Spybee `.rte` template with the operations team's real types; automatic type mapping.
- Ribbon tab (`IExternalApplication`) instead of External Tools.
- `ModelBuilder` packaged for APS Design Automation (no UI code allowed there).
