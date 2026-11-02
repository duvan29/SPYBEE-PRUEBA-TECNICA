from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from scan2bim.io.readers import UnsupportedCloudError, find_cloud_files, iter_chunks, read_info
from scan2bim.io.writers import write_las
from scan2bim.model import load_building
from scan2bim.paths import ProjectPaths
from scan2bim.synthetic import SyntheticSpec, make_synthetic_building


def test_laz_round_trip_keeps_millimetres_and_colour(tmp_path: Path) -> None:
    rng = np.random.default_rng(0)
    xyz = rng.uniform(0, 30, (1000, 3)) + np.array([4_880_000.0, 2_066_000.0, 2_600.0])
    rgb = rng.integers(0, 255, (1000, 3), dtype=np.uint8)
    path = tmp_path / "c.laz"
    write_las(path, xyz, rgb=rgb, crs_epsg=9377)
    info = read_info(path)
    assert info.point_count == 1000 and info.has_color
    chunk = next(iter_chunks(path, 10_000))
    np.testing.assert_allclose(chunk.xyz, xyz, atol=1e-3)
    assert chunk.rgb is not None
    np.testing.assert_array_equal(chunk.rgb, rgb)


def test_e57_round_trip(tmp_path: Path) -> None:
    pye57 = pytest.importorskip("pye57")
    n = 500
    data = {
        "cartesianX": np.linspace(0, 5, n),
        "cartesianY": np.linspace(0, 3, n),
        "cartesianZ": np.linspace(0, 2, n),
        "colorRed": np.full(n, 200, np.uint8),
        "colorGreen": np.full(n, 100, np.uint8),
        "colorBlue": np.full(n, 50, np.uint8),
    }
    path = tmp_path / "c.e57"
    e57 = pye57.E57(str(path), mode="w")
    e57.write_scan_raw(data)
    e57.close()
    info = read_info(path)
    assert info.point_count == n and info.has_color
    chunks = list(iter_chunks(path, 200))
    assert sum(len(c) for c in chunks) == n


def test_proprietary_only_folder_explains_what_to_do(tmp_path: Path) -> None:
    (tmp_path / "scan.rcp").write_bytes(b"x")
    with pytest.raises(UnsupportedCloudError, match="Export an E57"):
        find_cloud_files(tmp_path)


def test_synthetic_ground_truth_is_consistent() -> None:
    result = make_synthetic_building(SyntheticSpec(spacing=0.1))
    b = result.building
    assert [lv.name for lv in b.levels] == ["Level 1", "Level 2", "Roof"]
    assert len(b.walls) == 10 and len(b.openings) == 4 and len(b.columns) == 2
    assert len(b.spaces) == 4
    local = result.xyz_world - np.array([b.georef.offset.x, b.georef.offset.y, b.georef.offset.z])
    assert local[:, 0].min() > 9.9 and local[:, 0].max() < 22.1  # origin (10, 10), width 12
    assert local[:, 2].min() > -0.05 and local[:, 2].max() < 5.1


def test_synthetic_project_files(synthetic_project: ProjectPaths) -> None:
    assert (synthetic_project.raw / "synthetic.laz").exists()
    assert synthetic_project.project_file.exists()
    gt = load_building(synthetic_project.reference / "ground_truth.building.json")
    assert gt.georef.crs == "EPSG:9377"
