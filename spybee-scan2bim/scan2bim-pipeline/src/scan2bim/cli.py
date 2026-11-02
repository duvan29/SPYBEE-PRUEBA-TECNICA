"""Command line interface: ``scan2bim <command> --project <name>``.

Implemented: doctor, init-project, synth, schema, inspect, prep.
Every other stage is wired but exits with code 2 and points to its task in
docs/plan/EXECUTION_PLAN.md until it is implemented.
"""

from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, NoReturn

import typer

from scan2bim import __version__
from scan2bim.log import setup_logging
from scan2bim.paths import ProjectPaths, resolve_data_root

app = typer.Typer(
    name="scan2bim",
    help="Spybee Scan2BIM pipeline: point cloud -> building.json -> IFC / Revit.",
    no_args_is_help=True,
    add_completion=False,
)

ProjectOpt = Annotated[
    str, typer.Option("--project", "-p", help="Project folder name, e.g. torre-norte.")
]
DataRootOpt = Annotated[
    Path | None,
    typer.Option(
        "--data-root", envvar="SCAN2BIM_DATA_ROOT", help="Data folder (default: ./data or ../data)."
    ),
]


def _paths(project: str, data_root: Path | None) -> ProjectPaths:
    return ProjectPaths(resolve_data_root(data_root), project)


def _not_implemented(task: str) -> NoReturn:
    typer.secho(
        f"Not implemented yet - see task {task} in docs/plan/EXECUTION_PLAN.md.",
        fg=typer.colors.YELLOW,
        err=True,
    )
    raise typer.Exit(code=2)


@app.callback()
def main(
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Debug logging.")] = False,
) -> None:
    setup_logging(verbose)


@app.command()
def version() -> None:
    """Print the package version."""
    typer.echo(__version__)


@app.command()
def doctor(data_root: DataRootOpt = None) -> None:
    """Check the machine and Python environment (task T1.1)."""
    from scan2bim.doctor import report

    typer.echo(report(resolve_data_root(data_root)))


@app.command("init-project")
def init_project(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Create data/projects/<project>.yaml and the raw/reference folders."""
    from scan2bim.project import write_template

    paths = _paths(project, data_root)
    paths.raw.mkdir(parents=True, exist_ok=True)
    paths.reference.mkdir(parents=True, exist_ok=True)
    target = write_template(paths)
    typer.echo(f"Project file: {target}\nPut the point cloud in: {paths.raw}")


@app.command()
def synth(
    project: Annotated[str, typer.Option("--project", "-p")] = "synthetic-box",
    data_root: DataRootOpt = None,
    spacing: Annotated[float, typer.Option(help="Point spacing in metres.")] = 0.03,
    floors: Annotated[int, typer.Option(help="Number of storeys.")] = 2,
) -> None:
    """Generate a synthetic building (cloud + ground truth) for testing."""
    from scan2bim.synthetic import SyntheticSpec, write_synthetic_project

    paths = write_synthetic_project(
        resolve_data_root(data_root), project, SyntheticSpec(spacing=spacing, floors=floors)
    )
    typer.echo(f"Synthetic project written to {paths.raw} (ground truth in {paths.reference})")


@app.command()
def schema(
    output: Annotated[Path, typer.Option(help="Where to write the JSON Schema.")] = Path(
        "schema/building.schema.json"
    ),
    example: Annotated[
        Path | None, typer.Option(help="Also write an example building.json here.")
    ] = Path("schema/examples/building.example.json"),
) -> None:
    """Write the building.json JSON Schema (and an example) from the pydantic models."""
    from scan2bim.model import save_building, write_json_schema
    from scan2bim.synthetic import SyntheticSpec, make_synthetic_building

    write_json_schema(output)
    typer.echo(f"Schema written to {output}")
    if example is not None:
        building = make_synthetic_building(SyntheticSpec(floors=1, spacing=0.5)).building
        fixed = building.generator.model_copy(update={"created": datetime(2026, 1, 1, tzinfo=UTC)})
        save_building(building.model_copy(update={"generator": fixed}), example)  # deterministic
        typer.echo(f"Example written to {example}")


@app.command()
def inspect(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Cloud report + debug PNGs without loading the full cloud (task T1.4)."""
    from scan2bim.project import load_project_config
    from scan2bim.stages.inspect import run_inspect

    paths = _paths(project, data_root)
    cfg, meta = load_project_config(paths)
    result = run_inspect(paths, cfg, meta)
    typer.echo(f"Report: {paths.out / 'cloud_report.md'} ({result.total_points:,} points)")


@app.command()
def prep(
    project: ProjectOpt,
    data_root: DataRootOpt = None,
    normals: Annotated[
        bool, typer.Option("--normals/--no-normals", help="Compute normals (open3d).")
    ] = True,
) -> None:
    """Voxel down-sampling, local offset, cleaning and normals (task T1.5)."""
    from scan2bim.project import load_project_config
    from scan2bim.stages.prep import run_prep

    paths = _paths(project, data_root)
    cfg, meta = load_project_config(paths)
    result = run_prep(paths, cfg, meta, compute_normals=normals)
    typer.echo(
        f"Working cloud: {paths.working_cloud} ({result.output_points:,} points, "
        f"offset {result.offset}, normals={result.normals})"
    )


@app.command()
def levels(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Detect levels and split the cloud per storey (tasks T2.1-T2.3)."""
    _not_implemented("T2.2")


@app.command()
def slabs(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Slab outlines and thickness (task T2.4)."""
    _not_implemented("T2.4")


@app.command()
def walls(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Wall faces, pairing, regularisation and heights (tasks T4.1-T4.6)."""
    _not_implemented("T4.1")


@app.command()
def columns(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Free-standing and embedded columns (task T6.1)."""
    _not_implemented("T6.1")


@app.command()
def openings(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Doors, windows and openings per wall (task T6.2)."""
    _not_implemented("T6.2")


@app.command()
def spaces(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Rooms / spaces from the wall layout (task T6.3)."""
    _not_implemented("T6.3")


@app.command()
def export(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Write building.json, model.ifc and cloud_local.las (tasks T2.5, T3.1, T3.2)."""
    _not_implemented("T2.5")


@app.command()
def qa(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Per-element cloud-to-model deviation report (task T7.2)."""
    _not_implemented("T7.2")


@app.command()
def evaluate(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Compare against the reference model in data/reference (task T7.3)."""
    _not_implemented("T7.3")


@app.command("run-all")
def run_all(project: ProjectOpt, data_root: DataRootOpt = None) -> None:
    """Run every stage end to end (task T7.5)."""
    _not_implemented("T7.5")
