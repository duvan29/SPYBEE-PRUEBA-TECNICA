from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from scan2bim.model import SCHEMA_VERSION, Building, json_schema, load_building
from scan2bim.synthetic import SyntheticSpec, make_synthetic_building

REPO = Path(__file__).resolve().parents[1]


def _example() -> dict:
    building = make_synthetic_building(SyntheticSpec(floors=1, spacing=0.5)).building
    return json.loads(building.model_dump_json())


def test_example_file_validates() -> None:
    building = load_building(REPO / "schema" / "examples" / "building.example.json")
    assert building.schema_version == SCHEMA_VERSION
    assert len(building.walls) == 5


def test_schema_file_is_in_sync_with_models() -> None:
    """Fails when model.py changed but `scan2bim schema` was not re-run."""
    on_disk = json.loads((REPO / "schema" / "building.schema.json").read_text(encoding="utf-8"))
    assert on_disk == json_schema(), "Run: scan2bim schema (and sync it to scan2bim-revit)"


def test_schema_declares_version() -> None:
    assert json_schema()["x-schema-version"] == SCHEMA_VERSION


def test_dangling_level_reference_is_rejected() -> None:
    data = _example()
    data["walls"][0]["base_level"] = "L99"
    with pytest.raises(ValidationError, match="unknown level 'L99'"):
        Building.model_validate(data)


def test_duplicate_ids_are_rejected() -> None:
    data = _example()
    data["walls"][1]["id"] = data["walls"][0]["id"]
    with pytest.raises(ValidationError, match="duplicate id"):
        Building.model_validate(data)


def test_opening_must_fit_in_host_wall() -> None:
    data = _example()
    data["openings"][0]["offset_along"] = 50.0
    with pytest.raises(ValidationError, match="does not fit"):
        Building.model_validate(data)


def test_unknown_fields_are_rejected() -> None:
    data = _example()
    data["walls"][0]["colour"] = "red"
    with pytest.raises(ValidationError):
        Building.model_validate(data)


def test_column_size_must_match_shape() -> None:
    data = _example()
    data["columns"][0]["size"] = [0.3]
    with pytest.raises(ValidationError, match="needs 2 size"):
        Building.model_validate(data)
