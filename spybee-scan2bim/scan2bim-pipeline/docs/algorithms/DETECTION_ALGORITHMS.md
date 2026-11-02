# Detection algorithms

Everything in the MVP is **geometric**. Parameter names refer to `src/scan2bim/resources/default.yaml`.
For every stage: a simple version that works end-to-end on the real cloud first, refinements later.
Every stage must pass on the **synthetic building** (`scan2bim synth`, exact ground truth in
`data/reference/synthetic-box/`) before running on real data.

Read before §2–§6: **Cloud2BIM** (MIT) — https://github.com/VaclavNezerka/Cloud2BIM — slabs by z-histogram,
walls, openings, IFC output. Reusing code is allowed with the MIT notice kept in the file header.

---

## §0 Reading and preparation (`inspect`, `prep`) — implemented

- **E57** (`pye57`): per-scan reading with `transform=True` (scan poses applied). One giant SLAM scan bigger than
  `io.e57_max_ram_fraction` of free RAM is refused → pre-decimate with CloudCompare (environment doc §4).
- **LAS/LAZ** (`laspy`): `chunk_iterator(io.read_chunk_points)`.
- **Down-sampling:** streaming voxel filter (`prep.voxel_size` = 1 cm); one point per voxel; 21-bit packed keys.
- **Offset:** `georef.compute_offset` (see GEOREFERENCING_AND_CRS.md).
- **Cleaning + normals (open3d):** `remove_statistical_outlier(prep.outlier_nb_neighbors, prep.outlier_std_ratio)`;
  `estimate_normals(KDTreeSearchParamHybrid(prep.normal_radius, prep.normal_max_nn))`. Normals are unsigned:
  only `|nz|` matters for horizontal/vertical classification.
- **Cloud report:** bbox, CRS guess, z-histogram peaks (zero-padded so the lowest floor / highest ceiling are
  found; min separation 6 cm because a floor and the ceiling below are one slab apart), footprint density.

## §1 Geometric checks (T2.1)

- **Levelness:** RANSAC plane on points with `|nz| > 0.95` of the largest floor; angle to z > 0.5° → warn the
  user (do not auto-correct in the MVP).
- **Dominant direction:**
  1. Take points with `|nz| < walls.vertical_normal_max_nz`.
  2. Compute the azimuth `atan2(ny, nx)` mod 90° and build a 0.5° histogram with circular smoothing.
  3. The peak is `dominant_direction_deg`.
  4. A strong secondary peak that is not at 0° or 90° from the first means a rotated wing: log it and
     regularise per zone later.

## §2 Levels (T2.2–T2.3)

1. Take horizontal points (`|nz| > levels.horizontal_normal_min_nz`) and build a z-histogram with bin
   `levels.z_hist_bin`. Find peaks (`scipy.signal.find_peaks`) with a minimum height of
   `levels.min_peak_fraction` of the horizontal points.
2. **Floor vs ceiling:** on a 0.5 m plan grid, compare the occupancy of the bands z+0.3…z+1.8 (above) and
   z−1.8…z−0.3 (below). Free space and walls above mean a **floor**; below means a **ceiling / slab soffit**.
3. **Levels:**
   - every floor peak is a level;
   - merge floor peaks closer than `levels.min_floor_to_floor` and add the reason `level_merged`
     (a split level may be real);
   - name them `Level 1…n` bottom-up; basements are renamed if the user says so;
   - add a `Roof` level at the top slab.
4. **Slab between storeys:**
   - top = floor N+1;
   - soffit = highest ceiling peak between floor N and floor N+1;
   - thickness = top − soffit.
   - If the thickness falls outside `[levels.min_slab_thickness, levels.max_slab_thickness]`, use
     `levels.default_slab_thickness` and add the reason `thickness_default`.
5. **Storey split:** storey N gets the points with z in `[floor_N − 0.05, soffit_N+1 + 0.05]` and is written to
   `work/<p>/floors/F0N.laz`.

## §3 Slabs (T2.4)

