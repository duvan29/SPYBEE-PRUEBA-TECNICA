from __future__ import annotations

from pathlib import Path

import pytest

from scan2bim.paths import ProjectPaths
from scan2bim.synthetic import SyntheticSpec, write_synthetic_project

FAST_SPEC = SyntheticSpec(spacing=0.06, floors=2)


@pytest.fixture
def data_root(tmp_path: Path) -> Path:
    root = tmp_path / "data"
    root.mkdir()
    return root


@pytest.fixture
def synthetic_project(data_root: Path) -> ProjectPaths:
    return write_synthetic_project(data_root, "synthetic-box", FAST_SPEC)
