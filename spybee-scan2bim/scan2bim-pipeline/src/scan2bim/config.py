"""Typed pipeline configuration.

Defaults live in ``scan2bim/resources/default.yaml`` (shipped with the package). A project
can override any subset under ``overrides:`` in ``data/projects/<project>.yaml``. Every key is
validated: unknown keys raise an error so typos never silently fall back to defaults.
"""

from __future__ import annotations

import copy
import hashlib
import json
from importlib import resources
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict


class _Section(BaseModel):
    model_config = ConfigDict(extra="forbid")


class IOConfig(_Section):
    max_points_inspect_sample: int
    read_chunk_points: int
    e57_max_ram_fraction: float


class PrepConfig(_Section):
    voxel_size: float
    outlier_nb_neighbors: int
    outlier_std_ratio: float
    normal_radius: float
    normal_max_nn: int
    offset_round: float
    large_coord_threshold: float
    z_offset_threshold: float
    z_offset_round: float
    local_cloud_voxel: float


class LevelsConfig(_Section):
    horizontal_normal_min_nz: float
    z_hist_bin: float
    min_peak_fraction: float
    min_floor_to_floor: float
    max_floor_to_floor: float
    default_slab_thickness: float
    min_slab_thickness: float
    max_slab_thickness: float


class SlabsConfig(_Section):
    concave_hull_ratio: float
    raster_cell: float
    simplify_tolerance: float
    orthogonalize_angle_tol_deg: float
    min_hole_area: float


class WallsConfig(_Section):
    slice_main: tuple[float, float]
    slice_check: list[tuple[float, float]]
    vertical_normal_max_nz: float
    ransac_distance: float
    min_face_length: float
    min_face_points: int
    parallel_angle_tol_deg: float
    thickness_range: tuple[float, float]
    thickness_catalog: list[float]
    default_one_face_thickness: float
    snap_dominant_tol_deg: float
    collinear_merge_gap: float
    collinear_offset_tol: float
    join_extend_max: float
    min_vertical_continuity: float


class ColumnsConfig(_Section):
    size_range: tuple[float, float]
    max_aspect_ratio: float
    min_height_fraction: float
    embedded_bump_min: float


class OpeningsConfig(_Section):
    raster_cell: float
    min_width: float
    max_width: float
    min_height: float
    door_max_sill: float
    window_min_sill: float
    see_through_min_depth: float


class SpacesConfig(_Section):
    raster_cell: float
    min_area: float


class ConfidenceWeights(_Section):
    coverage: float
    residual: float
    consistency: float


class ConfidenceConfig(_Section):
    review_threshold: float
    weights: ConfidenceWeights
    reason_penalty: float


class QAConfig(_Section):
    tol_tight: float
    tol_loose: float


class PipelineConfig(_Section):
    io: IOConfig
    prep: PrepConfig
    levels: LevelsConfig
    slabs: SlabsConfig
    walls: WallsConfig
    columns: ColumnsConfig
    openings: OpeningsConfig
    spaces: SpacesConfig
    confidence: ConfidenceConfig
    qa: QAConfig

    def config_hash(self) -> str:
        """Short, stable hash recorded in building.json for traceability."""
        payload = json.dumps(self.model_dump(mode="json"), sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()[:12]


def default_config_dict() -> dict[str, Any]:
    text = resources.files("scan2bim.resources").joinpath("default.yaml").read_text("utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("default.yaml must contain a mapping")
    return data


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge ``override`` into a copy of ``base`` (override wins)."""
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def load_config(overrides: dict[str, Any] | None = None) -> PipelineConfig:
    data = default_config_dict()
    if overrides:
        data = deep_merge(data, overrides)
    return PipelineConfig.model_validate(data)
