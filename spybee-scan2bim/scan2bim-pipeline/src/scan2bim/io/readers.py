"""Streaming readers for E57 / LAS / LAZ.

Rules (see CLAUDE.md): never load a whole cloud blindly; iterate in chunks and keep
coordinates in float64 until a local offset has been subtracted.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

SUPPORTED_SUFFIXES = {".las", ".laz", ".e57"}
PROPRIETARY_SUFFIXES = {
    ".rcp": "Autodesk ReCap project",
    ".rcs": "Autodesk ReCap scan",
    ".fls": "FARO scan",
    ".fws": "FARO workspace",
    ".lgs": "Leica LGS",
    ".lgsx": "Leica LGS",
    ".pts": "PTS ASCII (convert with CloudCompare)",
    ".ptx": "PTX ASCII (convert with CloudCompare)",
}

LAS_COLOR_FORMATS = {2, 3, 5, 7, 8, 10}


class UnsupportedCloudError(RuntimeError):
    """Raised when the raw folder only contains formats we cannot read directly."""


@dataclass
class CloudFileInfo:
    path: Path
    format: str
    point_count: int
    scan_count: int = 1
    has_color: bool = False
    has_intensity: bool = False
    bbox_min: NDArray[np.float64] | None = None
    bbox_max: NDArray[np.float64] | None = None
    crs_wkt: str | None = None
    notes: list[str] = field(default_factory=list)

    @property
    def size_bytes(self) -> int:
        return self.path.stat().st_size


@dataclass
class PointChunk:
    xyz: NDArray[np.float64]  # (N, 3) world coordinates
    rgb: NDArray[np.uint8] | None = None  # (N, 3)
    intensity: NDArray[np.float32] | None = None  # (N,)

    def __len__(self) -> int:
        return int(self.xyz.shape[0])


def find_cloud_files(raw_dir: Path) -> list[Path]:
    """Return readable cloud files in ``raw_dir`` (sorted). Explain what to do otherwise."""
    if not raw_dir.is_dir():
        raise FileNotFoundError(f"Raw folder not found: {raw_dir}")
    files = sorted(p for p in raw_dir.iterdir() if p.is_file())
    readable = [p for p in files if p.suffix.lower() in SUPPORTED_SUFFIXES]
    if readable:
        return readable
    proprietary = [p for p in files if p.suffix.lower() in PROPRIETARY_SUFFIXES]
    if proprietary:
        kinds = ", ".join(sorted({PROPRIETARY_SUFFIXES[p.suffix.lower()] for p in proprietary}))
        raise UnsupportedCloudError(
            f"Only proprietary formats found ({kinds}). Export an E57 or LAS/LAZ from the "
            "scanner software (see docs/engineering/ENVIRONMENT_SETUP_WINDOWS.md)."
        )
    raise UnsupportedCloudError(f"No .e57/.las/.laz files in {raw_dir}")


# ---------------------------------------------------------------------------------------
# LAS / LAZ
# ---------------------------------------------------------------------------------------
def _las_info(path: Path) -> CloudFileInfo:
    import laspy

    with laspy.open(path) as reader:
        header = reader.header
        crs_wkt = None
        try:
            crs = header.parse_crs()
            crs_wkt = crs.to_wkt() if crs is not None else None
        except Exception:  # CRS VLRs are often missing or malformed
            crs_wkt = None
        return CloudFileInfo(
            path=path,
            format=path.suffix.lower().lstrip("."),
            point_count=int(header.point_count),
            has_color=header.point_format.id in LAS_COLOR_FORMATS,
            has_intensity=True,
            bbox_min=np.asarray(header.mins, dtype=np.float64),
            bbox_max=np.asarray(header.maxs, dtype=np.float64),
            crs_wkt=crs_wkt,
        )


def _to_uint8(channel: NDArray[np.generic]) -> NDArray[np.uint8]:
    arr = np.asarray(channel)
    if arr.size and arr.max() > 255:
        arr = arr // 256
    return arr.astype(np.uint8)


def _iter_las(path: Path, chunk_points: int) -> Iterator[PointChunk]:
    import laspy

    with laspy.open(path) as reader:
        has_color = reader.header.point_format.id in LAS_COLOR_FORMATS
        for pts in reader.chunk_iterator(chunk_points):
            xyz = np.column_stack([np.asarray(pts.x), np.asarray(pts.y), np.asarray(pts.z)]).astype(
                np.float64
            )
            rgb = None
            if has_color:
                rgb = np.column_stack(
                    [_to_uint8(pts.red), _to_uint8(pts.green), _to_uint8(pts.blue)]
                )
            intensity = np.asarray(pts.intensity, dtype=np.float32)
            yield PointChunk(xyz=xyz, rgb=rgb, intensity=intensity)


# ---------------------------------------------------------------------------------------
# E57
# ---------------------------------------------------------------------------------------
def _e57_info(path: Path) -> CloudFileInfo:
    import pye57

    e57 = pye57.E57(str(path))
    try:
        total = 0
        has_color = has_intensity = True
        for i in range(e57.scan_count):
            header = e57.get_header(i)
            total += int(header.point_count)
            fields = set(header.point_fields)
            has_color &= {"colorRed", "colorGreen", "colorBlue"} <= fields
            has_intensity &= "intensity" in fields
        return CloudFileInfo(
            path=path,
            format="e57",
            point_count=total,
            scan_count=int(e57.scan_count),
            has_color=has_color,
            has_intensity=has_intensity,
            notes=["E57 bounding box is computed while reading (scan poses applied)."],
        )
    finally:
        e57.close()


def _iter_e57(path: Path, chunk_points: int) -> Iterator[PointChunk]:
    import pye57

    e57 = pye57.E57(str(path))
    try:
        for i in range(e57.scan_count):
            fields = set(e57.get_header(i).point_fields)
            colors = {"colorRed", "colorGreen", "colorBlue"} <= fields
            intensity = "intensity" in fields
            data = e57.read_scan(
                i, ignore_missing_fields=True, colors=colors, intensity=intensity, transform=True
            )
            xyz = np.column_stack(
                [data["cartesianX"], data["cartesianY"], data["cartesianZ"]]
            ).astype(np.float64)
            rgb = (
                np.column_stack(
                    [
                        _to_uint8(data["colorRed"]),
                        _to_uint8(data["colorGreen"]),
                        _to_uint8(data["colorBlue"]),
                    ]
                )
                if colors
                else None
            )
            inten = np.asarray(data["intensity"], dtype=np.float32) if intensity else None
            for start in range(0, len(xyz), chunk_points):
                sl = slice(start, start + chunk_points)
                yield PointChunk(
                    xyz=xyz[sl],
                    rgb=None if rgb is None else rgb[sl],
                    intensity=None if inten is None else inten[sl],
                )
    finally:
        e57.close()


# ---------------------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------------------
def read_info(path: Path) -> CloudFileInfo:
    suffix = path.suffix.lower()
    if suffix in {".las", ".laz"}:
        return _las_info(path)
    if suffix == ".e57":
        return _e57_info(path)
    raise UnsupportedCloudError(f"Unsupported file: {path.name}")


def iter_chunks(path: Path, chunk_points: int) -> Iterator[PointChunk]:
    suffix = path.suffix.lower()
    if suffix in {".las", ".laz"}:
        yield from _iter_las(path, chunk_points)
    elif suffix == ".e57":
        yield from _iter_e57(path, chunk_points)
    else:
        raise UnsupportedCloudError(f"Unsupported file: {path.name}")
