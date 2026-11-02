"""Data folder layout (shared by every stage).

The data root lives OUTSIDE the git repositories (see the workspace data/README.md)::

    <data_root>/raw/<project>/        original deliverable from the scan leader (READ-ONLY)
    <data_root>/projects/<project>.yaml   project metadata + config overrides
    <data_root>/reference/<project>/  manually modelled RVT/IFC used for evaluation
    <data_root>/work/<project>/       intermediates (safe to delete and regenerate)
    <data_root>/out/<project>/        deliverables + debug PNGs
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

ENV_DATA_ROOT = "SCAN2BIM_DATA_ROOT"
_PROJECT_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


class ProjectNameError(ValueError):
    pass


def validate_project_name(name: str) -> str:
    if not _PROJECT_RE.match(name):
        raise ProjectNameError(
            f"Invalid project name '{name}': use lowercase letters, digits and '-' "
            "(no spaces or accents), e.g. 'torre-norte'."
        )
    return name


def resolve_data_root(explicit: Path | None = None, cwd: Path | None = None) -> Path:
    """Find the data root: --data-root > $SCAN2BIM_DATA_ROOT > ./data > ../data."""
    if explicit is not None:
        return explicit.resolve()
    env = os.environ.get(ENV_DATA_ROOT)
    if env:
        return Path(env).resolve()
    here = (cwd or Path.cwd()).resolve()
    for candidate in (here / "data", here.parent / "data"):
        if candidate.is_dir():
            return candidate
    return (here.parent / "data").resolve()


@dataclass(frozen=True)
class ProjectPaths:
    data_root: Path
    project: str

    def __post_init__(self) -> None:
        validate_project_name(self.project)

    @property
    def raw(self) -> Path:
        return self.data_root / "raw" / self.project

    @property
    def project_file(self) -> Path:
        return self.data_root / "projects" / f"{self.project}.yaml"

    @property
    def reference(self) -> Path:
        return self.data_root / "reference" / self.project

    @property
    def work(self) -> Path:
        return self.data_root / "work" / self.project

    @property
    def out(self) -> Path:
        return self.data_root / "out" / self.project

    def debug(self, stage: str) -> Path:
        path = self.out / "debug" / stage
        path.mkdir(parents=True, exist_ok=True)
        return path

    def ensure_outputs(self) -> None:
        self.work.mkdir(parents=True, exist_ok=True)
        self.out.mkdir(parents=True, exist_ok=True)

    # Well-known artefacts --------------------------------------------------------------
    @property
    def working_cloud(self) -> Path:
        return self.work / "cloud_work.laz"

    @property
    def normals_file(self) -> Path:
        return self.work / "normals.npz"

    @property
    def georef_file(self) -> Path:
        return self.work / "georef.json"

    @property
    def building_json(self) -> Path:
        return self.out / "building.json"

    @property
    def ifc_file(self) -> Path:
        return self.out / "model.ifc"

    @property
    def local_cloud(self) -> Path:
        return self.out / "cloud_local.las"
