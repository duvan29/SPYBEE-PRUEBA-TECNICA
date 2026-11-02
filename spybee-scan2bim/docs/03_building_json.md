# 03 · Formato intermedio `building.json`

`building.json` es el **contrato** entre el pipeline de Python y los generadores: el IFC (Python) y Revit (C#). Si cambia, se actualiza este documento y se sube `schema_version`.

## Convenciones

- **Unidades:** metros y grados.
- **Coordenadas:** **locales**, es decir, coordenada real menos `georef.offset`, con z hacia arriba.
- **Geometría en planta:** todas las coordenadas en planta son `[x, y]`. Las alturas se expresan respecto al nivel base del elemento.
- **Polígonos:** lista de vértices `[[x,y], ...]` en sentido antihorario y sin repetir el primero al final.
- **Campos comunes a todo elemento:**
  - `id`: identificador estable;
  - `confidence`: número entre 0 y 1;
  - `status`: `"auto"` o `"review"`;
  - `reasons`: lista de motivos, vacía si es `auto`;
  - `metrics`: indicadores del ajuste.

## Estructura

```jsonc
{
  "schema_version": "0.1",
  "generator": { "name": "scan2bim", "version": "0.1.0", "git": "abc1234",
                 "created": "2026-11-03T10:15:00-05:00", "config_hash": "…" },

  "project": {
    "id": "torre-norte", "name": "Torre Norte",
    "capture_date": "2026-10-28", "scanner": "XGRIDS L2 Pro",
    "building_state": "obra_gris"
  },

  "georef": {
    "crs": "EPSG:9377",            // o "local" si la nube no está georreferenciada
    "offset": { "x": 4880000.0, "y": 2070000.0, "z": 0.0 },   // real = local + offset
    "true_north_deg": 0.0,         // en el MVP es 0, porque la nube no se rota (ver 06)
    "vertical": "orthometric"      // orthometric | ellipsoidal | local
  },

  "dominant_direction_deg": 12.4,  // dirección dominante de los muros (solo informativa y para regularizar)

  "levels": [
    { "id": "L1", "name": "Piso 1", "elevation": 0.000, "confidence": 0.98, "status": "auto", "reasons": [] },
    { "id": "L2", "name": "Piso 2", "elevation": 2.600, "confidence": 0.97, "status": "auto", "reasons": [] }
  ],

  "slabs": [
    {
      "id": "S-0001", "level": "L2",
      "outline": [[0,0],[24.5,0],[24.5,18.2],[0,18.2]],
      "holes": [],                 // vacíos para ductos o escaleras, si se detectan
      "top_offset": 0.0,           // la cara superior queda en elevation(level) + top_offset
      "thickness": 0.12,           // hacia abajo
      "confidence": 0.95, "status": "auto", "reasons": [],
      "metrics": { "rms_m": 0.006, "coverage": 0.88, "thickness_measured": true }
    }
  ],

  "walls": [
    {
      "id": "W-0001", "base_level": "L1", "top_level": "L2",
      "axis": [[12.403, 5.210], [18.950, 5.212]],   // eje (línea central) en planta
      "thickness": 0.15,
      "base_offset": 0.0,          // respecto a elevation(base_level)
      "height": 2.48,              // altura libre, desde la base hasta la cara inferior de la losa de arriba
      "faces_seen": 2,             // 1 o 2
      "material_guess": "masonry", // masonry | concrete | drywall | unknown
      "confidence": 0.93, "status": "auto", "reasons": [],
      "metrics": { "rms_m": 0.006, "coverage": 0.81, "vertical_continuity": 0.92, "thickness_raw": 0.148 }
    }
  ],

  "columns": [
    {
      "id": "C-0001", "base_level": "L1", "top_level": "L2",
      "center": [6.000, 4.000],
      "shape": "rect",             // rect | circle
      "size": [0.30, 0.50],        // rect: [b, h]; circle: [diámetro]
      "rotation_deg": 12.4,        // rotación del lado b respecto al eje x local
      "embedded_in": null,         // id del muro si está embebida
      "confidence": 0.84, "status": "auto", "reasons": [],
      "metrics": { "rms_m": 0.008, "height_fraction": 0.95 }
    }
  ],

  "openings": [
    {
      "id": "O-0001", "host": "W-0001",
      "kind": "door",              // door | window | opening
      "offset_along": 2.10,        // distancia desde axis[0] hasta el borde del vano más cercano a axis[0]
      "width": 0.90, "height": 2.10,
      "sill": 0.00,                // antepecho, respecto a la base del muro
      "confidence": 0.71, "status": "review", "reasons": ["occlusion_partial"],
      "metrics": { "see_through": true, "edge_support": 0.6 }
    }
  ],

  "spaces": [
    {
      "id": "R-0001", "level": "L1",
      "polygon": [[0.15,0.15],[6.2,0.15],[6.2,4.9],[0.15,4.9]],
      "seed": [3.2, 2.5],          // punto interior para crear el Room en Revit
      "area": 28.7,
      "name_guess": null,
      "confidence": 0.9, "status": "auto", "reasons": []
    }
  ],

  "summary": {
    "counts": { "levels": 6, "slabs": 6, "walls": 412, "columns": 38, "openings": 190, "spaces": 96 },
    "review_counts": { "walls": 51, "columns": 6, "openings": 74, "slabs": 1, "spaces": 9 },
    "timings_s": { "prep": 640.2, "levels": 12.1, "walls": 95.4 }
  }
}
```

## Motivos de revisión estándar (`reasons`)

| Código | Significado |
|---|---|
| `one_face` | El muro se vio por una sola cara: el espesor es supuesto |
| `low_coverage` | Menos del ~50 % de la superficie tiene puntos |
| `high_residual` | El ajuste tiene un RMS alto: la superficie es irregular o hay ruido |
| `vertical_discontinuity` | No es continuo en altura: puede ser un mueble o un antepecho |
| `thickness_out_of_catalog` | El espesor medido está lejos de los valores del catálogo |
| `non_orthogonal` | El ángulo está fuera de la dirección dominante: puede estar bien, pero se revisa |
| `occlusion_partial` | Vano o elemento parcialmente ocluido |
| `embedded` | Columna embebida en un muro |
| `thickness_default` | Losa con espesor por defecto, no medido |
| `clutter` | Zona con mucho desorden: material o andamios |

## Validación

- `scan2bim/model.py` define el formato con **pydantic**.
- `export` siempre valida antes de escribir el archivo.
- Reglas mínimas:
  - los ids son únicos;
  - las referencias existen: `level`, `base_level`, `top_level` y `host`;
  - `thickness` es mayor que 0;
  - los polígonos tienen 3 o más vértices y no se autointersectan;
  - `offset_along + width` no supera la longitud del muro.

## Relación con IFC y Revit

| building.json | IFC4 | Revit |
|---|---|---|
| level | IfcBuildingStorey | Level |
| slab | IfcSlab (FLOOR) | Floor |
| wall | IfcWall | Wall (tipo básico con el espesor) |
| column | IfcColumn | Columna estructural (FamilyInstance) |
| opening door/window | IfcOpeningElement + IfcDoor/IfcWindow | v1: Opening en muro; v2: FamilyInstance de puerta o ventana |
| space | IfcSpace | Room |
| id, confidence, status | Pset_SpybeeScan2BIM | Marca / Comentarios (v1), parámetros compartidos (v2) |
