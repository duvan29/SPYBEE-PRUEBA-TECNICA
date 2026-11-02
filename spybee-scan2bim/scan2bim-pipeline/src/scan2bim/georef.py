"""Coordinate reference systems, local offsets and reprojection.

Principles (docs/architecture/GEOREFERENCING_AND_CRS.md):
1. Never rotate the cloud. Work in the cloud's own frame minus a round offset.
2. local = world - offset, computed in float64 BEFORE casting to float32.
3. Reproject only when the delivery CRS differs from the project CRS, and only
   horizontally (2D CRSs). Heights are never converted silently.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

# Colombian CRSs (EPSG). CTM12 / "Origen Nacional" is the official system (IGAC Res. 471/2020).
EPSG_CTM12 = 9377
EPSG_MAGNA_GEOGRAPHIC = 4686
MAGNA_GAUSS_KRUGER_ZONES = {
    3114: "MAGNA-SIRGAS / Colombia Far West zone",
    3115: "MAGNA-SIRGAS / Colombia West zone",
    3116: "MAGNA-SIRGAS / Colombia Bogota zone",
    3117: "MAGNA-SIRGAS / Colombia East Central zone",
    3118: "MAGNA-SIRGAS / Colombia East zone",
}


@dataclass(frozen=True)
class CrsGuess:
    kind: str  # local | ctm12 | magna_gauss_kruger | utm | geographic | unknown_projected
    epsg_candidates: list[int]
    note: str


def guess_crs(bbox_min: NDArray[np.floating], bbox_max: NDArray[np.floating]) -> CrsGuess:
    """Heuristic guess from coordinate magnitudes. ALWAYS confirm with the scan leader."""
    xmin, ymin = float(bbox_min[0]), float(bbox_min[1])
    xmax, ymax = float(bbox_max[0]), float(bbox_max[1])
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2

    if xmin >= -180 and xmax <= 180 and ymin >= -90 and ymax <= 90 and (xmax - xmin) < 1:
        return CrsGuess("geographic", [EPSG_MAGNA_GEOGRAPHIC], "Looks like lon/lat degrees.")
    if max(abs(xmin), abs(xmax), abs(ymin), abs(ymax)) < 20_000:
        return CrsGuess("local", [], "Small coordinates: local scanner/project frame.")
    if 3_500_000 <= cx <= 6_500_000 and 1_000_000 <= cy <= 3_500_000:
        return CrsGuess(
            "ctm12", [EPSG_CTM12], "Magnitudes match CTM12 / Origen Nacional (EPSG:9377)."
        )
    if 500_000 <= cx <= 1_600_000 and 0 <= cy <= 2_500_000:
        return CrsGuess(
            "magna_gauss_kruger",
            sorted(MAGNA_GAUSS_KRUGER_ZONES),
            "Magnitudes match a MAGNA-SIRGAS Gauss-Kruger zone (EPSG:3114-3118); "
            "Bogota zone is EPSG:3116.",
        )
    if 160_000 <= cx <= 840_000 and 0 <= cy <= 10_000_000:
        return CrsGuess("utm", [32617, 32618, 32619], "Magnitudes match UTM (zones 17N-19N).")
    return CrsGuess("unknown_projected", [], "Large coordinates of unknown projection.")


def compute_offset(
    bbox_min: NDArray[np.floating],
    bbox_max: NDArray[np.floating],
    xy_round: float = 1000.0,
    xy_threshold: float = 100_000.0,
    z_threshold: float = 1000.0,
    z_round: float = 100.0,
) -> NDArray[np.float64]:
    """Round offset near the bbox centre so local coordinates stay small.

    Rounding the centre to the NEAREST multiple (not the floor of the minimum) makes the
    offset robust to scanner noise around a round coordinate.
    """
    lo = np.asarray(bbox_min, dtype=np.float64)
    hi = np.asarray(bbox_max, dtype=np.float64)
    centre = (lo + hi) / 2
    offset = np.zeros(3, dtype=np.float64)
    if max(abs(lo[0]), abs(hi[0]), abs(lo[1]), abs(hi[1])) > xy_threshold:
        offset[:2] = np.round(centre[:2] / xy_round) * xy_round
    if max(abs(lo[2]), abs(hi[2])) > z_threshold:
        offset[2] = np.round(centre[2] / z_round) * z_round
    return offset


def to_local(xyz_world: NDArray[np.floating], offset: NDArray[np.floating]) -> NDArray[np.float32]:
    """Subtract the offset in float64, then cast to float32 (safe for local metres)."""
    return (np.asarray(xyz_world, dtype=np.float64) - np.asarray(offset, np.float64)).astype(
        np.float32
    )


def to_world(xyz_local: NDArray[np.floating], offset: NDArray[np.floating]) -> NDArray[np.float64]:
    return np.asarray(xyz_local, dtype=np.float64) + np.asarray(offset, dtype=np.float64)


def reproject_xy(
    xyz: NDArray[np.floating], src_crs: str | int, dst_crs: str | int
) -> NDArray[np.float64]:
    """Reproject horizontal coordinates between 2D CRSs; z is returned unchanged.

    Uses pyproj with ``always_xy=True`` (x=easting/longitude, y=northing/latitude).
    Vertical datum changes (ellipsoidal <-> orthometric) are intentionally NOT handled here.
    """
    from pyproj import Transformer

    arr = np.asarray(xyz, dtype=np.float64)
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    x, y = transformer.transform(arr[:, 0], arr[:, 1])
    return np.column_stack([np.asarray(x), np.asarray(y), arr[:, 2]])


@dataclass
class GeorefInfo:
    """Persisted as data/work/<project>/georef.json and copied into building.json."""

    crs: str = "local"
    offset: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    vertical: str = "unknown"
    guess_kind: str | None = None
    note: str | None = None

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> GeorefInfo:
        return cls(**json.loads(path.read_text(encoding="utf-8")))

    @property
    def offset_array(self) -> NDArray[np.float64]:
        return np.asarray(self.offset, dtype=np.float64)
