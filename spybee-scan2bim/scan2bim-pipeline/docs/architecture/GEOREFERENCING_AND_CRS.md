# Georeferencing, CRS and reprojection

## Principles (ADR-0004)

1. **Never rotate the cloud.** The model is built in the cloud's own frame, minus an offset. The dominant
   wall direction is only used to regularise angles.
2. **Work in local coordinates:** `local = world − offset`, computed in float64, then cast to float32.
   CTM12 coordinates are millions of metres, and float32 has only ~7 significant digits, which would cost
   decimetres.
3. **Georeferencing travels as metadata:**
   - `building.json` → `georef`;
   - IFC → `IfcMapConversion` + `IfcProjectedCRS`;
   - Revit → shared coordinates.
4. **Reproject only when necessary**, horizontally only, with pyproj, and record it.
5. **Never convert heights silently.** Ellipsoidal ↔ orthometric conversion needs a geoid model (GEOCOL)
   and is the surveyor's job. The pipeline only records which vertical reference the data uses.

## Colombian coordinate systems

| EPSG | Name | Typical magnitudes (x / y) | Notes |
|---|---|---|---|
| **9377** | MAGNA-SIRGAS 2018 / Origen-Nacional (CTM12) | ~4.3–5.9 M / ~1.0–3.0 M | **Official** (IGAC Res. 471/2020). False easting 5,000,000, false northing 2,000,000 |
| 3116 | MAGNA-SIRGAS / Colombia Bogota zone | ~0.8–1.2 M / ~0.9–1.2 M | Legacy Gauss-Krüger zone, very common in Bogotá projects |
| 3114, 3115, 3117, 3118 | MAGNA-SIRGAS Far West / West / East Central / East zones | ~1 M / ~1 M | Legacy zones |
| 4686 | MAGNA-SIRGAS geographic (lat/lon) | degrees | Never used for modelling directly |
| 32617–32619 | WGS 84 / UTM 17N–19N | 160 k–840 k / 0–1.4 M | Sometimes from GNSS / drones |
| — | Local | tens / hundreds of metres | Scanner frame; not georeferenced |

`scan2bim.georef.guess_crs()` guesses from magnitudes; **always confirm with the scan leader**.

Heights: orthometric (above sea level, about 2,600 m in Bogotá), ellipsoidal (raw GNSS), or local
(0 at the ground floor). They are recorded in `georef.vertical`.

## Offset (implemented in `scan2bim.georef.compute_offset`)

- x/y: if coordinates exceed 100 km, round the bbox **centre** to the nearest 1,000 m. Rounding the centre
  (not the floor of the minimum) makes the result robust to noise.
- z: if it exceeds 1,000 m, round the centre to the nearest 100 m.
- The result is stored in `work/<p>/georef.json` and copied to `building.json.georef.offset`.

## Reprojection (implemented in `scan2bim.georef.reproject_xy`)

```python
reproject_xy(xyz, "EPSG:3116", "EPSG:9377")   # Bogota zone -> CTM12, z unchanged
```

Rules:
- `pyproj.Transformer.from_crs(src, dst, always_xy=True)`: x = easting / longitude.
- Use it only when the project requires a different CRS than the delivery (e.g. the client wants CTM12 and the
  scan came in EPSG:3116). Reproject the **offset and the control points**, not the whole cloud, whenever possible.
  The local frame stays the same; only the georeference changes.
- Over a single building, the rotation and scale between conformal projections is small but not zero.
  If you reproject the georeference only, check a far-apart pair of control points; if the error is above
  tolerance, reproject the cloud with PDAL `filters.reprojection` or pyproj in chunks.
- Tests: round trip 3116 → 9377 → 3116 below 1 mm; Bogotá lon/lat → CTM12 inside the expected range
  (`tests/test_georef.py`).

## IFC (task T3.1)

- IFC4:
  - `IfcProjectedCRS(Name="EPSG:9377")`;
  - `IfcMapConversion(Eastings=offset.x, Northings=offset.y, OrthogonalHeight=offset.z, XAxisAbscissa=1, XAxisOrdinate=0, Scale=1)`.
- Element coordinates are **local**.
- With IfcOpenShell, use the `georeference` API module. Function names differ between 0.7, 0.8 and 0.9:
  check `help(ifcopenshell.api.georeference)` for the installed version.
- IFC2x3 has no IfcMapConversion; Revit writes `ePSet_MapConversion` property sets instead. We export IFC4.
- Verify by re-opening the file: local point + offset = world point.

## Revit (tasks T5.3–T5.4)

- Geometry is built near the **internal origin**. Revit degrades beyond about 32 km from it, so never model in
  raw CTM12 values.
- Shared coordinates: `ProjectLocation.SetProjectPosition(XYZ.Zero, ProjectPosition(E, N, Z, angle))` with
  E/N/Z = offset and angle = 0. A corner queried in shared coordinates then reports real CTM12 values.
- Link `cloud_local.las` (offset already removed) **origin to origin**. Never link the original CTM12 cloud
  origin to origin: it would land thousands of km away.

## Control points (optional, strongly recommended)

`data/raw/<p>/control_points.csv`:

```csv
id,easting,northing,elevation,method,precision_m
PC1,4880123.456,2066456.789,2601.234,total_station,0.005
PC2,4880187.012,2066470.321,2601.240,gnss_rtk,0.02
```

QA (T7.2):
- Transform each point to local coordinates and measure the distance to the nearest cloud point.
- Warn when it exceeds `qa.tol_loose` (5 cm): this points to a registration or CRS problem.
- In Revit, check one point in shared coordinates.
