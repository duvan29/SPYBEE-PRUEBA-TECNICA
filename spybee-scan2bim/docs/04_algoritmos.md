# 04 · Algoritmos de detección

Todo es **geométrico** en el MVP. Los parámetros están en `config/default.yaml` (ver `02_arquitectura.md`). Para cada etapa: primero una versión simple que funcione sobre la nube real, después los refinamientos.

Referencia de código abierto (MIT) que vale la pena leer antes de los §2–§6: **Cloud2BIM**, https://github.com/VaclavNezerka/Cloud2BIM. Hace losas por histograma, muros, vanos y salida IFC. Si se reutiliza código, conservar el aviso de licencia.

---

## §0 Lectura y preparación (`inspect`, `prep`)

### Lectura

**E57 con pye57:**
- `e57 = pye57.E57(path)`.
- Recorrer `range(e57.scan_count)` y leer cada escaneo con `read_scan(i, ignore_missing_fields=True, colors=True, intensity=True, transform=True)`. `transform=True` aplica la pose de cada escaneo.
- Para la ficha, usar `get_header(i).point_count` sin leer los puntos.
- **Si hay un solo escaneo gigante** (típico de SLAM) que no cabe en la RAM con margen, por ejemplo más de un tercio de la RAM libre:
  1. no leerlo con pye57;
  2. convertirlo antes a LAZ diezmado con CloudCompare por línea de comandos (ver `08_entorno.md`);
  3. leer ese LAZ.

**LAS/LAZ con laspy:**
- `with laspy.open(path) as f: for chunk in f.chunk_iterator(cfg.io.read_chunk_points): ...`
- Las coordenadas escaladas salen de `chunk.x`, `chunk.y`, `chunk.z`, en float64.

### Coordenadas grandes

- Si `max(|x|, |y|) > large_coord_threshold`, calcular `offset = round(min_xyz / offset_round) * offset_round` sobre x e y; z se deja en 0 salvo que sea muy grande.
- Restarlo **en float64**, antes de convertir a float32.
- Guardarlo en `work/<p>/georef.json`. Ver `06_georreferencia.md`.

### Submuestreo por bloques

Para cada bloque:
1. Calcular la clave de voxel `floor(xyz_local / voxel)`.
2. Quedarse con un punto por voxel: el primero, o el promedio si alcanza.
3. Acumular.

Al final, deduplicar de nuevo con todas las claves juntas, con `np.unique` sobre las claves empaquetadas en int64.

### Limpieza y normales

- Open3D: `remove_statistical_outlier(nb_neighbors, std_ratio)`.
- `estimate_normals(KDTreeSearchParamHybrid(radius=normal_radius, max_nn=normal_max_nn))`.
- Las normales no tienen signo. Para clasificar horizontales y verticales solo importa `|nz|`.

### Ficha (`ficha.md`)

Debe incluir:
- archivos;
- escaneos y puntos;
- campos disponibles;
- caja envolvente en coordenadas reales y locales;
- dimensiones del edificio;
- densidad: puntos por m² en una muestra de superficies;
- magnitud de las coordenadas y el CRS probable;
- número de pisos estimado a partir del histograma de z, como vista preliminar;
- tiempos de lectura;
- advertencias.

---

## §1 Chequeos geométricos (T2.1)

**Nivelación:**
- Tomar los puntos con `|nz| > 0.95` y calcular la normal media del plano dominante (RANSAC sobre el piso más grande).
- Si el ángulo respecto a z es mayor a 0,5°, avisar al usuario. **No corregir automáticamente en el MVP.**

**Dirección dominante:**
- Tomar los puntos con `|nz| < vertical_normal_max_nz`, que son superficies verticales.
- Calcular el azimut `θ = atan2(ny, nx)` y reducirlo a módulo 90°, en el rango [0, 90).
- Hacer un histograma de 0,5° con suavizado circular. El pico es `dominant_direction_deg`.
- Si hay un segundo pico fuerte que no está a 0° ni a 90° del primero, registrarlo: el edificio tiene alas giradas, y se regulariza por zona más adelante.

---

## §2 Niveles (T2.2–T2.3)

