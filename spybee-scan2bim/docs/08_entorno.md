# 08 · Entorno en Windows y solución de problemas

## Requisitos del PC

| Recurso | Mínimo | Recomendado |
|---|---|---|
| Sistema | Windows 10/11 de 64 bits | Windows 11 Pro |
| RAM | 32 GB (nubes ≤ ~200 M puntos) | 64–128 GB |
| Disco libre | 3 veces el tamaño de la nube | NVMe, con 200 GB o más libres |
| CPU | 8 núcleos | 16 o más |
| GPU | No hace falta en el MVP | NVIDIA con 16–32 GB para la fase de IA |
| Revit | La versión que usa operaciones | Con permisos para instalar add-ins en `%AppData%` |

## 1. Herramientas base (una sola vez)

1. **Git para Windows:** https://git-scm.com/download/win
2. **Claude Code:** sigue la instrucción oficial de instalación en Windows (https://docs.claude.com/en/docs/claude-code). Luego, en PowerShell, desde la carpeta del proyecto, ejecuta `claude`.
3. **Miniforge** (conda + mamba con conda-forge): https://github.com/conda-forge/miniforge. Instálalo "solo para mí" y abre "Miniforge Prompt", o ejecuta `conda init powershell`.
4. **.NET SDK 8:** https://dotnet.microsoft.com/download/dotnet/8.0. Es para el add-in de Revit 2025 o 2026. Para Revit 2024 o anterior también sirve el SDK 8 compilando a `net48`; si hace falta, instalar el "Developer Pack" de .NET Framework 4.8.
5. **(Opcional) CloudCompare:** https://www.danielgm.net/cc/. Sirve para mirar nubes y convertir formatos. Es gratis, con licencia GPL, y se usa como herramienta aparte, no como librería.

## 2. Entorno de Python

```powershell
mamba create -n scan2bim python=3.11 -y
conda activate scan2bim
pip install numpy scipy "open3d>=0.18" "laspy[lazrs]" pye57 "shapely>=2.0" scikit-image opencv-python-headless scikit-learn ifcopenshell pydantic pyyaml typer tqdm psutil matplotlib pytest
pip install -e .        # cuando exista pyproject.toml (T1.3)
python -c "import open3d, laspy, pye57, ifcopenshell, shapely, cv2; print('ok')"
```

- Si `pye57` falla en Windows, alternativas en orden de preferencia:
  1. `mamba install -c conda-forge pye57`;
  2. convertir el E57 a LAZ con CloudCompare (ver §4) y trabajar solo con LAZ.
- Si `open3d` no tiene versión para la versión de Python instalada, usar Python 3.10 o 3.11.
- **No instalar CUDA ni PyTorch** en el MVP.

## 3. Formatos de la nube: exportar a E57 o LAZ

| Formato de origen | Software | Cómo exportar |
|---|---|---|
| `.rcp` / `.rcs` (Autodesk ReCap) | ReCap Pro | Abrir el proyecto → Exportar → **E57** (o PTS). Si es muy grande, exportar por regiones o con submuestreo |
| `.fls` / proyecto SCENE (FARO) | FARO SCENE | Proyecto registrado → Exportar escaneos → **E57**, un solo archivo con todos los escaneos |
| `.lgs` / Cyclone (Leica) | Cyclone REGISTER 360 / Cyclone | Publicar o exportar → **E57** |
| NavVis | NavVis IVION / VLX processing | Exportar la nube como **E57 o LAS** |
| XGRIDS (Lixel) | LixelStudio | Exportar como **LAS** o PLY. Preferir LAS |
| `.pts`, `.ptx`, `.xyz`, `.ply` | CloudCompare | Abrir → Guardar como **LAS 1.4** (`.las`/`.laz`) |

Siempre: unidades en **metros**, con color si está disponible y **en el sistema de coordenadas del proyecto** (sin cambiarlo).

## 4. Nubes muy grandes: submuestreo previo con CloudCompare

Si el archivo es más grande que ~1/3 de la RAM libre, o es un solo escaneo SLAM de cientos de millones de puntos:

```powershell
& "C:\Program Files\CloudCompare\CloudCompare.exe" -SILENT -AUTO_SAVE OFF `
  -O "data\raw\<p>\nube.e57" -MERGE_CLOUDS -SS SPATIAL 0.01 `
  -C_EXPORT_FMT LAS -EXT laz -SAVE_CLOUDS FILE "data\work\<p>\cloud_cc_1cm.laz"
```

Revisar la sintaxis con la documentación de la línea de comandos de CloudCompare para la versión instalada. Después, `prep` lee ese LAZ en lugar del E57.

**Sobre las coordenadas grandes:** CloudCompare puede proponer un "global shift" al abrir coordenadas grandes. En modo silencioso lo aplica en memoria y lo revierte al guardar. Verificar en la ficha que las coordenadas del LAZ resultante sean las originales.

## 5. Revit

- Versión: revisar en `C:\Program Files\Autodesk\` qué carpetas `Revit 20XX` existen.
- Los add-ins se instalan en `%AppData%\Autodesk\Revit\Addins\<año>\`.
- En Revit en español, los comandos aparecen en **Complementos → Herramientas externas**.
- La primera vez que Revit carga el add-in, pregunta si confiar en él: elegir "Cargar siempre".
- **Cerrar Revit antes de recompilar**, porque bloquea la DLL.

## 6. Problemas frecuentes

| Problema | Solución |
|---|---|
| `MemoryError` o el PC se congela al leer | No leer todo de una. Usar lectura por bloques o submuestreo previo (§4). Revisar la RAM con `psutil` antes de leer |
| La nube aparece "plana" o deformada en los PNG | Coordenadas en float32 sin offset: restar el offset en float64 |
| Todos los puntos salen en un mismo lugar en Revit | Se vinculó la nube original con coordenadas CTM12. Vincular `cloud_local.las` de origen a origen |
| El modelo de Revit sale a 0,3048 veces o 3,28 veces el tamaño real | Falta la conversión de metros a pies (`UnitUtils.ConvertToInternalUnits`) |
| `dotnet build` no encuentra `RevitAPI.dll` | Revisar `RevitVersion` en el `.csproj` y la ruta de instalación de Revit |
| El add-in no aparece en Revit | Revisar el `.addin` en la carpeta del año correcto y que la ruta del ensamblado (`Assembly`) sea absoluta y exista |
| `open3d` es lento con nubes grandes | Trabajar por piso (`floors/F0X.laz`) y no sobre el edificio completo |
