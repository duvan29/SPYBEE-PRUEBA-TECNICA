# building.json contract (schema 0.1.0)

`building.json` is the **only** interface between the Python pipeline and the Revit add-in.

| Artefact | Location | Role |
|---|---|---|
| Source of truth | `src/scan2bim/model.py` (pydantic) | Defines and validates the contract |
| JSON Schema | `schema/building.schema.json` (generated: `uv run scan2bim schema`) | Language-neutral spec, carries `x-schema-version` |
| Example | `schema/examples/building.example.json` (generated, deterministic) | Fixture for both repos |
| C# mirror | `scan2bim-revit/src/Spybee.Scan2BIM.Contracts/BuildingModel.cs` | Deserialisation in Revit |

## Conventions

- Units: **metres and degrees**.
- Coordinates: **local** = world − `georef.offset`; z up. Plan points are `[x, y]`; heights are relative to the
  element's base level.
- Polygons: counter-clockwise, first vertex not repeated, valid (no self-intersections).
- Every element has `id`, `confidence` (0–1), `status` (`auto` | `review`), `reasons` (list of codes) and
  `metrics` (free numeric diagnostics).
- IDs are stable and readable: `L1…`/`LR` levels, `S-0001` slabs, `W-0001` walls, `C-0001` columns,
  `O-0001` openings, `R-0001` spaces. Assigned by storey, then position. Revit stores them in `Mark`.

## Structure (abridged — see the example file for a complete instance)

```jsonc
{
  "schema_version": "0.1.0",
  "generator": { "name": "scan2bim", "version": "0.1.0", "git": "abc1234", "created": "…Z", "config_hash": "…" },
  "project": { "id": "torre-norte", "name": "Torre Norte", "capture_date": "2026-10-28", "scanner": "…", "building_state": "shell" },
  "georef": { "crs": "EPSG:9377", "offset": { "x": 4880000.0, "y": 2066000.0, "z": 2600.0 }, "true_north_deg": 0.0, "vertical": "orthometric" },
  "dominant_direction_deg": 12.4,
  "levels":   [ { "id": "L1", "name": "Level 1", "elevation": 0.0, "confidence": 0.98, "status": "auto", "reasons": [], "metrics": {} } ],
  "slabs":    [ { "id": "S-0001", "level": "L2", "outline": [[0,0],[24.5,0],[24.5,18.2],[0,18.2]], "holes": [], "top_offset": 0.0, "thickness": 0.12, "…": "…" } ],
  "walls":    [ { "id": "W-0001", "base_level": "L1", "top_level": "L2", "axis": [[12.403,5.210],[18.950,5.212]], "thickness": 0.15,
                  "base_offset": 0.0, "height": 2.48, "faces_seen": 2, "material_guess": "masonry", "…": "…" } ],
  "columns":  [ { "id": "C-0001", "base_level": "L1", "top_level": "L2", "center": [6.0,4.0], "shape": "rect", "size": [0.30,0.50], "rotation_deg": 12.4, "embedded_in": null } ],
  "openings": [ { "id": "O-0001", "host": "W-0001", "kind": "door", "offset_along": 2.10, "width": 0.90, "height": 2.10, "sill": 0.0 } ],
  "spaces":   [ { "id": "R-0001", "level": "L1", "polygon": [[0.15,0.15],[6.2,0.15],[6.2,4.9],[0.15,4.9]], "seed": [3.2,2.5], "area": 28.7, "name_guess": null } ],
  "summary":  { "counts": {}, "review_counts": {}, "timings_s": {} }
}
```

Field semantics:
- **wall.height** — clear height from the base (level + base_offset) to the underside of the slab above.
- **wall.axis** — centre line. In Revit the location line must be *Wall Centerline*.
- **slab.thickness** — measured downwards from the top face, which sits at level elevation + `top_offset`.
- **opening.offset_along** — distance from `host.axis[0]` to the opening edge closest to `axis[0]`.
- **opening.sill** — relative to the host wall base.
- **column.rotation_deg** — rotation of side `b` from the local x axis.
- **column.size** — `[b, h]` for `rect`, `[d]` for `circle`.

## Review reasons

| Code | Meaning |
|---|---|
| `one_face` | Wall seen from one side only; thickness assumed |
| `low_coverage` | < ~50 % of the surface has points |
| `high_residual` | Fit RMS high (irregular surface or noise) |
| `vertical_discontinuity` | Not continuous in height (furniture / parapet?) |
| `thickness_out_of_catalog` | Measured thickness far from catalogue values |
| `non_orthogonal` | Outside the dominant direction (may be right; review) |
| `occlusion_partial` | Partly occluded opening/element |
| `embedded` | Column embedded in a wall |
| `thickness_default` | Slab thickness not measured |
| `clutter` | Heavy clutter area |
| `level_merged` | Two close peaks merged into one level |

## Integrity rules (enforced by model.py and C# `BuildingValidator`)

- Same MAJOR `schema_version`.
- Unique ids across all classes.
- References exist (levels, host walls).
- Wall axis is not zero-length.
- Thickness / height > 0.
- Rect columns have 2 sizes, circles 1.
- `offset_along + width ≤ host length (+1 cm)`.
- Polygons are valid.
- Unknown fields are rejected in Python (`extra="forbid"`) and ignored in C# (forward compatibility).

## Versioning and change process

- SemVer on `SCHEMA_VERSION`:
  - **PATCH**: documentation or validation tightening only;
  - **MINOR**: additive optional fields;
  - **MAJOR**: renames, removals, semantic changes.
- Process:
  1. Edit `model.py`, then add or adjust tests.
  2. `uv run scan2bim schema` (the schema and example are regenerated; the sync test fails until you do).
  3. Bump `SCHEMA_VERSION`; update this document and `CHANGELOG.md`.
  4. In `scan2bim-revit`: `./scripts/sync-schema.ps1`, update `BuildingModel.cs` and
     `ContractInfo.SupportedSchemaVersion`, then `dotnet test`.
  5. Two PRs (one per repo) that reference each other; merge the pipeline first.

## Mapping

| building.json | IFC4 | Revit |
|---|---|---|
| level | IfcBuildingStorey | Level |
| slab | IfcSlab (FLOOR) | Floor |
| wall | IfcWall | Wall (basic type with that thickness) |
| column | IfcColumn | Structural column (FamilyInstance) |
| opening door/window | IfcOpeningElement + IfcDoor/IfcWindow | v1 Opening in wall; v2 door/window family |
| space | IfcSpace | Room |
| id / confidence / status | Pset_SpybeeScan2BIM | Mark / Comments (v1); shared parameters (v2) |
