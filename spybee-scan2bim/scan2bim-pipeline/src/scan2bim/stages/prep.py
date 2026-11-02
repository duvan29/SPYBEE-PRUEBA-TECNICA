"""Stage ``prep``: streaming voxel down-sampling, local offset, optional cleaning + normals.

Outputs (work/<project>/): cloud_work.laz (LOCAL coordinates), normals.npz (if open3d),
georef.json, prep_report.json; debug/prep/top.png
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

import numpy as np
from numpy.typing import NDArray

from scan2bim import viz
from scan2bim.config import PipelineConfig
from scan2bim.georef import GeorefInfo, compute_offset, guess_crs, to_local
from scan2bim.io.readers import find_cloud_files, iter_chunks
from scan2bim.io.writers import write_las
from scan2bim.log import get_logger, stage
from scan2bim.paths import ProjectPaths
from scan2bim.project import ProjectMetadata

log = get_logger("prep")

_BITS = 21  # 21 bits per axis -> 2,097,152 voxels per axis (~20 km at 1 cm)
_HALF = 1 << (_BITS - 1)
_LIMIT = 1 << _BITS


@dataclass
class PrepResult:
    input_points: int
    output_points: int
    voxel_size: float
    offset: list[float]
    crs: str
    normals: bool
    outliers_removed: int = 0
    seconds: float = 0.0
    warnings: list[str] = field(default_factory=list)


class VoxelAccumulator:
    """Keeps the first point that falls in each voxel, across many chunks.

    Voxel indices are packed into one int64 key (21 bits per axis) relative to a base taken
    from the first chunk, so memory stays proportional to the OUTPUT size.
    """

    def __init__(self, voxel: float) -> None:
        self.voxel = voxel
        self.base: NDArray[np.int64] | None = None
        self._keys: list[NDArray[np.int64]] = []
        self._xyz: list[NDArray[np.float64]] = []
        self._rgb: list[NDArray[np.uint8] | None] = []
        self._pending = 0
        self._kept = 0

    def _pack(self, xyz: NDArray[np.float64]) -> NDArray[np.int64]:
        idx = np.floor(xyz / self.voxel).astype(np.int64)
        if self.base is None:
            self.base = idx.min(axis=0) - _HALF
        rel = idx - self.base
        if np.min(rel) < 0 or np.max(rel) >= _LIMIT:
            raise ValueError("Cloud extent exceeds the voxel key range (~20 km at 1 cm).")
        return rel[:, 0] | (rel[:, 1] << _BITS) | (rel[:, 2] << (2 * _BITS))

    def add(self, xyz: NDArray[np.float64], rgb: NDArray[np.uint8] | None) -> None:
        self._keys.append(self._pack(xyz))
        self._xyz.append(xyz)
        self._rgb.append(rgb)
        self._pending += len(xyz)
        if self._pending > max(2 * self._kept, 5_000_000):
            self._consolidate()

    def _consolidate(self) -> None:
        if not self._keys:
            return
        keys = np.concatenate(self._keys)
        _, first = np.unique(keys, return_index=True)
        xyz = np.concatenate(self._xyz)[first]
        has_rgb = all(r is not None for r in self._rgb)
        rgb = np.concatenate([r for r in self._rgb if r is not None])[first] if has_rgb else None
        self._keys, self._xyz, self._rgb = [keys[first]], [xyz], [rgb]
        self._kept = self._pending = len(first)

    def result(self) -> tuple[NDArray[np.float64], NDArray[np.uint8] | None]:
        self._consolidate()
        if not self._xyz:
            return np.empty((0, 3)), None
        return self._xyz[0], self._rgb[0]


def _clean_and_normals(
    local: NDArray[np.float32], cfg: PipelineConfig
) -> tuple[NDArray[np.bool_], NDArray[np.float32]]:
    """Statistical outlier removal + normals with open3d. Returns (keep_mask, normals)."""
    import open3d as o3d

    pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(local.astype(np.float64)))
    _, kept_idx = pcd.remove_statistical_outlier(
        nb_neighbors=cfg.prep.outlier_nb_neighbors, std_ratio=cfg.prep.outlier_std_ratio
    )
    keep = np.zeros(len(local), dtype=bool)
    keep[np.asarray(kept_idx)] = True
    pcd = pcd.select_by_index(kept_idx)
    pcd.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(
            radius=cfg.prep.normal_radius, max_nn=cfg.prep.normal_max_nn
        )
    )
    return keep, np.asarray(pcd.normals, dtype=np.float32)


def _resolve_crs(meta: ProjectMetadata | None, guess_kind: str, candidates: list[int]) -> str:
    if meta and meta.crs not in {"", "unknown"}:
        return meta.crs
    if guess_kind == "local":
        return "local"
    if guess_kind == "ctm12" and candidates:
        return f"EPSG:{candidates[0]}"
    return "unknown"


def run_prep(
    paths: ProjectPaths,
    cfg: PipelineConfig,
    meta: ProjectMetadata | None = None,
    compute_normals: bool = True,
) -> PrepResult:
    paths.ensure_outputs()
    warnings: list[str] = []
    with stage("prep") as stats:
        acc = VoxelAccumulator(cfg.prep.voxel_size)
        n_in = 0
        for path in find_cloud_files(paths.raw):
            for chunk in iter_chunks(path, cfg.io.read_chunk_points):
                acc.add(chunk.xyz, chunk.rgb)
                n_in += len(chunk)
            log.info("read %s (%s points so far)", path.name, f"{n_in:,}")
        world, rgb = acc.result()
        if len(world) == 0:
            raise RuntimeError("No points read.")
        lo, hi = world.min(axis=0), world.max(axis=0)
        offset = compute_offset(
            lo,
            hi,
            xy_round=cfg.prep.offset_round,
            xy_threshold=cfg.prep.large_coord_threshold,
            z_threshold=cfg.prep.z_offset_threshold,
            z_round=cfg.prep.z_offset_round,
        )
        local = to_local(world, offset)
        del world
        log.info(
            "voxel %.3f m: %s -> %s points", cfg.prep.voxel_size, f"{n_in:,}", f"{len(local):,}"
        )

        normals_ok = False
        removed = 0
        if compute_normals:
            try:
                keep, normals = _clean_and_normals(local, cfg)
                removed = int((~keep).sum())
                local = local[keep]
                rgb = rgb[keep] if rgb is not None else None
                np.savez_compressed(paths.normals_file, normals=normals)
                normals_ok = True
            except (ImportError, OSError) as exc:  # open3d missing or no graphics libs
                msg = f"open3d unavailable ({exc}); normals and outlier removal skipped."
                log.warning(msg)
                warnings.append(msg)

        write_las(paths.working_cloud, local, rgb=rgb)
        guess = guess_crs(lo, hi)
        crs = _resolve_crs(meta, guess.kind, guess.epsg_candidates)
        GeorefInfo(
            crs=crs,
            offset=[float(v) for v in offset],
            vertical=meta.vertical if meta else "unknown",
            guess_kind=guess.kind,
            note=guess.note,
        ).save(paths.georef_file)
        viz.plot_top(
            local, paths.debug("prep") / "top.png", f"{paths.project}: working cloud (local)"
        )

        result = PrepResult(
            input_points=n_in,
            output_points=len(local),
            voxel_size=cfg.prep.voxel_size,
            offset=[float(v) for v in offset],
            crs=crs,
            normals=normals_ok,
            outliers_removed=removed,
            warnings=warnings,
        )
    result.seconds = round(stats.seconds, 1)
    (paths.work / "prep_report.json").write_text(
        json.dumps(asdict(result), indent=2), encoding="utf-8"
    )
    return result
