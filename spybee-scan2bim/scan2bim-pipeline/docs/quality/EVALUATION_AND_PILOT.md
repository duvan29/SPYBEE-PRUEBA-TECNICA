# Evaluation, metrics and pilot

The MVP must answer one question: **does the machine do ~80 % and the person ~20 %?** Three levels of evidence:

1. **No reference:** internal metrics — cloud-to-model deviation, % of elements in `review`.
2. **With reference:** compare against the hand-made model of the same building (`evaluate`), or against the
   synthetic ground truth.
3. **Real pilot:** a modeller corrects the generated RVT with a stopwatch. **This is the number that matters.**

## §1 Preparing the reference

In Revit, with the manual model open:
1. File → Export → IFC (IFC4 Reference View, or IFC2x3 CV 2.0).
2. Coordinates: **Shared** if the model is georeferenced, otherwise **Internal**.
3. Save the file as `data/reference/<p>/manual_model.ifc`.

`evaluate` must:
- convert IFC units to metres (`ifcopenshell.util.unit.calculate_unit_scale`; Revit often exports millimetres);
- bring the reference into the local frame (subtract the offset if it is in world coordinates);
- **check the alignment**: compute the median distance from the reference wall axes to the cloud. If it is
  above 10 cm, estimate a rigid 2D transform (ICP between reference and detected axes), apply it, **report it**.

Reading the reference with IfcOpenShell:
- walls: `Axis` representation + `ifcopenshell.util.placement.get_local_placement`; thickness from
  `IfcMaterialLayerSetUsage`, or from the geometry (`ifcopenshell.geom`) when there is no Axis;
- slabs: 2D footprint + top z;
- columns: centre + section;
- openings: `IfcOpeningElement` / `IfcDoor` / `IfcWindow` on the host;
- levels: `IfcBuildingStorey.Elevation`.

## §2 Matching and metrics

Greedy one-to-one matching by best score:

| Class | Match rule | Metrics |
|---|---|---|
| Levels | \|Δz\| ≤ 5 cm | Recall, mean elevation error |
| Walls | same storey, angle ≤ 5°, axis distance ≤ 10 cm, overlap ≥ 50 % of the shorter | P/R, median and p90 axis error (cm), % thickness correct (±1 cm), % length covered |
| Slabs | same level, footprint IoU ≥ 0.7 | P/R, mean IoU, thickness error |
| Columns | same storey, centre ≤ 15 cm | P/R, section error |
| Openings | matched host wall, centre ≤ 30 cm, width ±15 cm | P/R per kind |
| Spaces | IoU ≥ 0.7 | P/R, area error % |

Also report:
- **confidence calibration** (precision of `auto` vs `review`);
- compute time per stage.

Outputs:
- `out/<p>/eval.json`;
- `debug/eval/*.png` (reference grey, true positives green, false positives red, misses blue);
- a new row in PROGRESS.md.

## §3 MVP targets

| Metric | MVP target | Note |
|---|---|---|
| Level recall | 100 % | Elevation error ≤ 3 cm |
| Wall P/R | ≥ 90 % / ≥ 85 % | Product target 95 % |
| Wall axis error (median) | ≤ 2 cm | p90 ≤ 5 cm |
| Wall thickness correct | ≥ 80 % | One-face walls pull this down |
| Slab P/R | ≥ 95 % | |
| Column P/R | ≥ 85 % | Free-standing; embedded measured separately |
| Opening P/R | ≥ 70 % | Hardest class; expected in the 20 % |
| Precision of `auto` | ≥ 95 % | Otherwise raise the confidence threshold |
| Compute, 5,000 m² | ≤ 90 min | On the office PC |
| **Correction rate (pilot)** | **≤ 20–30 %** | (modified + deleted + created) / (generated + created) |
| **Human hours per 1,000 m² (pilot)** | **measure; target ≤ 2.5 h** for LOD 200 arch+struct | Compare with historical manual hours |
| **Silent errors (pilot)** | as low as possible; report per class | `auto` elements that still needed fixing |

These targets are hypotheses. Adjust them with real data and record the change in PROGRESS.md → Decisions.

## §4 Pilot protocol (Phase 8)

1. **Modeller:** someone from operations who knows the standard and did **not** build the tool.
2. **Inputs:**
   - the generated RVT with the cloud linked;
   - the `00_REVIEW` view;
   - `qa.html`;
   - the instruction "make it a deliverable LOD 200 arch+struct to the Spybee standard".
3. **Stopwatch:** effective time only, split into:
   - (a) reviewing red elements;
   - (b) fixing unflagged errors (silent errors);
   - (c) adding missing elements.
4. **Export:** `Spybee: Export corrections` → `corrections.json`.
5. **Ten-minute interview:**
   - What was most annoying?
   - What did you trust or distrust?
   - What saved the most time?
6. **Compute:**
   - correction rate per class;
   - hours per 1,000 m²;
   - silent errors.
7. **Compare with the baseline:** real manual hours for a similar building (ops records or the third party's
   invoice) and cost per m².
8. **Write** `out/<p>/pilot_report.md` (T8.3).
