"""``scan2bim doctor``: environment diagnostics for task T1.1."""

from __future__ import annotations

import importlib
import platform
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGES = [
    "numpy",
    "scipy",
    "laspy",
    "lazrs",
    "pye57",
    "open3d",
    "shapely",
    "pyproj",
    "skimage",
    "cv2",
    "sklearn",
    "ifcopenshell",
    "pydantic",
    "yaml",
    "typer",
    "matplotlib",
    "psutil",
]


def _version(name: str) -> str:
    try:
        mod = importlib.import_module(name)
    except Exception as exc:  # report every failure mode (missing DLLs, etc.)
        return f"MISSING ({type(exc).__name__}: {str(exc)[:60]})"
    version = getattr(mod, "__version__", None)
    return str(version) if isinstance(version, str) else "ok"


def _gpu() -> str:
    if shutil.which("nvidia-smi") is None:
        return "no NVIDIA driver found (not needed for the MVP)"
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return out.stdout.strip() or "nvidia-smi returned nothing"
    except (OSError, subprocess.SubprocessError) as exc:
        return f"nvidia-smi failed: {exc}"


def _revit_versions() -> list[str]:
    base = Path("C:/Program Files/Autodesk")
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.glob("Revit 20*") if (p / "RevitAPI.dll").exists())


def report(data_root: Path) -> str:
    import psutil

    vm = psutil.virtual_memory()
    disk_target = data_root if data_root.exists() else Path.cwd()
    disk = shutil.disk_usage(disk_target)
    lines = [
        "# scan2bim doctor",
        "",
        f"- OS: {platform.platform()}",
        f"- Python: {sys.version.split()[0]} ({sys.executable})",
        f"- CPU: {platform.processor() or 'n/a'} / logical cores: {psutil.cpu_count()}",
        f"- RAM: total {vm.total / 1e9:.1f} GB, available {vm.available / 1e9:.1f} GB",
        f"- Disk free at {disk_target}: {disk.free / 1e9:.1f} GB",
        f"- GPU: {_gpu()}",
        f"- Revit installs with API: {_revit_versions() or 'none found'}",
        f"- dotnet: {shutil.which('dotnet') or 'not found'}",
        f"- git: {shutil.which('git') or 'not found'}",
        f"- Data root: {data_root} (exists: {data_root.exists()})",
        "",
        "## Python packages",
        "",
    ]
    lines += [f"- {name}: {_version(name)}" for name in PACKAGES]
    return "\n".join(lines) + "\n"
