"""The ``building.json`` contract.

This module is the **single source of truth** for the data exchanged between the Python
pipeline and the Revit add-in (C#). The JSON Schema in ``schema/building.schema.json`` is
generated from these models (``scan2bim schema``) and copied to the ``scan2bim-revit`` repo.

Conventions (see docs/architecture/BUILDING_JSON_CONTRACT.md):
- Units: metres and degrees.
- Coordinates: local = world - georef.offset, z up. Plan coordinates are [x, y].
- Polygons: counter-clockwise, first vertex not repeated.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import date, datetime
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = "0.1.0"
"""Semantic version of the contract. Bump MINOR for additive changes, MAJOR for breaking ones."""

Point2 = tuple[float, float]
Polygon2 = Annotated[list[Point2], Field(min_length=3)]
MetricValue = float | int | bool


class Status(StrEnum):
    """Whether an element can be trusted as-is or must be reviewed by a modeller."""

    AUTO = "auto"
    REVIEW = "review"


class ReviewReason(StrEnum):
    """Machine-readable reasons why an element was flagged for review."""

    ONE_FACE = "one_face"
    LOW_COVERAGE = "low_coverage"
    HIGH_RESIDUAL = "high_residual"
    VERTICAL_DISCONTINUITY = "vertical_discontinuity"
    THICKNESS_OUT_OF_CATALOG = "thickness_out_of_catalog"
    NON_ORTHOGONAL = "non_orthogonal"
    OCCLUSION_PARTIAL = "occlusion_partial"
    EMBEDDED = "embedded"
    THICKNESS_DEFAULT = "thickness_default"
    CLUTTER = "clutter"
    LEVEL_MERGED = "level_merged"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Element(_Strict):
    """Fields shared by every detected element."""

    id: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    status: Status
    reasons: list[ReviewReason] = Field(default_factory=list)
    metrics: dict[str, MetricValue] = Field(default_factory=dict)


class Level(Element):
    name: str
    elevation: float


class Slab(Element):
    level: str
    outline: Polygon2
    holes: list[Polygon2] = Field(default_factory=list)
    top_offset: float = 0.0
    thickness: float = Field(gt=0.0)


class Wall(Element):
    base_level: str
    top_level: str | None = None
    axis: tuple[Point2, Point2]
    thickness: float = Field(gt=0.0)
    base_offset: float = 0.0
    height: float = Field(gt=0.0)
    faces_seen: Literal[1, 2] = 2
    material_guess: Literal["masonry", "concrete", "drywall", "unknown"] = "unknown"

    @property
    def length(self) -> float:
        (x0, y0), (x1, y1) = self.axis
        return float(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)


class Column(Element):
    base_level: str
    top_level: str | None = None
    center: Point2
    shape: Literal["rect", "circle"]
    size: list[Annotated[float, Field(gt=0.0)]] = Field(min_length=1, max_length=2)
    rotation_deg: float = 0.0
    embedded_in: str | None = None

    @model_validator(mode="after")
    def _size_matches_shape(self) -> Column:
        expected = 2 if self.shape == "rect" else 1
        if len(self.size) != expected:
            raise ValueError(
                f"column {self.id}: shape '{self.shape}' needs {expected} size value(s)"
            )
        return self


class Opening(Element):
    host: str
    kind: Literal["door", "window", "opening"]
    offset_along: float = Field(ge=0.0)
    width: float = Field(gt=0.0)
    height: float = Field(gt=0.0)
    sill: float = Field(ge=0.0)


class Space(Element):
    level: str
    polygon: Polygon2
    seed: Point2
    area: float = Field(ge=0.0)
    name_guess: str | None = None


class GeneratorInfo(_Strict):
    name: str = "scan2bim"
    version: str
    git: str | None = None
    created: datetime
    config_hash: str | None = None


class ProjectInfo(_Strict):
    id: str
    name: str
    capture_date: date | None = None
    scanner: str | None = None
    building_state: Literal["shell", "finishing", "occupied", "unknown"] = "unknown"


class Offset(_Strict):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class Georef(_Strict):
    crs: str = "local"
    offset: Offset = Field(default_factory=Offset)
    true_north_deg: float = 0.0
    vertical: Literal["orthometric", "ellipsoidal", "local", "unknown"] = "unknown"


class Summary(_Strict):
    counts: dict[str, int] = Field(default_factory=dict)
    review_counts: dict[str, int] = Field(default_factory=dict)
    timings_s: dict[str, float] = Field(default_factory=dict)


class Building(_Strict):
    """Root object of ``building.json``."""

    model_config = ConfigDict(
        extra="forbid",
        title="SpybeeBuilding",
        json_schema_extra={"x-schema-version": SCHEMA_VERSION},
    )

    schema_version: str = SCHEMA_VERSION
    generator: GeneratorInfo
    project: ProjectInfo
    georef: Georef = Field(default_factory=Georef)
    dominant_direction_deg: float | None = None
    levels: list[Level] = Field(default_factory=list)
    slabs: list[Slab] = Field(default_factory=list)
    walls: list[Wall] = Field(default_factory=list)
    columns: list[Column] = Field(default_factory=list)
    openings: list[Opening] = Field(default_factory=list)
    spaces: list[Space] = Field(default_factory=list)
    summary: Summary | None = None

    @model_validator(mode="after")
    def _check_integrity(self) -> Building:
        errors = integrity_errors(self)
        if errors:
            raise ValueError("building.json integrity errors: " + "; ".join(errors[:20]))
        return self

    def all_elements(self) -> list[Element]:
        return [
            *self.levels,
            *self.slabs,
            *self.walls,
            *self.columns,
            *self.openings,
            *self.spaces,
        ]


def integrity_errors(b: Building) -> list[str]:
    """Return human-readable integrity problems (empty list when valid)."""
    errors: list[str] = []

    if b.schema_version.split(".")[0] != SCHEMA_VERSION.split(".")[0]:
        errors.append(f"schema_version {b.schema_version} incompatible with {SCHEMA_VERSION}")

    counts = Counter(e.id for e in b.all_elements())
    errors.extend(f"duplicate id '{i}'" for i, n in counts.items() if n > 1)

    level_ids = {lv.id for lv in b.levels}

    def need_level(owner: str, ref: str | None, optional: bool = False) -> None:
        if ref is None and optional:
            return
        if ref not in level_ids:
            errors.append(f"{owner}: unknown level '{ref}'")

    for s in b.slabs:
        need_level(s.id, s.level)
    for w in b.walls:
        need_level(w.id, w.base_level)
        need_level(w.id, w.top_level, optional=True)
        if w.length <= 1e-6:
            errors.append(f"{w.id}: zero-length axis")
    for c in b.columns:
        need_level(c.id, c.base_level)
        need_level(c.id, c.top_level, optional=True)
    for sp in b.spaces:
        need_level(sp.id, sp.level)

    walls = {w.id: w for w in b.walls}
    for o in b.openings:
        host = walls.get(o.host)
        if host is None:
            errors.append(f"{o.id}: unknown host wall '{o.host}'")
        elif o.offset_along + o.width > host.length + 0.01:
            errors.append(f"{o.id}: does not fit in host wall {o.host} ({host.length:.2f} m)")

    errors.extend(_polygon_errors(b))
    return errors


def _polygon_errors(b: Building) -> list[str]:
    from shapely.geometry import Polygon

    errors: list[str] = []
    polys: list[tuple[str, list[Point2]]] = [(s.id, s.outline) for s in b.slabs]
    polys += [(f"{s.id}.hole", h) for s in b.slabs for h in s.holes]
    polys += [(sp.id, sp.polygon) for sp in b.spaces]
    for owner, pts in polys:
        poly = Polygon(pts)
        if not poly.is_valid or poly.area <= 0:
            errors.append(f"{owner}: invalid or self-intersecting polygon")
    return errors


def load_building(path: Path) -> Building:
    return Building.model_validate_json(path.read_text(encoding="utf-8"))


def save_building(building: Building, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(building.model_dump_json(indent=2), encoding="utf-8")


def json_schema() -> dict[str, Any]:
    """JSON Schema of the contract (written to schema/building.schema.json)."""
    schema = Building.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return schema


def write_json_schema(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_schema(), indent=2) + "\n", encoding="utf-8")
