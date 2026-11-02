"""Logging helpers: consistent format, per-stage timing and memory."""

from __future__ import annotations

import logging
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field

LOGGER_NAME = "scan2bim"


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s", "%H:%M:%S")
    )
    root = logging.getLogger(LOGGER_NAME)
    root.handlers[:] = [handler]
    root.setLevel(level)
    root.propagate = False


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"{LOGGER_NAME}.{name}")


def peak_rss_mb() -> float | None:
    """Peak resident memory of this process in MB (best effort, cross-platform)."""
    try:
        import psutil

        info = psutil.Process().memory_info()
        peak = getattr(info, "peak_wset", None)  # Windows
        if peak is not None:
            return float(peak) / 1e6
    except ImportError:  # pragma: no cover
        pass
    try:
        import resource

        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return usage / 1e3 if sys.platform != "darwin" else usage / 1e6
    except (ImportError, AttributeError):  # pragma: no cover
        return None


def available_ram_bytes() -> int | None:
    try:
        import psutil

        return int(psutil.virtual_memory().available)
    except ImportError:  # pragma: no cover
        return None


@dataclass
class StageStats:
    name: str
    seconds: float = 0.0
    peak_rss_mb: float | None = None
    extra: dict[str, float | int | str] = field(default_factory=dict)


@contextmanager
def stage(name: str) -> Iterator[StageStats]:
    """Time a pipeline stage and log duration + peak memory when it ends."""
    log = get_logger(name)
    stats = StageStats(name=name)
    start = time.perf_counter()
    log.info("start")
    try:
        yield stats
    finally:
        stats.seconds = time.perf_counter() - start
        stats.peak_rss_mb = peak_rss_mb()
        mem = f"{stats.peak_rss_mb:.0f} MB" if stats.peak_rss_mb else "n/a"
        log.info("done in %.1f s (peak RSS %s)", stats.seconds, mem)
