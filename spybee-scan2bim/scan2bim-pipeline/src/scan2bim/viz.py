"""Debug PNGs. Every stage writes at least one image; Claude must LOOK at them.

Headless (Agg backend), max ~2000 px, metres on the axes, grey cloud + coloured results.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

MAX_PLOT_POINTS = 400_000


def _thin(points: NDArray[np.floating], max_points: int = MAX_PLOT_POINTS) -> NDArray[np.floating]:
    if len(points) <= max_points:
        return points
    step = int(np.ceil(len(points) / max_points))
    return points[::step]


def plot_top(xyz: NDArray[np.floating], path: Path, title: str) -> None:
    pts = _thin(xyz)
    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    sc = ax.scatter(pts[:, 0], pts[:, 1], c=pts[:, 2], s=0.2, cmap="viridis", linewidths=0)
    fig.colorbar(sc, ax=ax, label="z [m]")
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_side(xyz: NDArray[np.floating], path: Path, title: str, axis: int = 0) -> None:
    pts = _thin(xyz)
    fig, ax = plt.subplots(figsize=(14, 6), dpi=150)
    ax.scatter(pts[:, axis], pts[:, 2], s=0.2, c="0.3", linewidths=0)
    ax.set_aspect("equal")
    ax.set_xlabel(f"{'xy'[axis]} [m]")
    ax.set_ylabel("z [m]")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_histogram(
    values: NDArray[np.floating],
    bin_size: float,
    path: Path,
    title: str,
    xlabel: str,
    peaks: list[float] | None = None,
) -> None:
    lo, hi = float(np.min(values)), float(np.max(values))
    bins = max(int(np.ceil((hi - lo) / bin_size)), 1)
    fig, ax = plt.subplots(figsize=(12, 5), dpi=150)
    ax.hist(values, bins=bins, color="0.4")
    for p in peaks or []:
        ax.axvline(p, color="tab:red", linewidth=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("points")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
