# Market and technology research — summary

Condensed from the research done on 2026-11-02 (full Spanish report and notes on branch
`claude/investigacion-scan-to-bim` of the original research repo).

> **Evidence caveat:** most pages could not be fetched in full; figures come from search-engine extracts.
> Vendor claims are marked *(vendor)*. Verify before quoting to clients.

## Where the time goes

- Manual modelling is 85–95 % of the effort. Concrete Bureau (35 projects): 75–180 modeller-hours for < 2,500 m²
  at LOD 200 (all disciplines); 2,300–5,350 h for > 15,000 m² at LOD 400. Multipliers: LOD 300–350 ≈ ×1.35,
  LOD 400 ≈ ×3.0 over LOD 200.
- Capture is already fast: ~5,000 m² in about half a day with SLAM, versus 1.5–3 days with TLS.

## What "minutes" can honestly mean

| Horizon | What fits |
|---|---|
| Minutes | Compute of a LOD 100–200 arch/struct draft (Cloud2BIM: ~60 s per test building); scan-vs-BIM comparisons |
| Hours | Reviewed LOD 200 draft, capture included (MVP target 24–48 h) |
| Days | Validated LOD 300 arch/struct |
| Weeks | MEP LOD 350–400 (assisted tools cut 50–70 % of the hours) |

No vendor sells unattended LOD 300. The fastest services (IPX BIMIT, Matterport BIM files, Moving Atoms) still
use human review. IPX BIMIT tiers: fully automatic ~US$0.43/m² delivered in hours; LOD 300 reviewed
~US$2.91/m² delivered in days *(vendor)*.

## Capture hardware (2026)

| Category | Examples | Accuracy | Role |
|---|---|---|---|
| High-end TLS | Leica RTC300/500/700, FARO Focus i.1, Trimble X9 | 1.5–2.3 mm @ 10 m | Critical zones (MEP rooms, structure, façades) |
| Mid-range SLAM | FARO Orbis, Emesent Hovermap ST-X, XGRIDS L2 Pro | 6–9 mm (independent tests) | Bulk capture |
| Premium SLAM | NavVis VLX 3/4 | ~5 mm *(vendor)* | Reference quality |
| Prosumer | Matterport Pro3, iPad LiDAR | ±20 mm / up to ±30 cm drift | Room checks only |
| Robotics | Spot + BLK ARC / X7 | — | Repeatable unattended capture, later |

**Recommendation:** hybrid capture anchored to control.
- Total-station control points on every floor.
- SLAM for the bulk of the building.
- TLS only in critical zones.

**Accuracy reporting:** datasheets quote 1σ while USIBD LOA uses 95 %, so roughly double the datasheet figure.

## Software landscape

- **Assisted extraction:** ClearEdge3D EdgeWise is the only incumbent that extracts many classes into native
  Revit families. A Cambridge study measured −67 % pipe-modelling time; EdgeWise Lite costs US$1,995/yr.
- **Revit helpers, no automatic modelling:** Leica CloudWorx, FARO As-Built, PointCab.
- **Classification or meshing only, no Revit objects:** Cyclone 3DR, Cintoo, ReCap Pro 2026.
- **AI-native newcomers:**
  - Aurivus — Revit plug-in, about €0.25/m², 25–50 % saved *(vendor)*;
  - XGRIDS LCC for Revit;
  - Moving Atoms (YC 2026) — 48 h turnaround;
  - ScanToBIM AI — about US$1.94/m² at LOD 300.
- **Consolidation:** Topcon owns ClearEdge3D, Hexagon owns Leica and Avvir, AMETEK owns FARO (2025),
  CoStar owns Matterport (2025).
- **Competition near Spybee:** Buildots accepts E57 laser scans since August 2026.

## Open source / research

- **Cloud2BIM** (MIT, Automation in Construction 2025): slabs by z-histogram, walls (non-orthogonal too),
  rectangular openings, zoning, IFC via IfcOpenShell. **Best starting reference.**
- **Pointcept** (MIT) is the state of the art for indoor segmentation:
  - PTv3: 77.6 mIoU on ScanNet;
  - LitePT (MIT, CVPR 2026): 76.5 mIoU, 21 ms, 2 GB.
- **Licences:** the strongest pretrained **weights are CC BY-NC** (Sonata, Utonia, SpatialLM, OneFormer3D,
  standalone PTv3), and so are ScanNet / Structured3D. They are **not usable commercially**, so we train our own.
- **Domain gap:** SpatialLM wall F1 drops from 94 (synthetic) to about 68 (real scans) without fine-tuning.
- **Synthetic data:** mixing synthetic data generated from BIM with real data beats real-only, and simulated
  laser scanning beats uniform sampling (+3.3 mIoU).
- **Tooling:**
  - Revit API point access is capped at 1 M points per call, so cloud processing lives outside Revit;
  - APS Design Automation costs about 2 Flex tokens per processing hour;
  - an official Revit MCP server exists (Revit 2027).

## Business

- In Bogotá, a Revit modeller earns about COP 3.5–4.0 M/month. Labour is cheap; the case for automation is
  **speed, scale and recurrence**, not salary.
- Spybee's edge comes from three things at once: recurring site presence, client design models in ACC, and its
  own scan–BIM pairs. Together they support progress monitoring (scan-vs-BIM), which is the highest recurring value.