1. Tomar los puntos horizontales, con `|nz| > horizontal_normal_min_nz`, y hacer un histograma de z con `z_hist_bin = 2 cm`.
2. Buscar los picos (`scipy.signal.find_peaks`) con una altura mínima igual a `min_peak_fraction` del total de puntos horizontales.
3. **Clasificar cada pico como piso o cielo raso.**
   - Para cada pico, mirar si los puntos de esa superficie tienen puntos **arriba** (espacio libre de ~2 m o más) o **abajo**.
   - Una heurística simple: en una grilla en planta de 0,5 m, para las celdas del pico, ver si hay más ocupación en la franja z+0,3…z+1,8 o en la franja z−1,8…z−0,3.
   - Si arriba hay muros y espacio libre, es un **piso**; si lo hay abajo, es un **cielo raso o la cara inferior de una losa**.
4. **Asignar los niveles.**
   - Cada pico de piso es un nivel.
   - Si dos picos de piso están a menos de `min_floor_to_floor`, fusionarlos. Si la diferencia es de pocos cm, se toma el que tenga más puntos. Ojo: podría ser un desnivel real; anotarlo en `reasons`.
   - Nombres: `Piso 1…n`, desde el más bajo. Si hay pisos bajo el nivel de la calle, el usuario lo indica y se renombran a `Sótano`.
5. **Losa entre pisos:**
   - cara superior = cota del piso N+1;
   - cara inferior = el pico de cielo raso más alto por debajo de ese piso y por encima del piso N.
   - El espesor medido es la diferencia. Si no está entre 0,08 y 0,6 m, usar `default_slab_thickness` y agregar el motivo `thickness_default`.
6. **División por pisos:** el piso N contiene los puntos con `z` en `[cota_N − 0,05, cara_inferior_losa_N+1 + 0,05]`. El último piso llega hasta la cubierta.

---

## §3 Losas (T2.4)

- **Puntos de cada losa:** los horizontales del pico del piso, en ±3 cm.
- **Contorno:**
  1. Calcular un casco cóncavo en 2D con `shapely.concave_hull(MultiPoint, ratio=concave_hull_ratio)`.
  2. Si es lento, primero hacer un raster de 5 cm, cerrar con morfología (closing) y tomar el contorno del componente más grande, con `skimage.measure.find_contours` o `cv2.findContours`.
  3. Simplificar con `simplify(simplify_tolerance)`.
- **Ortogonalización:** girar cada arista que esté dentro de ±`orthogonalize_angle_tol_deg` de la dirección dominante o de su perpendicular, y recalcular los vértices como intersecciones de aristas consecutivas.
- **Huecos:** buscar huecos internos de más de 1 m², como vacíos de escaleras o ductos, en el raster.
- **Cubierta:** la losa del último nivel cuenta igual si fue escaneada.
- **Confianza:**
  - cobertura = área con puntos / área del polígono;
  - rms = residuo del plano;
  - se penaliza si el espesor no se midió.

---

## §4 Muros (T4.1–T4.6)

### 4.1 Cortes

- Franja principal: `slice_main = [1.0, 1.5]` m sobre la cota del piso.
- Franjas de validación: `slice_check`.
- Solo los puntos con `|nz| < vertical_normal_max_nz`. Esto quita pisos, mesones y la mayor parte del ruido.

### 4.2 Detección de caras: elegir la opción A y pasar a la B si falla

**Opción A, en 3D (recomendada):**
1. Sobre los puntos verticales del piso, correr RANSAC iterativo de planos (`segment_plane(distance_threshold=ransac_distance, ransac_n=3, num_iterations=1000)`).
2. Aceptar el plano solo si su normal es casi horizontal.
3. Separar los puntos del plano en tramos con DBSCAN en 1D, a lo largo de la dirección del plano, con eps = 0,15 m.
4. Cada tramo de largo ≥ `min_face_length` con ≥ `min_face_points` puntos es una **cara**: segmento 2D (extremos = percentiles 1 y 99 de la proyección), normal, z mínima y máxima, y número de puntos.
5. Quitar esos puntos y repetir hasta que no queden planos grandes.

Alternativa rápida en Open3D: `detect_planar_patches(...)`, que devuelve parches planos como cajas orientadas. Probar si va más rápido en nubes grandes.

**Opción B, en 2D:**
1. Hacer un raster del corte con celda de 2 cm, ocupado o libre, y aplicar un closing de 1 celda.
2. Extraer segmentos con `cv2.ximgproc` o LSD (`cv2.createLineSegmentDetector`), o con Hough probabilístico (`skimage.transform.probabilistic_hough_line`).
3. Volver a ajustar cada segmento a los puntos cercanos con mínimos cuadrados.

### 4.3 Emparejar caras: eje y espesor

