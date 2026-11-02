"""Project metadata (``data/projects/<project>.yaml``)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from scan2bim.config import PipelineConfig, load_config
from scan2bim.paths import ProjectPaths

TEMPLATE = """\
# Project metadata for the Scan2BIM pipeline. Fill in what you know; leave the rest empty.
name: "{name}"
address: ""
floors:                    # number of storeys scanned (integer)
floor_to_floor_m:          # typical floor-to-floor height in metres, e.g. 2.6
use: unknown               # residential | office | commercial | industrial | other | unknown
building_state: unknown    # shell (obra gris) | finishing | occupied | unknown
scanner: ""                # e.g. "Leica RTC360", "XGRIDS L2 Pro"
registration_software: ""  # e.g. "Cyclone REGISTER 360", "LixelStudio"
crs: unknown               # e.g. "EPSG:9377" (CTM12), "EPSG:3116", "local", "unknown"
vertical: unknown          # orthometric | ellipsoidal | local | unknown
capture_date:              # YYYY-MM-DD
lod_target: 200
notes: ""
# Parameter overrides (only the keys that change), e.g.:
# overrides:
#   walls:
#     thickness_catalog: [0.10, 0.12, 0.15, 0.20]
overrides: {{}}
"""


class ProjectMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    address: str | None = None
    floors: int | None = None
    floor_to_floor_m: float | None = None
    use: Literal["residential", "office", "commercial", "industrial", "other", "unknown"] = (
        "unknown"
    )
    building_state: Literal["shell", "finishing", "occupied", "unknown"] = "unknown"
    scanner: str | None = None
    registration_software: str | None = None
    crs: str = "unknown"
    vertical: Literal["orthometric", "ellipsoidal", "local", "unknown"] = "unknown"
    capture_date: date | None = None
    lod_target: int = 200
    notes: str | None = None
    overrides: dict[str, Any] = Field(default_factory=dict)


def write_template(paths: ProjectPaths, overwrite: bool = False) -> Path:
    target = paths.project_file
    if target.exists() and not overwrite:
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(TEMPLATE.format(name=paths.project), encoding="utf-8")
    return target


def load_metadata(paths: ProjectPaths) -> ProjectMetadata | None:
    if not paths.project_file.exists():
        return None
    data = yaml.safe_load(paths.project_file.read_text(encoding="utf-8")) or {}
    return ProjectMetadata.model_validate(data)


def load_project_config(paths: ProjectPaths) -> tuple[PipelineConfig, ProjectMetadata | None]:
    meta = load_metadata(paths)
    cfg = load_config(meta.overrides if meta else None)
    return cfg, meta