- **Points:** horizontal points within ±3 cm of the floor peak.
- **Outline:**
  - `shapely.concave_hull(MultiPoint, ratio=slabs.concave_hull_ratio)`;
  - faster alternative: raster at `slabs.raster_cell`, morphological closing, largest contour
    (`skimage.measure.find_contours` / `cv2.findContours`);
  - then `simplify(slabs.simplify_tolerance)`.
- **Orthogonalisation:** snap edges within `slabs.orthogonalize_angle_tol_deg` of the dominant direction (or its
  perpendicular), then recompute the vertices as intersections of consecutive edges.
- **Holes:** internal empty regions larger than `slabs.min_hole_area` (stair voids, shafts).
- **Confidence:** coverage (area with points / polygon area), plane RMS, and a penalty if the thickness is not
  measured.

## §4 Walls (T4.1–T4.6) — the core

### 4.1 Slices
- Main slice: `walls.slice_main` = 1.0–1.5 m above the floor (above furniture, below ceilings).
- Check slices: `walls.slice_check`.
- Only points with `|nz| < walls.vertical_normal_max_nz`. This removes floors, worktops and most noise.

### 4.2 Face detection (start with A; switch to B if A struggles)
- **A — 3D:**
  1. Run iterative RANSAC planes on the storey's vertical points
     (`segment_plane(distance_threshold=walls.ransac_distance, ransac_n=3, num_iterations=1000)`) and keep
     near-horizontal normals.
  2. Split each plane into runs with 1D DBSCAN along the plane direction (eps ≈ 0.15 m).
  3. Each run of at least `walls.min_face_length` and `walls.min_face_points` becomes a **face**: a 2D segment
     (1st–99th percentile of the projection), its normal, z range and point count.
  4. Remove the points and repeat.
  - Open3D `detect_planar_patches` can be faster on large clouds; benchmark it.
- **B — 2D:**
  1. Raster the slice at 2 cm and close it by one cell.
  2. Extract line segments (LSD: `cv2.createLineSegmentDetector`, or `skimage.transform.probabilistic_hough_line`).
  3. Refit each segment to its nearby points by least squares.

### 4.3 Pairing faces → axis + thickness
- **Candidate pair:**
  - angle ≤ `walls.parallel_angle_tol_deg`;
  - normals facing each other;
  - perpendicular distance within `walls.thickness_range`;
  - overlap ≥ 50 % of the shorter face.
- **Assignment:** greedy by score (high overlap, distance close to a catalogue value). A face can be split
  where its partner is interrupted, for example by a door.
- **Axis:** midline between the two faces, over the union of their extents. **Thickness:** mean distance.
- **Unpaired faces with free space on the other side** (façade scanned from inside only):
  - axis = face shifted `walls.default_one_face_thickness / 2` towards the empty side;
  - reasons `one_face`; status `review`.
- **Unpaired faces with low vertical continuity** are furniture or scaffolding: discard them (see 4.5).

### 4.4 Regularisation
1. **Angle snap:** rotate an axis around its midpoint onto the dominant direction (or its perpendicular) when
   within `walls.snap_dominant_tol_deg`.
2. **Collinear merge:** merge axes when
   - the perpendicular offset is ≤ `walls.collinear_offset_tol`;
   - the gap is ≤ `walls.collinear_merge_gap`;
   - the thickness is the same;
   - **and** the gap is not a confirmed opening (a door gap stays open).
3. **Joints:**
   - extend or trim free ends to the nearest intersection within `walls.join_extend_max`;
   - L-junction: both ends meet at the intersection;
   - T-junction: the end meets the **face** of the through wall.
4. **Catalogue:** snap the thickness to the nearest `walls.thickness_catalog` value; add
   `thickness_out_of_catalog` if the difference is above 2 cm.
5. Remove near-duplicate axes.

### 4.5 Heights and vertical continuity
- **Height:** from the level elevation to the soffit of the slab above. `top_level` = next level.
- **Continuity:** the share of check slices where points lie within `t/2 + 2 cm` of the axis over at least
  50 % of its length.
  - Below `walls.min_vertical_continuity`: add the reason `vertical_discontinuity`.
  - If the face was also unpaired and its points stop below 1.6 m: discard it (furniture or parapet).

