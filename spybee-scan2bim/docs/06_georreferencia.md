# 06 · Georreferencia y sistemas de coordenadas

## Principios

1. **No se rota la nube.** El modelo se construye en el mismo marco que la nube, menos un desplazamiento (offset). La dirección dominante de los muros se usa solo para regularizar.
2. **Se trabaja en coordenadas locales** para no perder precisión: `local = real − offset`.
3. **La georreferencia viaja como metadato**:
   - en `building.json`, en `georef`;
   - en IFC, con `IfcMapConversion` + `IfcProjectedCRS`;
   - en Revit, con las coordenadas compartidas.

## Casos posibles de la nube

| Caso | Cómo detectarlo | Qué hacer |
|---|---|---|
| **A. CTM12 / EPSG:9377** (Origen Nacional, oficial en Colombia) | Valores de x alrededor de 4–5 millones de metros y de y alrededor de 1–3 millones (falso este 5.000.000, falso norte 2.000.000) | `offset` redondo en x e y; `crs = "EPSG:9377"` |
| **B. MAGNA-SIRGAS por origen** (Bogotá, Oeste, etc.) o CTM12 sin confirmar | Coordenadas del orden de cientos de miles o de millones, sin metadatos | Preguntar al usuario o al scan leader. Usar `offset` igual. `crs` queda como el que digan, o `"unknown_projected"` |
| **C. Local** (origen en el primer escaneo) | Coordenadas pequeñas, en decenas o cientos de metros | Sin `offset` (0,0,0) y `crs = "local"`. El modelo no queda georreferenciado y eso se anota en las preguntas abiertas |
| **D. Geográficas** (lat/lon en grados) | Valores x/y entre −180 y 180 con z en metros | Raro en una nube. Detenerse y pedir una exportación en un sistema proyectado |

Las **cotas** pueden ser:
- **ortométricas**: sobre el nivel del mar, por ejemplo unos 2.600 m en Bogotá;
- **elipsoidales**, si salen directas de un GNSS;
- **locales**: 0 en el primer piso.

El pipeline **no convierte entre ellas**: solo registra cuál es (`georef.vertical`). Si la z es grande, por ejemplo más de 1.000 m, también se le aplica un offset redondo en z.

## Cálculo del offset (`prep`)

```python
if max(abs(xmin), abs(xmax), abs(ymin), abs(ymax)) > cfg.prep.large_coord_threshold:
    ox = math.floor(xmin / cfg.prep.offset_round) * cfg.prep.offset_round
    oy = math.floor(ymin / cfg.prep.offset_round) * cfg.prep.offset_round
else:
    ox = oy = 0.0
oz = math.floor(zmin / 100.0) * 100.0 if abs(zmin) > 1000 else 0.0
# guardar en data/work/<p>/georef.json: {"crs": ..., "offset": {"x": ox, "y": oy, "z": oz}, "vertical": ...}
```

La resta se hace **en float64** y solo después se convierte a float32.

## IFC (IfcOpenShell)

- Agregar el contexto de georreferencia con el módulo `georeference` de la API de IfcOpenShell. Los nombres exactos de las funciones varían entre versiones 0.7 y 0.8: **revisar con `help(ifcopenshell.api.georeference)` en la versión instalada.** La idea:
  - `IfcProjectedCRS.Name = "EPSG:9377"`;
  - `IfcMapConversion`:
    - `Eastings = offset.x`, `Northings = offset.y`, `OrthogonalHeight = offset.z`;
    - `XAxisAbscissa = 1.0`, `XAxisOrdinate = 0.0`, porque no hay rotación;
    - `Scale = 1.0`.
- Las coordenadas de los elementos en el IFC son las **locales**.
- Verificar reabriendo el IFC: para un muro, el punto local más el offset debe dar la coordenada real.

## Revit

1. **Geometría cerca del origen interno.** El add-in crea todo en coordenadas locales: el origen interno de Revit es el `offset`. Revit pierde precisión con geometría a más de unos 32 km del origen interno, y por eso nunca se modela en coordenadas CTM12 directas.
2. **Coordenadas compartidas.**
   - `ProjectLocation.SetProjectPosition(XYZ.Zero, new ProjectPosition(E, N, Z, ángulo))`, con E, N y Z iguales al offset y ángulo 0.
   - Así, cualquier punto consultado con *Coordenada de punto* en coordenadas compartidas muestra su valor real CTM12.
   - Ver `05_revit_addin.md` §10.
3. **Nube en Revit.**
   - Se vincula `data/out/<p>/cloud_local.las`, que ya tiene el offset restado, con posicionamiento **Automático – Origen a origen**. Así queda exactamente sobre el modelo.
   - **No** vincular la nube original con coordenadas CTM12 de origen a origen: quedaría a miles de km del modelo.
   - Si Revit no inserta LAS o E57 directamente, convertir `cloud_local.las` a RCP con ReCap, sin mover el origen.
4. **Verificación.**
   - Si hay `control_points.csv`, el reporte QA lista para cada punto su coordenada local y su distancia al punto más cercano de la nube.
   - En Revit, el usuario marca uno de esos puntos y consulta la coordenada compartida.
   - El error debe ser de unos pocos cm.

## Puntos de control (opcional)

Formato `data/raw/<p>/control_points.csv`:

```csv
id,este,norte,cota,metodo,precision_m
PC1,4880123.456,2070456.789,2601.234,estacion_total,0.005
PC2,4880187.012,2070470.321,2601.240,gnss_rtk,0.02
```

QA:
- Para cada punto, calcular `local = real − offset` y la distancia al punto más cercano de la nube.
- Si alguna distancia es mayor que `qa.tol_loose`, advertirlo: puede ser un error de registro o de coordenadas.
