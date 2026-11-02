"""Stage ``inspect``: cloud report without loading the full cloud.

Outputs (out/<project>/): cloud_report.md, cloud_report.json, debug/inspect/*.png
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from scipy.signal import find_peaks

from scan2bim import viz
from scan2bim.config import PipelineConfig
from scan2bim.georef import compute_offset, guess_crs
from scan2bim.io.readers import find_cloud_files, iter_chunks, read_info
from scan2bim.log import available_ram_bytes, get_logger, stage
from scan2bim.paths import ProjectPaths
from scan2bim.project import ProjectMetadata

log = get_logger("inspect")
BYTES_PER_POINT_E57 = 40  # rough in-memory cost when pye57 reads a scan


@dataclass
class FileSummary:
    name: str
    format: str
    size_mb: float
    point_count: int
    scan_count: int
    has_color: bool
    has_intensity: bool
    crs_in_header: bool
    skipped_reason: str | None = None


@dataclass
class InspectResult:
    project: str
    files: list[FileSummary]
    total_points: int
    sampled_points: int
    sample_stride: int
    bbox_min: list[float]
    bbox_max: list[float]
    dimensions_m: list[float]
    crs_guess: str
    crs_epsg_candidates: list[int]
    crs_note: str
    suggested_offset: list[float]
    horizontal_surface_peaks_z_local: list[float]
    footprint_area_m2: float
    points_per_m2_footprint: float
    seconds: float = 0.0
    warnings: list[str] = field(default_factory=list)


def _z_peaks(z: NDArray[np.floating], bin_size: float, min_separation: float = 0.06) -> list[float]:
    """Peaks of the z histogram (horizontal surfaces).

    The histogram is zero-padded so the lowest floor / highest ceiling (at the array edges)
    can be detected, and ``min_separation`` is small because a floor and the ceiling below it
    are only one slab thickness (~0.10-0.20 m) apart.
    """
    lo, hi = float(np.min(z)), float(np.max(z))
    bins = max(math.ceil((hi - lo) / bin_size), 1)
    hist, edges = np.histogram(z, bins=bins, range=(lo, hi))
    centres = (edges[:-1] + edges[1:]) / 2
    if hist.max() == 0:
        return []
    padded = np.concatenate([[0], hist, [0]])
    idx, _ = find_peaks(
        padded, prominence=hist.max() * 0.15, distance=max(int(min_separation / bin_size), 1)
    )
    return [round(float(centres[i - 1]), 3) for i in idx]


def _footprint_area(xy: NDArray[np.floating], cell: float = 0.5) -> float:
    if len(xy) == 0:
        return 0.0
    keys = np.floor(xy / cell).astype(np.int64)
    return float(len(np.unique(keys, axis=0))) * cell * cell


def run_inspect(
    paths: ProjectPaths, cfg: PipelineConfig, meta: ProjectMetadata | None = None
) -> InspectResult:
    paths.ensure_outputs()
    with stage("inspect") as stats:
        files = find_cloud_files(paths.raw)
        infos = [read_info(f) for f in files]
        total = sum(i.point_count for i in infos)
        stride = max(1, math.ceil(total / cfg.io.max_points_inspect_sample))
        log.info("%d file(s), %s points, sample stride %d", len(files), f"{total:,}", stride)

        free_ram = available_ram_bytes()
        summaries: list[FileSummary] = []
        samples: list[NDArray[np.float64]] = []
        lo = np.full(3, np.inf)
        hi = np.full(3, -np.inf)
        warnings: list[str] = []
        for info in infos:
            skipped = None
            if (
                info.format == "e57"
                and free_ram is not None
                and info.point_count * BYTES_PER_POINT_E57 > cfg.io.e57_max_ram_fraction * free_ram
            ):
                skipped = (
                    "E57 too large to read safely with the free RAM; pre-decimate with "
                    "CloudCompare (docs/engineering/ENVIRONMENT_SETUP_WINDOWS.md)."
                )
                warnings.append(f"{info.path.name}: {skipped}")
            else:
                for chunk in iter_chunks(info.path, cfg.io.read_chunk_points):
                    lo = np.minimum(lo, chunk.xyz.min(axis=0))
                    hi = np.maximum(hi, chunk.xyz.max(axis=0))
                    samples.append(chunk.xyz[::stride])
            summaries.append(
                FileSummary(
                    name=info.path.name,
                    format=info.format,
                    size_mb=round(info.size_bytes / 1e6, 1),
                    point_count=info.point_count,
                    scan_count=info.scan_count,
                    has_color=info.has_color,
                    has_intensity=info.has_intensity,
                    crs_in_header=info.crs_wkt is not None,
                    skipped_reason=skipped,
                )
            )
        if not samples:
            raise RuntimeError("No file could be sampled. See warnings: " + "; ".join(warnings))

        sample = np.vstack(samples)
        guess = guess_crs(lo, hi)
        offset = compute_offset(
            lo,
            hi,
            xy_round=cfg.prep.offset_round,
            xy_threshold=cfg.prep.large_coord_threshold,
            z_threshold=cfg.prep.z_offset_threshold,
            z_round=cfg.prep.z_offset_round,
        )
        local = sample - offset
        peaks = _z_peaks(local[:, 2], cfg.levels.z_hist_bin)
        area = _footprint_area(local[:, :2])

        if (
            meta
            and meta.crs not in {"unknown", ""}
            and guess.kind == "local"
            and meta.crs != "local"
        ):
            warnings.append(f"Metadata says CRS {meta.crs} but coordinates look local.")

        debug = paths.debug("inspect")
        viz.plot_top(local, debug / "top.png", f"{paths.project}: top view (local, coloured by z)")
        viz.plot_side(local, debug / "side_x.png", f"{paths.project}: side view x-z", axis=0)
        viz.plot_side(local, debug / "side_y.png", f"{paths.project}: side view y-z", axis=1)
        viz.plot_histogram(
            local[:, 2],
            cfg.levels.z_hist_bin,
            debug / "z_hist.png",
            f"{paths.project}: z histogram (peaks = horizontal surfaces)",
            "z local [m]",
            peaks,
        )

        result = InspectResult(
            project=paths.project,
            files=summaries,
            total_points=total,
            sampled_points=len(sample),
            sample_stride=stride,
            bbox_min=[round(float(v), 3) for v in lo],
            bbox_max=[round(float(v), 3) for v in hi],
            dimensions_m=[round(float(v), 2) for v in (hi - lo)],
            crs_guess=guess.kind,
            crs_epsg_candidates=guess.epsg_candidates,
            crs_note=guess.note,
            suggested_offset=[float(v) for v in offset],
            horizontal_surface_peaks_z_local=peaks,
            footprint_area_m2=round(area, 1),
            points_per_m2_footprint=round(total / area, 1) if area else 0.0,
            warnings=warnings,
        )
    result.seconds = round(stats.seconds, 1)
    _write_reports(paths, result, meta)
    return result


def _write_reports(paths: ProjectPaths, r: InspectResult, meta: ProjectMetadata | None) -> None:
    (paths.out / "cloud_report.json").write_text(json.dumps(asdict(r), indent=2), encoding="utf-8")
    lines = [
        f"# Cloud report - {r.project}",
        "",
        "## Files",
        "",
        "| File | Format | Size (MB) | Points | Scans | Colour | Intensity | CRS in header |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for f in r.files:
        lines.append(
            f"| {f.name} | {f.format} | {f.size_mb} | {f.point_count:,} | {f.scan_count} | "
            f"{f.has_color} | {f.has_intensity} | {f.crs_in_header} |"
        )
    lines += [
        "",
        "## Geometry",
        "",
        f"- Total points: **{r.total_points:,}** (sampled {r.sampled_points:,}, stride {r.sample_stride})",
        f"- Bounding box min (world): {r.bbox_min}",
        f"- Bounding box max (world): {r.bbox_max}",
        f"- Dimensions (m): {r.dimensions_m}",
        f"- Footprint area (0.5 m grid): {r.footprint_area_m2} m2",
        f"- Points per m2 of footprint (all storeys): {r.points_per_m2_footprint}",
        "",
        "## Coordinate system",
        "",
        f"- Guess: **{r.crs_guess}** {r.crs_epsg_candidates} - {r.crs_note}",
        f"- Metadata CRS: {meta.crs if meta else 'n/a (no data/projects file)'}",
        f"- Suggested local offset: {r.suggested_offset}",
        "",
        "## Horizontal surfaces (z histogram peaks, local z)",
        "",
        f"{r.horizontal_surface_peaks_z_local}",
        "",
        "Floors and ceilings both produce peaks; the `levels` stage classifies them.",
    ]
    if meta and meta.floors:
        lines.append(
            f"Expected storeys from metadata: {meta.floors} (floor-to-floor {meta.floor_to_floor_m} m)."
        )
    lines += ["", "## Warnings", ""]
    lines += [f"- {w}" for w in r.warnings] or ["- none"]
    lines += [
        "",
        "## Debug images",
        "",
        "- debug/inspect/top.png, side_x.png, side_y.png, z_hist.png",
        "",
        f"_Generated in {r.seconds} s._",
    ]
    Path(paths.out / "cloud_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