### 4.6 Mandatory PNGs
- `F0X_slice.png`, `F0X_faces.png`, `F0X_walls.png` (thickness labels, `review` walls in red),
  `F0X_before_after.png`.

## §5 Columns (T6.1)

- **Free-standing:**
  1. Remove main-slice points within `t/2 + 3 cm` of any wall.
  2. Run 2D DBSCAN (eps 5 cm).
  3. Per cluster, compute `shapely.minimum_rotated_rectangle`; check that the sides are within
     `columns.size_range` and the aspect ratio ≤ `columns.max_aspect_ratio`.
  4. Fit a circle when the residual is low.
  5. Require presence in the check slices: `height_fraction ≥ columns.min_height_fraction`.
  6. Four faces seen gives high confidence; 2–3 faces means the rectangle is completed with lower confidence.
- **Embedded (optional in the MVP):**
  - every 5 cm along a wall, measure the local face offset;
  - a 20–100 cm run that bulges at least `columns.embedded_bump_min` is a candidate:
    `embedded_in` = wall, status `review`, reason `embedded`;
  - a clear colour difference (concrete vs brick) raises the confidence.

## §6 Openings (T6.2)

Per wall:
1. Take the points within `t/2 + 3 cm` of the axis, over the wall's extent.
2. Project them to (u, z): u along the axis from `axis[0]`, z from the base.
3. Raster at `openings.raster_cell`.
4. Connected empty regions are candidates. Drop regions touching the top or side edges (doors may touch the floor).
5. Fit an axis-aligned rectangle; filter by `openings.min_width`, `openings.max_width` and `openings.min_height`.
6. **See-through test:** a real opening shows points beyond the wall plane (≥ `openings.see_through_min_depth`)
   on either side; otherwise it may be a scan shadow → `review` + `occlusion_partial`.
7. **Kind:**
   - sill ≤ `openings.door_max_sill` → `door`;
   - sill ≥ `openings.window_min_sill` → `window`;
   - anything in between → `opening`.

PNGs: elevation of sample walls (raster + rectangles) and a plan per storey with openings on the axes.

## §7 Spaces (T6.3)

1. Raster per storey at `spaces.raster_cell`; draw walls (filled rectangles of their thickness) and columns.
2. Close door openings with a line so each room is separate.
3. Flood-fill the free space and label connected components inside the slab outline.
4. Drop the components smaller than `spaces.min_area` and the outside component.
5. Polygon via contour + simplification; `seed = polygon.representative_point()`; area from the polygon
   (Revit recomputes the room area from the walls).

## §8 Confidence (T7.1)

```
coverage    = share of the element surface with points within 3 cm (10 cm cells)
residual    = 1 - min(rms / 0.02, 1)                       # rms in metres
consistency = vertical continuity (walls) | height_fraction (columns) | see-through 1.0 / 0.4 (openings)
confidence  = w.coverage*coverage + w.residual*residual + w.consistency*consistency - reason_penalty*len(reasons)
```

- `status = review` when `confidence < confidence.review_threshold` or a "hard" reason is present
  (`one_face`, `occlusion_partial`, `embedded`, `thickness_default`).
- **Calibration:** with a reference model, plot confidence against correct / incorrect and pick the threshold
  that gives ≥ 95 % precision for `auto`. Record the decision.

## §9 Typical failures

| Symptom in the PNGs | Likely cause | Try |
|---|---|---|
| Double parallel walls 1–3 cm apart | Noise, or plaster and block faces on the same side | Raise `collinear_offset_tol`; check pairing |
| Many short segments | Site clutter, scaffolding | Raise `min_face_length` / `min_face_points`; require vertical continuity |
| Corners not closing | `join_extend_max` too small | 0.8 m; check the angle snap |
| Absurd thickness (> 40 cm) | Faces of different walls paired | Lower the max of `thickness_range`; require overlap |
| Extra levels | Worktops, stair landings, stacked material | Raise `min_peak_fraction`; require a minimum peak area |
| Fake openings in empty zones | Scan shadows | Require see-through |
| Model rotated a few degrees vs Revit | Someone rotated the cloud / true north confusion | **Never rotate the cloud** (GEOREFERENCING doc) |
