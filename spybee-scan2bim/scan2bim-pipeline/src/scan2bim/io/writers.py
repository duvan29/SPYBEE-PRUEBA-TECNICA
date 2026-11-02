"""Writers for LAS/LAZ (LAZ when the suffix is .laz; needs the lazrs backend)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def write_las(
    path: Path,
    xyz: NDArray[np.floating],
    rgb: NDArray[np.uint8] | None = None,
    intensity: NDArray[np.floating] | None = None,
    scale: float = 0.001,
    crs_epsg: int | None = None,
) -> None:
    """Write a LAS 1.4 file (point format 7 with colour, 6 without).

    Coordinates are stored as int32 * ``scale`` + header offset; the offset is chosen
    from the data so 1 mm precision is kept even for large (e.g. CTM12) coordinates.
    """
    import laspy

    xyz = np.asarray(xyz, dtype=np.float64)
    header = laspy.LasHeader(point_format=7 if rgb is not None else 6, version="1.4")
    header.scales = np.array([scale, scale, scale])
    header.offsets = np.floor(xyz.min(axis=0)) if len(xyz) else np.zeros(3)
    if crs_epsg is not None:
        from pyproj import CRS

        header.add_crs(CRS.from_epsg(crs_epsg))
    las = laspy.LasData(header)
    las.x, las.y, las.z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
    if rgb is not None:
        rgb16 = np.asarray(rgb, dtype=np.uint16) * 257
        las.red, las.green, las.blue = rgb16[:, 0], rgb16[:, 1], rgb16[:, 2]
    if intensity is not None:
        las.intensity = np.clip(np.asarray(intensity), 0, 65535).astype(np.uint16)
    path.parent.mkdir(parents=True, exist_ok=True)
    las.write(path)