- **Candidatos a par:** dos caras con
  - ángulo entre direcciones ≤ `parallel_angle_tol_deg`;
  - normales opuestas (mirando una hacia la otra: el vector entre sus centros proyectado sobre la normal tiene signos opuestos);
  - distancia perpendicular dentro de `thickness_range`;
  - solape a lo largo de su dirección ≥ 50 % de la más corta.
- **Asignación:** greedy por mejor puntaje, combinando solape alto y distancia cercana a un valor del catálogo. Una cara puede emparejarse por tramos si su compañera está partida, por ejemplo por un vano. En ese caso se parte la cara.
- **Eje:** línea media entre las dos caras, extendida a la unión de sus proyecciones.
- **Espesor:** distancia perpendicular media.
- **Caras sin par:**
  - si tienen el otro lado libre (espacio vacío de 0,5 m o más), son muros de fachada vistos de un solo lado, o muros cuya otra cara no se escaneó;
  - eje = cara desplazada `default_one_face_thickness / 2` hacia el lado sin datos;
  - motivos `one_face`, status `review`.
- **Caras sin par que son ruido:** por ejemplo, el frente de un mueble o un andamio. Se descartan si su continuidad vertical es baja (ver 4.5).

### 4.4 Regularización

1. **Snap de ángulo:** si el ángulo del eje está a ≤ `snap_dominant_tol_deg` de la dirección dominante o de su perpendicular, rotarlo sobre su punto medio hasta coincidir.
2. **Fusión de colineales:** fusionar dos ejes paralelos con un desfase perpendicular ≤ `collinear_offset_tol`, un hueco entre ellos ≤ `collinear_merge_gap` y espesor igual. **Excepción:** no fusionar si el hueco coincide con un vano confirmado; en ese caso el hueco es la puerta.
3. **Uniones:**
   - Para cada extremo libre, buscar la intersección con otro eje a ≤ `join_extend_max`, extendiendo o recortando.
   - **L:** ambos extremos llegan a la intersección.
   - **T:** el extremo llega a la **cara** del muro pasante, no a su eje. Revit también resuelve las uniones si los extremos están cerca.
4. **Espesor al catálogo:** redondear al valor más cercano de `thickness_catalog`. Si la diferencia es mayor a 2 cm, agregar el motivo `thickness_out_of_catalog`, pero redondear igual.
5. **Duplicados:** eliminar los ejes casi idénticos.

### 4.5 Alturas y verificación vertical

- **Altura:** desde la cota del nivel hasta la cara inferior de la losa del piso de arriba (o hasta la cubierta). Ese valor va en `height`, con `top_level` igual al siguiente nivel.
- **Continuidad vertical:** fracción de las franjas de `slice_check` en las que el muro también aparece. Se busca en cada franja si hay puntos a menos de `t/2 + 2 cm` del eje en al menos el 50 % de su largo.
  - Si es menor a `min_vertical_continuity`, agregar el motivo `vertical_discontinuity` y bajar la confianza.
  - Si además la cara no tenía par y la altura de sus puntos llega a menos de 1,6 m, descartarla como mueble o antepecho.

### 4.6 PNG obligatorios

- `F0X_slice.png`: el corte.
- `F0X_faces.png`: las caras de colores.
- `F0X_walls.png`: los ejes, con el espesor anotado y los `review` en rojo.
- `F0X_before_after.png`: la regularización.

---

## §5 Columnas (T6.1)

**Exentas:**
1. Del corte principal, quitar los puntos a menos de `t/2 + 3 cm` de algún muro.
2. Agrupar el resto con DBSCAN en 2D, con eps = 5 cm.
3. Para cada cluster, tomar el rectángulo mínimo rotado (`shapely.minimum_rotated_rectangle`) y medir:
   - el tamaño de cada lado, dentro de `size_range`;
   - la relación de aspecto ≤ 4.
4. Si el cluster es un arco o círculo, ajustar un círculo por mínimos cuadrados. Si el residuo es bajo, la columna es circular.
5. Verificar que exista en las franjas de validación: `height_fraction ≥ min_height_fraction`.
6. Los clusters de 4 caras vistas son de alta confianza. Si se ven 2 o 3 caras, se completa el rectángulo con baja confianza.

**Embebidas (opcional en el MVP):**
- A lo largo de cada muro, medir el desfase local de cada cara cada 5 cm.
- Un tramo de 20–100 cm con un abultamiento ≥ `embedded_bump_min` en una o ambas caras es una columna candidata, con `embedded_in = muro`, status `review` y motivo `embedded`.
- Si hay color, una diferencia clara de color entre el tramo y el muro (concreto gris frente a ladrillo) sube la confianza.

