# 02 · Arquitectura del código

## Flujo

```
data/raw/<p>/*.e57|las|laz
   │  inspect  → out/<p>/ficha.md + debug/inspect/*.png
   │  prep     → work/<p>/cloud_1cm.laz, normals.npz, georef.json
   │  levels   → work/<p>/levels.json, floors/F01.laz …
   │  slabs    → work/<p>/slabs.json
   │  walls    → work/<p>/walls.json
   │  columns  → work/<p>/columns.json
   │  openings → work/<p>/openings.json
   │  spaces   → work/<p>/spaces.json
   │  export   → out/<p>/building.json, model.ifc, cloud_local.las
   │  qa       → out/<p>/qa.html
   │  eval     → out/<p>/eval.json   (si hay data/reference/<p>/)
   ▼
Revit: add-in "Spybee: Generar modelo" lee building.json → RVT nativo
Revit: "Spybee: Exportar correcciones" → corrections.json
```

**Las etapas son independientes y reanudables.**
- Cada una lee los resultados de la anterior desde `work/` y escribe los suyos ahí.
- Si un archivo de salida ya existe y es más nuevo que sus entradas, la etapa se salta, salvo que se pase `--force`.
- Así se puede iterar sobre `walls` sin volver a correr `prep`, que es la etapa lenta.

## Estructura del repositorio

```
scan2bim/                      # repo local (raíz = esta carpeta)
├── CLAUDE.md  README.md  PROGRESO.md  .gitignore
├── pyproject.toml             # paquete "scan2bim", dependencias, pytest
├── config/
│   └── default.yaml           # TODOS los parámetros (ver abajo)
├── scan2bim/
│   ├── __init__.py
│   ├── __main__.py            # permite `python -m scan2bim`
│   ├── cli.py                 # argparse o typer: subcomandos
│   ├── config.py              # carga YAML + overrides por proyecto (data/raw/<p>/config.yaml opcional)
│   ├── paths.py               # rutas raw/work/out/debug por proyecto
│   ├── log.py                 # logging con tiempos por etapa y RAM máxima
│   ├── io/
│   │   ├── readers.py         # E57 (pye57) y LAS/LAZ (laspy), lectura por bloques
│   │   └── writers.py         # LAZ/LAS, npz
│   ├── geometry/
│   │   ├── planes.py          # RANSAC de planos, normales, verticalidad
│   │   ├── lines2d.py         # segmentos 2D, emparejamiento, colinealidad
│   │   ├── polygons.py        # casco cóncavo, simplificación, ortogonalización
│   │   └── raster.py          # rasterización 2D, componentes conexos
│   ├── stages/
│   │   ├── inspect.py
│   │   ├── prep.py
│   │   ├── levels.py
│   │   ├── slabs.py
│   │   ├── walls.py
│   │   ├── columns.py
│   │   ├── openings.py
│   │   ├── spaces.py
│   │   ├── confidence.py
│   │   ├── export_json.py
│   │   ├── export_ifc.py
│   │   ├── qa.py
│   │   └── evaluate.py
│   ├── model.py               # dataclasses/pydantic de building.json + validación
│   └── viz.py                 # PNG de depuración (matplotlib, sin ventanas: backend Agg)
├── revit/
│   ├── Spybee.Scan2BIM.Revit/ # proyecto C# (ver 05_revit_addin.md)
│   └── install.ps1
├── tests/
│   ├── test_smoke.py
│   ├── test_lines2d.py        # pruebas con geometría sintética (planta en L, en T, etc.)
│   └── test_model.py
└── data/                      # ignorado por git (ver data/README.md)
```

## Dependencias de Python

| Paquete | Uso | Licencia |
|---|---|---|
| numpy, scipy | Base numérica, KD-trees | BSD |
| open3d | Normales, voxel, RANSAC de planos, DBSCAN, `detect_planar_patches` | MIT |
| laspy[lazrs] | Leer y escribir LAS/LAZ por bloques | BSD-2 / MIT-Apache |
| pye57 | Leer E57 | MIT |
| shapely ≥ 2.0 | Polígonos, casco cóncavo, rectángulo mínimo rotado | BSD |
| scikit-image, opencv-python-headless | Raster, componentes conexos, líneas (Hough/LSD) | BSD / Apache-2.0 |
| scikit-learn | DBSCAN y RANSAC alternativos | BSD |
| ifcopenshell | Escribir y leer IFC | LGPL-3.0 (se usa como librería) |
| pydantic | Modelo y validación de `building.json` | MIT |
| pyyaml, typer o argparse, tqdm, psutil | Configuración, CLI, progreso, RAM | MIT/BSD |
| matplotlib | PNG de depuración | PSF/BSD |
| pytest | Pruebas | MIT |

