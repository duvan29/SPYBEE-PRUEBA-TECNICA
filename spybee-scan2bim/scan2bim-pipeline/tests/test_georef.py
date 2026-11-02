from __future__ import annotations

import numpy as np
import pytest

from scan2bim.georef import compute_offset, guess_crs, reproject_xy, to_local, to_world


def test_offset_is_round_and_noise_robust() -> None:
    lo = np.array([4_879_999.996, 2_065_999.99, 2_599.99])
    hi = np.array([4_880_032.0, 2_066_028.0, 2_606.0])
    np.testing.assert_allclose(compute_offset(lo, hi), [4_880_000.0, 2_066_000.0, 2_600.0])


def test_small_coordinates_get_no_offset() -> None:
    np.testing.assert_allclose(compute_offset(np.array([-5, -3, 0]), np.array([30, 20, 9])), 0.0)


def test_local_world_round_trip_keeps_millimetres() -> None:
    world = np.array([[4_880_123.4567, 2_066_456.7891, 2_601.2345]])
    offset = np.array([4_880_000.0, 2_066_000.0, 2_600.0])
    local = to_local(world, offset)
    assert local.dtype == np.float32
    np.testing.assert_allclose(to_world(local, offset), world, atol=1e-3)


@pytest.mark.parametrize(
    ("lo", "hi", "kind"),
    [
        ([4_880_000, 2_066_000, 2600], [4_880_050, 2_066_030, 2620], "ctm12"),
        ([999_000, 1_000_000, 2600], [999_050, 1_000_030, 2620], "magna_gauss_kruger"),
        ([-12, -8, -1], [40, 30, 20], "local"),
    ],
)
def test_guess_crs(lo: list[float], hi: list[float], kind: str) -> None:
    assert guess_crs(np.array(lo, float), np.array(hi, float)).kind == kind


def test_bogota_lonlat_to_ctm12_is_in_expected_range() -> None:
    xyz = np.array([[-74.0817, 4.6097, 2600.0]])  # Plaza de Bolivar, MAGNA-SIRGAS geographic
    out = reproject_xy(xyz, "EPSG:4686", "EPSG:9377")
    assert 4_850_000 < out[0, 0] < 4_910_000
    assert 2_030_000 < out[0, 1] < 2_100_000
    assert out[0, 2] == pytest.approx(2600.0)  # heights are never changed


def test_bogota_zone_to_ctm12_round_trip_submillimetre() -> None:
    xyz = np.array([[1_000_500.123, 1_001_200.456, 2600.0]])
    there = reproject_xy(xyz, "EPSG:3116", "EPSG:9377")
    back = reproject_xy(there, "EPSG:9377", "EPSG:3116")
    np.testing.assert_allclose(back, xyz, atol=1e-3)
