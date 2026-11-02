# Data folder (shared by both repos, never committed)

```
data/
├── raw/<project>/            What the pipeline reads: the scan leader's deliverable. READ-ONLY.
│   ├── *.e57 | *.las | *.laz (every cloud file here is read — no duplicates)
│   └── control_points.csv    (optional) id,easting,northing,elevation,method,precision_m
├── originals/<project>/      (optional) huge originals archived when a decimated copy is used in raw/
├── projects/<project>.yaml   Project metadata + parameter overrides (`scan2bim init-project -p <project>`)
├── reference/<project>/      Hand-made model of the same building, for evaluation
│   ├── manual_model.rvt
│   └── manual_model.ifc      (Revit → Export → IFC)
├── work/<project>/           Intermediates (safe to delete and regenerate)
│   ├── cloud_work.laz        working cloud, LOCAL coordinates
│   ├── normals.npz
│   ├── georef.json           CRS + offset (world = local + offset)
│   └── floors/F01.laz ...
└── out/<project>/            Deliverables
    ├── cloud_report.md/json  from `inspect`
    ├── building.json         the contract consumed by the Revit add-in
    ├── model.ifc             IFC4
    ├── cloud_local.las       decimated local cloud to link in Revit (origin to origin)
    ├── qa.html               per-element deviation report
    ├── eval.json             metrics vs reference
    ├── corrections.json      exported from Revit after review
    └── debug/<stage>/*.png   images Claude must look at
```

Rules:
- `<project>`: lowercase letters, digits and `-` only (e.g. `torre-norte`).
- The pipeline finds this folder via `--data-root`, `$SCAN2BIM_DATA_ROOT`, `./data` or `../data`.
- Back up `raw/` and `reference/` outside this PC (object storage / NAS). Never in git.
- Before using a client's scans to **train** models, a contract clause must allow it.
