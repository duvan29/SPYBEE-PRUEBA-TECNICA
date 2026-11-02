# Sources and how to research

## How to research (rules for Claude Code)

1. **Search locally first.** Read this repo's docs, the installed package (`help(module.func)`, `dir()`,
   `inspect.signature`, the source in `.venv/Lib/site-packages`) and, for Revit, the Object Browser on
   `RevitAPI.dll`. Local information always matches the installed version; web pages often do not.
2. **Then official docs, for the installed version**:
   - check the version first (`uv pip show <pkg>`, the Revit year);
   - use the version selector in the docs;
   - prefer API references over blog posts;
   - use the web tools (WebSearch / WebFetch) when available.
3. **Then primary sources**: papers (arXiv, journal), the authors' GitHub repository and its README/LICENSE.
4. **Then secondary sources** (blogs, forums, Stack Overflow, The Building Coder) for patterns and gotchas.
   Confirm anything important against a primary source or a quick local experiment.
5. **Never put client data in a query**: no coordinates, addresses, client or project names.
6. **Check the licence before reusing code** (see below). Reimplementing an idea from a paper is fine; copying
   code is governed by its licence.
7. **Record what you used**:
   - add a one-line source link in the code comment when the logic is non-obvious (a formula, a heuristic,
     a workaround);
   - list consulted sources in the PROGRESS.md entry for the task;
   - add durable references to the tables below.
8. If a source contradicts these docs, say so to the user (in Spanish), propose the change and record it as a
   decision or ADR.

## Licensing rules

| Licence | Use as dependency | Copy code into our repos |
|---|---|---|
| MIT, BSD, Apache-2.0, ISC, PSF | ✅ | ✅ keep the copyright/licence header (and NOTICE for Apache) |
| LGPL (e.g. IfcOpenShell) | ✅ as an unmodified library | ❌ do not copy code |
| GPL / AGPL (e.g. CloudCompare) | ⚠️ only as a separate external tool, never imported or linked | ❌ |
| CC BY-NC / "research only" / no licence | ❌ (weights, datasets or code) | ❌ |
| Proprietary SDKs (Revit API, ODA) | ✅ under their terms | ❌ |

Known non-commercial items to avoid: Sonata and Utonia weights, SpatialLM 1.x weights, OneFormer3D code,
standalone PTv3 repo, SceneScript, ScanNet, Structured3D, and repos without a licence (PolyRoom, FRI-Net).
The Pointcept codebase itself is MIT.

## Libraries (official docs)

| Topic | Source |
|---|---|
| Open3D | https://www.open3d.org/docs/release/ |
| laspy | https://laspy.readthedocs.io/ |
| pye57 | https://github.com/davidcaron/pye57 |
| PDAL (optional, CLI pipelines, reprojection) | https://pdal.io/ |
| pyproj / PROJ | https://pyproj4.github.io/pyproj/stable/ · https://proj.org/ |
| EPSG registry (check codes such as 9377, 3116) | https://epsg.io/ · https://epsg.org/ |
| Shapely 2 | https://shapely.readthedocs.io/ |
| scikit-image / OpenCV | https://scikit-image.org/docs/stable/ · https://docs.opencv.org/ |
| IfcOpenShell (API, georeference, geom) | https://docs.ifcopenshell.org/ |
| pydantic v2 | https://docs.pydantic.dev/ |
| Typer | https://typer.tiangolo.com/ |
| uv | https://docs.astral.sh/uv/ |
| ruff / mypy / pytest | https://docs.astral.sh/ruff/ · https://mypy.readthedocs.io/ · https://docs.pytest.org/ |
| CloudCompare command line | https://www.cloudcompare.org/doc/wiki/index.php/Command_line_mode |

## Revit / Autodesk

| Topic | Source |
|---|---|
| Revit API reference (per year) | https://www.revitapidocs.com/ |
| Revit API developer guide | https://help.autodesk.com/view/RVT/2025/ENU/?guid=Revit_API_Revit_API_Developers_Guide_html |
| The Building Coder (patterns, gotchas) | https://thebuildingcoder.typepad.com/ |
| Nice3point (templates, Revit API NuGet refs) | https://github.com/Nice3point |
| APS Design Automation for Revit | https://aps.autodesk.com/en/docs/design-automation/v3/developers_guide/overview/ |
| Revit coordinates (internal origin, survey point, shared coordinates) | Autodesk Revit help → "About Coordinates" |

## Standards

| Topic | Source |
|---|---|
| IFC4 (buildingSMART) — IfcMapConversion, IfcProjectedCRS | https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/ |
| buildingSMART georeferencing guidance | https://www.buildingsmart.org/ (User Guide for Geo-referencing in IFC) |
| USIBD Level of Accuracy (LOA) v3.1 | https://usibd.org/ |
| BIMForum Level of Development spec (2025, Spanish edition 2026) | https://bimforum.org/LOD/ |
| ISO 19650 / ISO 7817-1 (level of information need) | https://www.iso.org/ |
| Colombia CRS — IGAC Origen Nacional (Res. 471/2020) | https://www.igac.gov.co/ |
| Colombia national BIM strategy | https://bim.presidencia.gov.co/ |

## Scan-to-BIM research and reference code

| Item | Licence | Why it matters |
|---|---|---|
| Cloud2BIM — https://github.com/VaclavNezerka/Cloud2BIM (paper: arXiv 2503.11498) | MIT | Closest open pipeline: slabs, walls, openings, zones, IFC |
| Pointcept — https://github.com/Pointcept/Pointcept | MIT (code) | Segmentation codebase for the ML phase |
| LitePT — https://github.com/prs-eth/LitePT | MIT | Light segmentation backbone |
| RoomFormer — https://github.com/ywyue/RoomFormer | MIT | Floor-plan / room polygon reconstruction ideas |
| pyRANSAC-3D — https://github.com/leomariga/pyRANSAC-3D | Apache-2.0 | Primitive fitting (planes, cylinders) |
| SpatialLM — https://github.com/manycore-research/SpatialLM | weights NC | Read only: shows the synthetic → real domain gap |
| BIMStruct3D (EC3 2026) | check | Hybrid learned + geometric walls/doors/columns → IfcOpenShell |
| Survey: Scan-to-BIM automation (Automation in Construction, ISPRS) | — | Background reading for failure modes |

## Market references (context only)

ClearEdge3D EdgeWise, Leica Cyclone 3DR / CloudWorx, FARO As-Built, Trimble RealWorks, PointCab, Aurivus,
XGRIDS LCC for Revit, IPX BIMIT, ScanToBIM AI, Matterport BIM files, Moving Atoms, Buildots, Doxel, Avvir.
Details and numbers: `context/RESEARCH_SUMMARY.md`.

## Consulted-sources log

Add durable references here; per-task sources go into the PROGRESS.md entry.

| Date | Task | Source | Used for |
|---|---|---|---|
| 2026-11-02 | T0.0 | pyproj/PROJ EPSG:9377 (local PROJ db: "MAGNA-SIRGAS 2018 / Origen-Nacional") | CRS tests |
| 2026-11-02 | T0.0 | pye57 API (installed package introspection) | E57 reader |
