# Project context

## The problem

Today at Spybee, Scan-to-BIM works like this:

1. An engineer or scan leader goes to the site and scans with LiDAR.
2. The scans are registered in the scanner software.
3. Operations or a third party **models everything by hand in Revit** on top of the point cloud.

The time does not go into scanning. Across the market, manual modelling takes **85–95 % of the effort**. One
documented case logged 8 nights of scanning, 8 days of registration and 300 days of modelling. A typical
~5,000 m² project takes 6–12 weeks end to end. Outsourced modelling costs about US$1.6–2.7/m² at LOD 200 and
US$2.7–4.8/m² at LOD 300, according to vendor-published price lists. That is US$8k–24k for 5,000 m².

## What the MVP builds

A pipeline that takes **the scan leader's registered cloud** and automatically produces:

1. **`building.json`**: every detected element with a **confidence** (0–1) and a status `auto` / `review`.
2. **IFC4**: an open format that any viewer can open.
3. **A native Revit model**, built by a custom add-in: real walls, floors and columns, georeferenced via
   shared coordinates, with `REVIEW` elements in red in the `00_REVIEW` view and the cloud linked on top.
4. **A QA report**: per-element cloud-to-model deviation.

The modeller only fixes what is red. **Target: ~80 % automatic, ~20 % corrections**, measured in human hours
and not only in element counts.

## Scope

| In the MVP (LOD 200, architecture + structure) | Later |
|---|---|
| Levels and floor elevations | MEP (pipes, ducts, trays) |
| Slabs: outline + thickness | Curved walls, curtain walls, complex glazed façades |
| Straight walls (also non-orthogonal): thickness + height | Stairs, ramps, downstand beams |
| Rectangular and round columns | Hidden elements (inside walls, above ceilings) |
| Rectangular openings: openings, generic doors and windows | Client-specific families/types (LOD 300+) |
| Spaces / rooms with area | ML segmentation (after the MVP, own weights) |
| Georeferencing when the cloud has it | Cloud processing + Spybee platform UI (ROADMAP) |

**Key decision (ADR-0002):** the MVP is **geometric** (RANSAC, 2D slices, histograms, primitive fitting).
It needs no training data and works from the first cloud. ML comes later, mainly to remove site clutter
(scaffolding, materials, people).

## Colombia-specific facts

- **Common structural systems:**
  - concrete frames with 10–15 cm masonry infill;
  - in housing (especially VIS social housing), **industrialised cast-in-place concrete walls**
    8–12 cm thick, with **no columns**.
- On a shell building, a column embedded in a brick wall is almost coplanar with it. Colour or intensity can
  separate concrete from brick. In the MVP these are flagged `review`.
- **Typical floor-to-floor height:**
  - housing: 2.3–2.7 m;
  - offices / retail: 3.0–4.0 m.
- **Official CRS:** Origen Nacional **CTM12, EPSG:9377** (IGAC Resolution 471 of 2020). Older projects use the
  MAGNA-SIRGAS Gauss-Krüger zones EPSG:3114–3118; the Bogotá zone is EPSG:3116.
- **Usual deliverables:** RVT, IFC, DWG floor plans (for municipal *curaduría* permits).
- **National BIM strategy:** Colombia's 2020–2026 strategy makes BIM mandatory for national public projects
  from 2026. Existing-conditions and as-built models appear among the official BIM uses, but no rule found
  requires scan-based as-builts.

## Glossary

| Term | Meaning |
|---|---|
| Point cloud | Millions of XYZ points (+ colour / intensity) from the scanner |
| E57 / LAS / LAZ | Open cloud formats; LAZ is compressed LAS |
| RCP/RCS, FLS, LGS | Proprietary Autodesk ReCap / FARO / Leica formats; export to E57 |
| Registration | Merging individual scans into one consistent cloud |
| SLAM / TLS | Walking mobile scanner / static tripod terrestrial laser scanner |
| LOD | Level of Development (detail). 200 = approximate geometry, generic types; 300 = precise geometry, specific types |
| LOA | Level of Accuracy (USIBD). LOA20 = 15 mm–5 cm; LOA30 = 5–15 mm (95 % confidence) |
| IFC | Open BIM format (IFC4 is current) |
| Shared coordinates | Revit mechanism to place a model in real-world coordinates without moving geometry |
| HITL | Human-in-the-loop: the machine proposes, a person approves or fixes |
| P/R | Precision / recall: fraction of detections that are right / fraction of real elements found |
| Silent error | An element marked `auto` that the modeller still had to fix (worst for trust) |
