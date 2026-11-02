# Environment setup (Windows)

## 1. Machine

| Resource | Minimum | Recommended |
|---|---|---|
| OS | Windows 10/11 64-bit | Windows 11 Pro |
| RAM | 32 GB (clouds ≤ ~200 M points) | 64–128 GB |
| Free disk | 3× the cloud size | NVMe, ≥ 200 GB free |
| CPU | 8 cores | 16+ |
| GPU | Not needed for the MVP | NVIDIA 16–32 GB for the ML phase |
| Revit | The version operations uses | Permission to install add-ins in `%APPDATA%` |

## 2. Tools (one time)

1. **Git for Windows:** https://git-scm.com/download/win
2. **Claude Code:** follow the official installation guide (https://docs.anthropic.com/en/docs/claude-code),
   then run `claude` in the workspace folder.
3. **uv** (Python manager): https://docs.astral.sh/uv/getting-started/installation/ — PowerShell installer;
   uv downloads Python 3.12 by itself.
4. **.NET SDK 8** (or newer): https://dotnet.microsoft.com/download. For Revit ≤ 2024 the add-in targets
   .NET Framework 4.8; install the 4.8 Developer Pack if the build asks for it.
5. *(Optional)* **CloudCompare** (free, GPL, used as a separate tool): https://www.cloudcompare.org/ — to look at
   clouds and convert or decimate them.
6. *(Optional)* Visual Studio 2022 Community or VS Code with the C# Dev Kit, for debugging the add-in.

## 3. Python repo

```powershell
cd scan2bim-pipeline
uv sync --all-groups
uv run pre-commit install
uv run pytest
uv run scan2bim doctor
```

- If `open3d` or `pye57` fail to import, pin Python 3.11: `uv python pin 3.11; uv sync --all-groups`.
- If open3d fails with missing DLLs, install the latest "Microsoft Visual C++ Redistributable (x64)".
- No CUDA or PyTorch in the MVP.

## 4. C# repo

```powershell
cd scan2bim-revit
./scripts/bootstrap.ps1 -RevitVersion 2025   # use the installed year
./scripts/install.ps1  -RevitVersion 2025    # Revit closed
```

- If PowerShell blocks scripts, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- In Spanish Revit, the commands are under **Complementos → Herramientas externas**.
- The first time Revit loads the add-in it asks whether to trust it: choose "Cargar siempre" (Always load).

## 5. Cloud formats — export to E57 or LAS/LAZ

| Source | Software | How |
|---|---|---|
| `.rcp` / `.rcs` (ReCap) | ReCap Pro | Open the project → Export → **E57**; export by regions if it is huge |
| `.fls` / SCENE project (FARO) | FARO SCENE | Registered project → Export scans → **E57** (one file with all scans) |
| `.lgs` / Cyclone (Leica) | Cyclone REGISTER 360 / Cyclone | Publish / Export → **E57** |
| NavVis | IVION / NavVis processing | Export cloud as **E57 or LAS** |
| XGRIDS (Lixel) | LixelStudio | Export **LAS** (preferred) or PLY |
| `.pts`, `.ptx`, `.xyz`, `.ply` | CloudCompare | Open → Save as **LAS 1.4** (`.las` / `.laz`) |

Always export in **metres**, with colour if available, in the **project coordinate system** (do not change it).

## 6. Very large clouds — pre-decimate with CloudCompare

Use this when one file is bigger than about 1/3 of the free RAM, or for a single SLAM scan with hundreds of
millions of points:

The pipeline reads **every** cloud file in `raw/<p>/`, so the original and its decimated copy must not sit
there together. With the user's OK:

1. The **user** moves the original E57 to `data/originals/<p>/`, the read-only archive. Claude never moves
   anything out of `raw/`.
2. Write the decimated LAZ into `raw/<p>/`:

```powershell
& "C:\Program Files\CloudCompare\CloudCompare.exe" -SILENT -AUTO_SAVE OFF `
  -O "data\originals\<p>\cloud.e57" -MERGE_CLOUDS -SS SPATIAL 0.01 `
  -C_EXPORT_FMT LAS -EXT laz -SAVE_CLOUDS FILE "data\raw\<p>\cloud_cc_1cm.laz"
```

- Check the flags against the CloudCompare command-line wiki for the installed version.
- Record the decimation (tool, version, spacing) in `data/projects/<p>.yaml` → `notes`.
- CloudCompare may apply a "global shift" in memory for large coordinates. Verify with `inspect` that the
  output keeps the original coordinates.

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| `MemoryError` / the PC freezes | Do not read everything at once; pre-decimate (§6); check free RAM with `scan2bim doctor` |
| Cloud looks "flat" or blocky in the PNGs | float32 used before subtracting the offset — keep float64 until `to_local` |
| Everything far away in Revit | The original CTM12 cloud was linked; link `cloud_local.las` origin to origin |
| Revit model ×0.3048 or ×3.28 the real size | Missing metre ↔ foot conversion (`RevitUnits`) |
| `dotnet build` cannot find RevitAPI.dll | Check `-p:RevitVersion` / `RevitInstallDir` |
| Add-in not listed in Revit | Manifest in the wrong year folder, or the `<Assembly>` path does not exist |
| open3d slow | Work per storey (`floors/F0X.laz`), not on the whole building |