No hace falta GPU para el MVP: todo es CPU. La GPU se usará cuando entre la IA.

## Configuración: `config/default.yaml`

Valores iniciales. Si un proyecto necesita otros, se crea `data/raw/<p>/config.yaml` con solo las claves que cambian.

```yaml
io:
  max_points_inspect_sample: 2_000_000
  read_chunk_points: 20_000_000

prep:
  voxel_size: 0.01            # m, nube de trabajo
  outlier_nb_neighbors: 20
  outlier_std_ratio: 2.0
  normal_radius: 0.05         # m
  normal_max_nn: 30
  offset_round: 1000.0        # m, redondeo del offset si las coordenadas son grandes
  large_coord_threshold: 100_000.0  # m; si |x| o |y| supera esto, se aplica offset
  local_cloud_voxel: 0.025    # m, nube que se vincula en Revit

levels:
  horizontal_normal_min_nz: 0.9
  z_hist_bin: 0.02            # m
  min_peak_fraction: 0.02     # fracción mínima de puntos horizontales para considerar un pico
  min_floor_to_floor: 2.0     # m
  max_floor_to_floor: 6.0     # m
  default_slab_thickness: 0.12

slabs:
  concave_hull_ratio: 0.05
  simplify_tolerance: 0.05    # m
  orthogonalize_angle_tol_deg: 5

walls:
  slice_main: [1.0, 1.5]      # m sobre el piso
  slice_check: [[0.5, 0.9], [1.6, 2.0]]
  vertical_normal_max_nz: 0.15
  ransac_distance: 0.015      # m
  min_face_length: 0.40       # m
  min_face_points: 300
  parallel_angle_tol_deg: 3
  thickness_range: [0.06, 0.40]
  thickness_catalog: [0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
  default_one_face_thickness: 0.15
  snap_dominant_tol_deg: 3
  collinear_merge_gap: 0.30   # m
  collinear_offset_tol: 0.03  # m
  join_extend_max: 0.50       # m
  min_vertical_continuity: 0.6

columns:
  size_range: [0.20, 1.20]    # m
  min_height_fraction: 0.7
  embedded_bump_min: 0.03     # m

openings:
  raster_cell: 0.05           # m
  min_width: 0.50
  max_width: 3.50
  min_height: 0.40
  door_max_sill: 0.10         # antepecho ≤ esto ⇒ puerta
  window_min_sill: 0.50
  see_through_min_depth: 0.30 # m de puntos "detrás" del muro para confirmar vano

spaces:
  raster_cell: 0.05
  min_area: 1.0               # m²

confidence:
  review_threshold: 0.75      # por debajo ⇒ status "review"
  weights: {coverage: 0.4, residual: 0.3, consistency: 0.3}

qa:
  tol_tight: 0.02             # m
  tol_loose: 0.05             # m
```

## Convenciones

- **Coordenadas internas:** metros, en el sistema local (nube menos `offset`), con z hacia arriba. Los arreglos de puntos se manejan como `float64` mientras haya `offset` por aplicar y como `float32` en coordenadas locales para ahorrar RAM.
- **IDs estables:** `L1…` para niveles, `S-0001` para losas, `W-0001` para muros, `C-0001` para columnas, `O-0001` para vanos y `R-0001` para espacios, asignados en orden de piso y luego de posición. Revit los guarda en `Marca` para poder rastrear las correcciones.
- **Cada etapa:**
  1. registra en el log su tiempo, la RAM máxima y los conteos;
  2. escribe al menos un PNG en `debug/<etapa>/`;
  3. escribe su JSON en `work/`.
- **PNG legibles:** vista en planta con fondo de puntos grises y elementos en color, escala en metros y título con el piso y la etapa. Tamaño máximo de unos 2000 px para que se puedan mirar.
- **Pruebas:** la geometría se prueba con casos sintéticos generados en el propio test (una caja de 10 × 8 m con un muro interior en T, una puerta y una columna), sin depender de la nube real.
- **Rendimiento:** usar operaciones vectorizadas de numpy y KD-trees de scipy o Open3D. Nada de bucles de Python sobre millones de puntos.
