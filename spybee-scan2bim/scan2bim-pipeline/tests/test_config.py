from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from scan2bim.config import deep_merge, load_config
from scan2bim.paths import ProjectPaths
from scan2bim.project import load_project_config, write_template


def test_defaults_load() -> None:
    cfg = load_config()
    assert cfg.prep.voxel_size == pytest.approx(0.01)
    assert 0.15 in cfg.walls.thickness_catalog
    assert len(cfg.config_hash()) == 12


def test_override_is_merged_and_changes_hash() -> None:
    base = load_config()
    cfg = load_config({"walls": {"min_face_length": 0.8}})
    assert cfg.walls.min_face_length == pytest.approx(0.8)
    assert cfg.walls.ransac_distance == base.walls.ransac_distance
    assert cfg.config_hash() != base.config_hash()


def test_unknown_key_is_rejected() -> None:
    with pytest.raises(ValidationError):
        load_config({"walls": {"min_face_lenght": 0.8}})


def test_deep_merge_does_not_mutate_inputs() -> None:
    base = {"a": {"b": 1, "c": 2}}
    out = deep_merge(base, {"a": {"b": 5}})
    assert out == {"a": {"b": 5, "c": 2}}
    assert base == {"a": {"b": 1, "c": 2}}


def test_project_template_round_trip(data_root: Path) -> None:
    paths = ProjectPaths(data_root, "torre-norte")
    write_template(paths)
    cfg, meta = load_project_config(paths)
    assert meta is not None and meta.name == "torre-norte"
    assert cfg.prep.voxel_size == pytest.approx(0.01)
