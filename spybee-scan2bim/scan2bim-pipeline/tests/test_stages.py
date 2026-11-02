from __future__ import annotations

import json

import numpy as np
import pytest
from typer.testing import CliRunner

from scan2bim.cli import app
from scan2bim.georef import GeorefInfo
from scan2bim.io.readers import iter_chunks
from scan2bim.model import load_building
from scan2bim.paths import ProjectPaths
from scan2bim.project import load_project_config
from scan2bim.stages.inspect import run_inspect
from scan2bim.stages.prep import VoxelAccumulator, run_prep


def test_inspect_on_synthetic(synthetic_project: ProjectPaths) -> None:
    cfg, meta = load_project_config(synthetic_project)
    result = run_inspect(synthetic_project, cfg, meta)
    assert result.crs_guess == "ctm12"
    assert result.suggested_offset == [4_880_000.0, 2_066_000.0, 2_600.0]
    report = synthetic_project.out / "cloud_report.md"
    assert report.exists() and "ctm12" in report.read_text(encoding="utf-8")
    for name in ("top.png", "side_x.png", "side_y.png", "z_hist.png"):
        assert (synthetic_project.out / "debug" / "inspect" / name).stat().st_size > 10_000
    # floors at z=0 and 2.6 and ceilings at 2.48 and 5.08 must appear as peaks
    peaks = np.array(result.horizontal_surface_peaks_z_local)
    for expected in (0.0, 2.48, 2.6, 5.08):
        assert np.min(np.abs(peaks - expected)) < 0.05, (expected, peaks)


def test_voxel_accumulator_keeps_one_point_per_voxel() -> None:
    rng = np.random.default_rng(1)
    acc = VoxelAccumulator(0.1)
    pts = rng.uniform(0, 2, (50_000, 3)) + 4_880_000.0
    for part in np.array_split(pts, 7):
        acc.add(part, None)
    out, rgb = acc.result()
    assert rgb is None
    keys = np.floor(out / 0.1).astype(np.int64)
    assert len(np.unique(keys, axis=0)) == len(out)
    assert len(out) <= 20**3


def test_prep_on_synthetic(synthetic_project: ProjectPaths) -> None:
    cfg, meta = load_project_config(synthetic_project)
    cfg = cfg.model_copy(update={"prep": cfg.prep.model_copy(update={"voxel_size": 0.08})})
    result = run_prep(synthetic_project, cfg, meta, compute_normals=False)
    assert 0 < result.output_points < result.input_points
    assert result.offset == [4_880_000.0, 2_066_000.0, 2_600.0]
    assert result.crs == "EPSG:9377"
    georef = GeorefInfo.load(synthetic_project.georef_file)
    gt = load_building(synthetic_project.reference / "ground_truth.building.json")
    assert georef.offset == [gt.georef.offset.x, gt.georef.offset.y, gt.georef.offset.z]
    local = next(iter_chunks(synthetic_project.working_cloud, 10_000_000)).xyz
    assert np.abs(local).max() < 100  # local coordinates are small
    report = json.loads((synthetic_project.work / "prep_report.json").read_text(encoding="utf-8"))
    assert report["output_points"] == result.output_points


@pytest.mark.parametrize("command", ["levels", "walls", "export", "run-all"])
def test_unimplemented_stages_exit_with_code_2(
    command: str, synthetic_project: ProjectPaths
) -> None:
    runner = CliRunner()
    res = runner.invoke(
        app, [command, "-p", "synthetic-box", "--data-root", str(synthetic_project.data_root)]
    )
    assert res.exit_code == 2


def test_cli_help_and_version() -> None:
    runner = CliRunner()
    assert runner.invoke(app, ["--help"]).exit_code == 0
    assert runner.invoke(app, ["version"]).exit_code == 0