---

## §6 Vanos (T6.2)

Para cada muro:
1. Tomar los puntos a ≤ `t/2 + 3 cm` del eje (los del muro, en todas sus alturas) dentro del tramo del muro.
2. Proyectarlos a coordenadas (u, z): u es la distancia a lo largo del eje desde `axis[0]`, y z es la altura desde la base.
3. Hacer un raster de `raster_cell = 5 cm` con las celdas ocupadas en 1.
4. Las celdas vacías conectadas forman huecos candidatos. Descartar las que tocan los bordes superior o laterales del muro, salvo las puertas que tocan el piso.
5. Tomar el rectángulo envolvente alineado de cada hueco y filtrar por `min_width`, `max_width` y `min_height`.
6. **Confirmar que el hueco es real y no una sombra del escaneo:**
   - en la región del hueco, buscar puntos **más allá del muro**, a ≥ `see_through_min_depth` del plano, a cualquiera de los dos lados;
   - si se ve a través, es un vano real (`see_through = true`);
   - si no, puede ser una sombra producida por un objeto delante: status `review`, motivo `occlusion_partial`.
7. **Clasificar:**
   - `sill ≤ door_max_sill` → `door`;
   - `sill ≥ window_min_sill` → `window`;
   - otro valor → `opening`.
8. **Puertas:** si el hueco llega al piso y tiene un dintel de concreto o mampostería encima, la altura es la del dintel.

PNG: `debug/openings/W-xxxx.png` con la elevación del muro (raster y rectángulos) para una muestra de muros, y una planta por piso con los vanos marcados sobre los ejes.

---

## §7 Espacios (T6.3)

1. Hacer un raster por piso con `raster_cell = 5 cm` y dibujar los muros con su espesor, como rectángulos rellenos, y las columnas.
2. Cerrar los vanos de puertas con una línea, para que cada recinto quede separado.
3. Rellenar el espacio libre (flood fill) y etiquetar los componentes conexos que estén **dentro** del contorno de la losa.
4. Descartar los componentes de menos de `min_area` y el componente exterior.
5. Obtener el polígono de cada componente con `find_contours` y simplificarlo. El `seed` es un punto interior: usar `polygon.representative_point()`.
6. El área es la del polígono. En Revit, el Room calcula su propia área a partir de los muros.

---

## §8 Confianza (T7.1)

Para cada elemento:

```
coverage     = fracción de la superficie del elemento con puntos a ≤ 3 cm (en celdas de 10 cm)
residual     = 1 − min(rms / 0.02, 1)          # rms en metros
consistency  = continuidad vertical (muros), height_fraction (columnas), see_through (vanos: 1 o 0,4), etc.
confidence   = w_cov·coverage + w_res·residual + w_con·consistency
```

- Los pesos van en `confidence.weights`.
- Cada motivo de la lista estándar (`03_building_json.md`) resta 0,1 adicional, con un mínimo de 0.
- Si `confidence < review_threshold` o hay un motivo "fuerte" (`one_face`, `occlusion_partial`, `embedded`, `thickness_default`), el status es `review`.

**Calibración:**
- Cuando haya referencia, graficar la confianza frente a si el elemento resultó correcto o no.
- Ajustar el umbral para que los `auto` tengan ≥ 95 % de precisión.
- Registrar la decisión en `PROGRESO.md`.

---

## §9 Errores típicos y cómo detectarlos

| Síntoma en los PNG | Causa probable | Qué probar |
|---|---|---|
| Muros dobles paralelos a 1–3 cm | Ruido, o dos caras del mismo lado (pañete) | Subir `collinear_offset_tol` y verificar el emparejamiento |
| Muchos segmentos cortos | Desorden de obra, andamios | Subir `min_face_length` y `min_face_points`; exigir continuidad vertical |
| Muros que no cierran en esquinas | `join_extend_max` muy bajo | Subirlo a 0,8 m; revisar el snap de ángulo |
| Espesores absurdos (> 40 cm) | Se emparejaron caras de muros distintos | Bajar el máximo de `thickness_range`; exigir solape |
| Niveles de más | Mesones, losas de escalera, material apilado | Subir `min_peak_fraction`; exigir área mínima del pico |
| Vanos falsos en zonas sin datos | Sombras de escaneo | Exigir `see_through` |
| Todo rotado unos grados respecto a Revit | Se rotó la nube o hubo confusión con el norte real | **No rotar la nube.** Revisar `06_georreferencia.md` |
