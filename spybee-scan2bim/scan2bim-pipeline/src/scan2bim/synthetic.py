"""Synthetic building generator: point cloud + exact ground-truth ``building.json``.

Every detection algorithm must first pass on synthetic data (known answer), then on the real
cloud. The default spec is a 12 x 8 m, 2-storey box with:
- 4 exterior walls (15 cm) meeting in L-junctions,
- 1 interior wall (10 cm) splitting two rooms, T-junctions at both ends, with a door,
- 1 window in the south wall, 1 free-standing 30 x 30 cm column, slabs and ceilings.
Coordinates are shifted to CTM12-like magnitudes to exercise the offset logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np
import yaml
from numpy.typing import NDArray

from scan2bim import __version__
from scan2bim.io.writers import write_las
from scan2bim.model import (
    Building,
    Column,
    GeneratorInfo,
    Georef,
    Level,
    Offset,
    Opening,
    ProjectInfo,
    Slab,
    Space,
    Status,
    Wall,
    save_building,
)
from scan2bim.paths import ProjectPaths

Hole = tuple[float, float, float, float]  # u0, u1, z0, z1 in the wall's (u, z) frame

COLOR_WALL = (205, 200, 190)
COLOR_FLOOR = (120, 118, 115)
COLOR_CEILING = (235, 235, 235)
COLOR_COLUMN = (150, 150, 160)


@dataclass(frozen=True)
class SyntheticSpec:
    width: float = 12.0
    depth: float = 8.0
    floors: int = 2
    floor_to_floor: float = 2.6
    slab_thickness: float = 0.12
    exterior_wall_thickness: float = 0.15
    interior_wall_thickness: float = 0.10
    column_size: float = 0.30
    column_center: tuple[float, float] = (9.0, 6.0)
    spacing: float = 0.03
    noise_sigma: float = 0.003
    origin: tuple[float, float] = (10.0, 10.0)
    world_offset: tuple[float, float, float] = (4_880_000.0, 2_066_000.0, 2_600.0)
    seed: int = 7


@dataclass
class SyntheticResult:
    xyz_world: NDArray[np.float64]
    rgb: NDArray[np.uint8]
    building: Building


def _grid(a0: float, a1: float, step: float) -> NDArray[np.float64]:
    n = max(round((a1 - a0) / step), 1)
    return np.linspace(a0, a1, n + 1)


def _vertical_face(
    p0: tuple[float, float],
    p1: tuple[float, float],
    normal_offset: float,
    u_range: tuple[float, float],
    z_range: tuple[float, float],
    step: float,
    holes: list[Hole] | None = None,
) -> NDArray[np.float64]:
    a, b = np.asarray(p0, float), np.asarray(p1, float)
    length = float(np.linalg.norm(b - a))
    t = (b - a) / length
    n = np.array([-t[1], t[0]])  # left normal
    UU, ZZ = np.meshgrid(_grid(*u_range, step), _grid(*z_range, step))
    U, Z = UU.ravel(), ZZ.ravel()
    keep = np.ones(U.shape, dtype=bool)
    for u0, u1, z0, z1 in holes or []:
        keep &= ~((u0 < U) & (u1 > U) & (z0 < Z) & (z1 > Z))
    xy = a + np.outer(U[keep], t) + n * normal_offset
    return np.column_stack([xy, Z[keep]])


def _horizontal_rect(
    x_range: tuple[float, float],
    y_range: tuple[float, float],
    z: float,
    step: float,
    exclude: list[tuple[float, float, float, float]],
) -> NDArray[np.float64]:
    XX, YY = np.meshgrid(_grid(*x_range, step), _grid(*y_range, step))
    X, Y = XX.ravel(), YY.ravel()
    keep = np.ones(X.shape, dtype=bool)
    for x0, x1, y0, y1 in exclude:
        keep &= ~((x0 <= X) & (x1 >= X) & (y0 <= Y) & (y1 >= Y))
    return np.column_stack([X[keep], Y[keep], np.full(int(keep.sum()), z)])


def make_synthetic_building(spec: SyntheticSpec | None = None) -> SyntheticResult:
    s = spec or SyntheticSpec()
    rng = np.random.default_rng(s.seed)
    W, D, te, ti, t = (
        s.width,
        s.depth,
        s.exterior_wall_thickness,
        s.interior_wall_thickness,
        s.slab_thickness,
    )
    h = s.floor_to_floor - t  # clear wall height
    ox, oy = s.origin
    cx, cy = s.column_center
    cs = s.column_size

    # Wall axes (counter-clockwise exterior => left normal points inside).
    exterior = {
        "S": ((te / 2, te / 2), (W - te / 2, te / 2)),
        "E": ((W - te / 2, te / 2), (W - te / 2, D - te / 2)),
        "N": ((W - te / 2, D - te / 2), (te / 2, D - te / 2)),
        "W": ((te / 2, D - te / 2), (te / 2, te / 2)),
    }
    interior = ((te, D / 2), (W - te, D / 2))
    window = {"offset_along": 4.0, "width": 1.2, "height": 1.0, "sill": 0.9}
    door = {"offset_along": 2.0, "width": 0.9, "height": 2.1, "sill": 0.0}

    clouds: list[NDArray[np.float64]] = []
    colors: list[NDArray[np.uint8]] = []

    def add(points: NDArray[np.float64], color: tuple[int, int, int]) -> None:
        clouds.append(points)
        colors.append(np.tile(np.array(color, dtype=np.uint8), (len(points), 1)))

    footprint_exclusions = [
        (te, W - te, D / 2 - ti / 2, D / 2 + ti / 2),  # interior wall
        (cx - cs / 2, cx + cs / 2, cy - cs / 2, cy + cs / 2),  # column
    ]
    for k in range(s.floors):
        z0 = k * s.floor_to_floor
        z1 = z0 + h
        for name, (p0, p1) in exterior.items():
            length = float(np.hypot(p1[0] - p0[0], p1[1] - p0[1]))
            holes: list[Hole] = []
            if name == "S":
                u0 = window["offset_along"]
                holes.append(
                    (
                        u0,
                        u0 + window["width"],
                        z0 + window["sill"],
                        z0 + window["sill"] + window["height"],
                    )
                )
            add(
                _vertical_face(
                    p0, p1, +te / 2, (te / 2, length - te / 2), (z0, z1), s.spacing, holes
                ),
                COLOR_WALL,
            )
            add(
                _vertical_face(
                    p0, p1, -te / 2, (-te / 2, length + te / 2), (z0, z1), s.spacing, holes
                ),
                COLOR_WALL,
            )
        length_i = float(interior[1][0] - interior[0][0])
        u0 = door["offset_along"]
        door_hole: Hole = (u0, u0 + door["width"], z0 - 0.01, z0 + door["height"])
        for side in (+ti / 2, -ti / 2):
            add(
                _vertical_face(
                    interior[0],
                    interior[1],
                    side,
                    (0.0, length_i),
                    (z0, z1),
                    s.spacing,
                    [door_hole],
                ),
                COLOR_WALL,
            )
        corners = [
            (cx - cs / 2, cy - cs / 2),
            (cx + cs / 2, cy - cs / 2),
            (cx + cs / 2, cy + cs / 2),
            (cx - cs / 2, cy + cs / 2),
        ]
        for i in range(4):
            a, b = corners[i], corners[(i + 1) % 4]
            add(_vertical_face(a, b, 0.0, (0.0, cs), (z0, z1), s.spacing), COLOR_COLUMN)
        inner_x, inner_y = (te, W - te), (te, D - te)
        add(_horizontal_rect(inner_x, inner_y, z0, s.spacing, footprint_exclusions), COLOR_FLOOR)
        add(_horizontal_rect(inner_x, inner_y, z1, s.spacing, footprint_exclusions), COLOR_CEILING)

    xyz_local = np.vstack(clouds)
    xyz_local[:, :2] += np.array([ox, oy])
    xyz_local += rng.normal(0.0, s.noise_sigma, size=xyz_local.shape)
    xyz_world = xyz_local + np.asarray(s.world_offset, dtype=np.float64)
    rgb = np.vstack(colors)

    building = _ground_truth(s, exterior, interior, window, door, h)
    return SyntheticResult(xyz_world=xyz_world, rgb=rgb, building=building)


def _ground_truth(
    s: SyntheticSpec,
    exterior: dict[str, tuple[tuple[float, float], tuple[float, float]]],
    interior: tuple[tuple[float, float], tuple[float, float]],
    window: dict[str, float],
    door: dict[str, float],
    h: float,
) -> Building:
    ox, oy = s.origin
    W, D, te, ti = s.width, s.depth, s.exterior_wall_thickness, s.interior_wall_thickness

    def p(x: float, y: float) -> tuple[float, float]:
        return (round(x + ox, 6), round(y + oy, 6))

    ok = {"confidence": 1.0, "status": Status.AUTO}
    level_ids = [f"L{k + 1}" for k in range(s.floors)] + ["LR"]
    levels = [
        Level(
            id=lid,
            name=f"Level {k + 1}" if lid != "LR" else "Roof",
            elevation=k * s.floor_to_floor,
            **ok,
        )
        for k, lid in enumerate(level_ids)
    ]
    footprint = [p(0, 0), p(W, 0), p(W, D), p(0, D)]
    slabs = [
        Slab(id=f"S-{k + 1:04d}", level=lid, outline=footprint, thickness=s.slab_thickness, **ok)
        for k, lid in enumerate(level_ids)
    ]
    walls: list[Wall] = []
    openings: list[Opening] = []
    columns: list[Column] = []
    spaces: list[Space] = []
    for k in range(s.floors):
        base, top = level_ids[k], level_ids[k + 1]
        for name, (a, b) in exterior.items():
            wid = f"W-{len(walls) + 1:04d}"
            walls.append(
                Wall(
                    id=wid,
                    base_level=base,
                    top_level=top,
                    axis=(p(*a), p(*b)),
                    thickness=te,
                    height=h,
                    material_guess="masonry",
                    **ok,
                )
            )
            if name == "S":
                openings.append(
                    Opening(
                        id=f"O-{len(openings) + 1:04d}", host=wid, kind="window", **window, **ok
                    )
                )
        wid = f"W-{len(walls) + 1:04d}"
        walls.append(
            Wall(
                id=wid,
                base_level=base,
                top_level=top,
                axis=(p(*interior[0]), p(*interior[1])),
                thickness=ti,
                height=h,
                material_guess="masonry",
                **ok,
            )
        )
        openings.append(
            Opening(id=f"O-{len(openings) + 1:04d}", host=wid, kind="door", **door, **ok)
        )
        columns.append(
            Column(
                id=f"C-{len(columns) + 1:04d}",
                base_level=base,
                top_level=top,
                center=p(*s.column_center),
                shape="rect",
                size=[s.column_size, s.column_size],
                **ok,
            )
        )
        south = [p(te, te), p(W - te, te), p(W - te, D / 2 - ti / 2), p(te, D / 2 - ti / 2)]
        north = [p(te, D / 2 + ti / 2), p(W - te, D / 2 + ti / 2), p(W - te, D - te), p(te, D - te)]
        for poly in (south, north):
            xs, ys = [q[0] for q in poly], [q[1] for q in poly]
            area = (max(xs) - min(xs)) * (max(ys) - min(ys))
            seed = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
            spaces.append(
                Space(
                    id=f"R-{len(spaces) + 1:04d}",
                    level=base,
                    polygon=poly,
                    seed=seed,
                    area=area,
                    **ok,
                )
            )

    return Building(
        generator=GeneratorInfo(version=__version__, created=datetime.now(UTC)),
        project=ProjectInfo(
            id="synthetic",
            name="Synthetic box",
            capture_date=date(2026, 1, 1),
            scanner="synthetic",
            building_state="shell",
        ),
        georef=Georef(
            crs="EPSG:9377",
            offset=Offset(x=s.world_offset[0], y=s.world_offset[1], z=s.world_offset[2]),
            vertical="orthometric",
        ),
        dominant_direction_deg=0.0,
        levels=levels,
        slabs=slabs,
        walls=walls,
        columns=columns,
        openings=openings,
        spaces=spaces,
    )


def write_synthetic_project(
    data_root: Path, project: str = "synthetic-box", spec: SyntheticSpec | None = None
) -> ProjectPaths:
    """Create raw cloud + project metadata + ground truth (as the reference model)."""
    paths = ProjectPaths(data_root, project)
    result = make_synthetic_building(spec)
    paths.raw.mkdir(parents=True, exist_ok=True)
    write_las(paths.raw / "synthetic.laz", result.xyz_world, rgb=result.rgb, crs_epsg=9377)
    paths.reference.mkdir(parents=True, exist_ok=True)
    save_building(result.building, paths.reference / "ground_truth.building.json")
    s = spec or SyntheticSpec()
    meta = {
        "name": "Synthetic box",
        "floors": s.floors,
        "floor_to_floor_m": s.floor_to_floor,
        "use": "other",
        "building_state": "shell",
        "scanner": "synthetic",
        "crs": "EPSG:9377",
        "vertical": "orthometric",
        "capture_date": "2026-01-01",
        "lod_target": 200,
        "notes": "Generated by scan2bim.synthetic (ground truth in reference/).",
        "overrides": {},
    }
    paths.project_file.parent.mkdir(parents=True, exist_ok=True)
    paths.project_file.write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    return paths
