# 01 · Plan de ejecución del MVP

**Cómo usar este plan (Claude):**
- Toma la primera casilla sin marcar.
- Lee los documentos que indica la tarea.
- Implementa y verifica contra el criterio de aceptación, **mirando los PNG**.
- Marca `- [x]`, registra en `PROGRESO.md` y haz commit.
- En cada 🎯 HITO, detente y muestra los resultados al usuario.

**Principio:** primero de punta a punta y feo, después bonito. Cada bloque deja algo visible.

---

## Bloque 0 · Preparación (lo hace el equipo, antes de abrir Claude Code)

- [ ] **T0.1** Copiar esta carpeta al PC en una ruta corta, por ejemplo `C:\spybee\scan2bim`.
- [ ] **T0.2** Copiar la nube a `data/raw/<proyecto>/`. Si está en RCP, FLS o LGS, exportar también a E57 (ver `08_entorno.md`).
- [ ] **T0.3** Si existe, copiar el modelo manual a `data/reference/<proyecto>/` y exportarlo a IFC.
- [ ] **T0.4** Instalar Claude Code y Git. Abrir una terminal en la carpeta y ejecutar `claude`, luego `/arrancar`.

---

## Bloque 1 · Entorno y ficha de la nube (día 1)

- [ ] **T1.1 Diagnóstico del PC.**
  - Revisar el sistema operativo, la CPU, la RAM total y libre, la GPU (`nvidia-smi` si existe), el disco libre, las versiones de Revit instaladas (`C:\Program Files\Autodesk\Revit 20XX`) y si hay Git, conda, Python y dotnet.
  - Registrar todo en `PROGRESO.md`.
  - *Acepta:* la tabla "Datos del proyecto" de `PROGRESO.md` tiene la fila del PC completa.

- [ ] **T1.2 Entorno de Python** (ver `08_entorno.md`).
  - Crear el entorno conda `scan2bim` con Python 3.11 e instalar las dependencias.
  - `git init` en la carpeta si no existe un repositorio.
  - *Acepta:* `python -c "import open3d, laspy, pye57, ifcopenshell, shapely; print('ok')"` imprime `ok`.

- [ ] **T1.3 Esqueleto del paquete** (ver `02_arquitectura.md`).
  - Crear `scan2bim/` con su CLI (`python -m scan2bim <comando> --project <p>`), el lector de configuración `config/default.yaml`, el logging y las utilidades de rutas.
  - Crear `tests/` con una prueba de humo.
  - *Acepta:* `python -m scan2bim --help` lista los comandos y `pytest -q` pasa.

- [ ] **T1.4 `inspect`: ficha de la nube.**
  - Leer la cabecera y los metadatos sin cargar todo: número de escaneos y de puntos, campos disponibles (RGB, intensidad), caja envolvente y magnitud de las coordenadas (para saber si es CTM12 o local).
  - Muestrear unos 2 millones de puntos y generar:
    - `debug/inspect/top.png`: vista superior coloreada por altura;
    - `debug/inspect/side.png`: vista lateral;
    - `debug/inspect/z_hist.png`: histograma de alturas.
  - Calcular la densidad estimada.
  - Escribir `data/out/<p>/ficha.md`.
  - *Acepta:* la ficha existe y los PNG muestran el edificio reconocible. Revisarlos con la herramienta de imágenes.

- [ ] **T1.5 `prep`: nube de trabajo.**
  - Leer por escaneo o por bloques y submuestrear con voxel de 1 cm.
  - Eliminar puntos aislados (outliers estadísticos) y estimar normales.
  - Guardar `data/work/<p>/cloud_1cm.laz` y `normals.npz`.
  - Si las coordenadas son grandes, calcular el `offset` y guardarlo en `data/work/<p>/georef.json`. Ver `06_georreferencia.md`.
  - *Acepta:* la nube de trabajo tiene menos de ~150 M puntos y se abre en CloudCompare, si está instalado. El tiempo y la RAM máxima quedan registrados.

🎯 **HITO 1:** mostrar la ficha y los PNG. Preguntar si coinciden con lo que el equipo sabe del edificio: pisos, dimensiones aproximadas y georreferencia.

---

## Bloque 2 · Niveles y losas (día 2)

- [ ] **T2.1 Chequeos geométricos** (`04_algoritmos.md` §1).
  - Verificar que la nube esté nivelada: el ángulo de las normales de piso respecto a z debe ser menor a 0,5°. Si no lo está, avisar.
  - Calcular la **dirección dominante** de los muros a partir del histograma de azimut de las normales horizontales, en módulo 90°.
  - *Acepta:* PNG `debug/levels/azimuth_hist.png` con un pico claro. El ángulo queda en el log.

- [ ] **T2.2 `levels`: detección de niveles** (§2).
  - Hacer el histograma de z de los puntos con normal vertical.
  - Detectar los picos, clasificarlos en piso o cielo raso y calcular la cota de cada nivel.
  - *Acepta:* PNG `debug/levels/z_peaks.png`. El número de niveles y la altura de piso a piso coinciden con lo que dio el usuario, con una tolerancia de ±3 cm en la altura.

- [ ] **T2.3 División por pisos.**
  - Guardar `data/work/<p>/floors/F01.laz`, `F02.laz`, etc., cada uno con todos los puntos entre la cara superior de su losa y la cara inferior de la losa del piso de arriba.
  - *Acepta:* un PNG de planta por piso (`debug/levels/F01_top.png`, …) y ningún piso vacío.

- [ ] **T2.4 `slabs`: losas** (§3).
  - Calcular el contorno de cada losa con un casco cóncavo de los puntos de piso, simplificarlo y ortogonalizarlo.
  - Calcular el espesor a partir de la cara inferior medida desde el piso de abajo. Si no se puede medir, usar el valor por defecto de la configuración y bajar la confianza.
  - *Acepta:* PNG con el contorno de cada losa sobre su nube. El área es coherente con la que dio el usuario, si la sabe.

- [ ] **T2.5 `building.json` v0** (ver `03_building_json.md`).
  - Escribir los niveles y las losas con su confianza.
  - Agregar un validador del formato con pydantic o jsonschema y una prueba.
  - *Acepta:* el JSON valida y `pytest -q` pasa.

---

## Bloque 3 · Primer IFC visible (día 3)

- [ ] **T3.1 `export`: IFC4 con IfcOpenShell** (`03`, `06`).
  - Crear el proyecto, el sitio, el edificio y un `IfcBuildingStorey` por nivel, y las `IfcSlab` con su geometría.
  - Usar unidades en metros. Si hay georreferencia, agregar `IfcMapConversion` y `IfcProjectedCRS`.
  - Agregar el set de propiedades `Pset_SpybeeScan2BIM` con `Confidence`, `Status` y `SpybeeId`.
  - *Acepta:* `model.ifc` abre sin errores. Validarlo reabriéndolo con ifcopenshell y contando las entidades.

- [ ] **T3.2 Nube local para Revit.**
  - Exportar `data/out/<p>/cloud_local.las` diezmada a 2–3 cm, en **coordenadas locales**, es decir, con el `offset` restado.
  - *Acepta:* el archivo existe y su caja envolvente coincide con la del `building.json`.

- [ ] **T3.3 Verificación visual en Revit**, con ayuda del usuario.
  - Dar instrucciones paso a paso:
    1. Proyecto nuevo.
    2. Insertar → Vincular IFC (`model.ifc`).
    3. Insertar → Nube de puntos (`cloud_local.las`, posicionamiento "Automático – Origen a origen"). Si Revit no acepta LAS o E57 directamente, convertir antes a RCP con ReCap.
  - Pedir una captura de pantalla.
  - *Acepta:* las losas quedan alineadas con la nube, con un error de pocos cm.

🎯 **HITO 2 — primera demo:** losas y niveles alineados con la nube, dentro de Revit.

---

## Bloque 4 · Muros (días 4–6)

Este bloque es el corazón del MVP. Ver `04_algoritmos.md` §4.

- [ ] **T4.1 Cortes por piso.**
  - Para cada piso, tomar una franja de z entre `piso + 1,0` y `piso + 1,5` m, más dos franjas extra (0,5–0,9 y 1,6–2,0 m) para validar.
  - Proyectarlas en 2D.
  - *Acepta:* PNG `debug/walls/F01_slice.png` donde se ven claramente las líneas de los muros.

- [ ] **T4.2 Detección de caras.**
  - Extraer los segmentos de cara de muro: planos verticales con RANSAC más DBSCAN, o líneas 2D. Ver las opciones en §4.
  - *Acepta:* PNG con los segmentos sobre el corte. Casi todas las caras visibles quedan detectadas y hay pocos falsos positivos (muebles, andamios).

- [ ] **T4.3 Emparejar caras: eje y espesor.**
  - Formar pares de caras paralelas y opuestas, a una distancia dentro del rango de espesores.
  - Los muros vistos por una sola cara reciben el espesor por defecto, baja confianza y estado `review`.
  - *Acepta:* PNG con los ejes y los espesores anotados. Los espesores caen en valores razonables (8–30 cm).

- [ ] **T4.4 Regularización.**
  - Llevar los ángulos a la dirección dominante (±3°) y fusionar segmentos colineales.
  - Extender o recortar hasta las intersecciones (uniones en L y en T).
  - Redondear los espesores al catálogo.
  - *Acepta:* PNG "antes y después". Las esquinas quedan cerradas y no hay muros duplicados.

- [ ] **T4.5 Alturas y verificación vertical.**
  - Altura del muro: desde su nivel hasta la cara inferior de la losa del piso de arriba.
  - Verificar con las franjas extra que el muro es continuo en altura. Si no lo es, puede ser un antepecho o un mueble: bajar la confianza.
  - *Acepta:* el log muestra cuántos muros pasaron y cuántos quedaron en `review`.

- [ ] **T4.6 Muros en `building.json` e IFC.**
  - *Acepta:* el IFC muestra los muros en Revit alineados con la nube, y el usuario lo confirma.
  - Si hay referencia, correr una evaluación preliminar de muros (ver `07_evaluacion.md`) y registrarla en las métricas.

🎯 **HITO 3:** PNG de cada piso con los muros detectados sobre la nube, más el IFC en Revit. Revisarlo con el usuario: ¿qué falta, qué sobra?

---

## Bloque 5 · Revit nativo (días 7–8)

Ver `05_revit_addin.md`.

- [ ] **T5.1 Proyecto C# que compila.**
  - Detectar la versión de Revit: 2025 o 2026 usan `net8.0-windows`; 2024 o anteriores, `net48`.
  - Crear `revit/Spybee.Scan2BIM.Revit/`, el `.addin` y un script `revit/install.ps1` que compila y copia a `%AppData%\Autodesk\Revit\Addins\<año>\`.
  - Agregar un comando "Spybee: Hola" que muestre un `TaskDialog`.
  - *Acepta:* el usuario abre Revit y ve el comando en **Complementos → Herramientas externas**, y el comando funciona.

- [ ] **T5.2 Comando "Spybee: Generar modelo" (v1).**
  - Leer `building.json` con un diálogo para elegir el archivo.
  - Crear los niveles, los tipos de muro por espesor (`Spybee Generico 15 cm`), los muros con restricción superior al nivel de arriba y los tipos de losa por espesor con sus losas.
  - Usar una sola transacción y mostrar un resumen al final.
  - *Acepta:* el RVT tiene muros y losas **nativos**, editables con los grips de Revit.

- [ ] **T5.3 Marcado para revisión.**
  - Escribir en cada elemento `Marca = SpybeeId` y `Comentarios = "AUTO conf=0.93"` o `"REVISAR conf=0.62 motivo=una_cara"`.
  - Crear una planta por nivel y una vista 3D `00_REVISAR` con un override rojo sobre los elementos a revisar.
  - *Acepta:* en `00_REVISAR` se ven en rojo exactamente los elementos con `status = review`.

- [ ] **T5.4 Coordenadas y nube.**
  - Si hay georreferencia, fijar las coordenadas compartidas: punto de reconocimiento igual al `offset` y ángulo al norte real. Ver `06_georreferencia.md`.
  - Dar instrucciones para vincular `cloud_local.las` o su RCP de origen a origen. La automatización se deja como opcional.
  - *Acepta:* la nube queda alineada con los muros nativos. Si hay puntos de control, uno de ellos consultado en Revit coincide en coordenadas reales con un error de pocos cm.

🎯 **HITO 4 — segunda demo:** el modelador abre el RVT nativo con la nube y lo recorre.

---

## Bloque 6 · Columnas, vanos y espacios (días 9–11)

Ver `04_algoritmos.md` §5–7.

- [ ] **T6.1 `columns`.**
  - Detectar columnas exentas: clusters pequeños en el corte, ajustados a un rectángulo o un círculo y verificados en altura.
  - Detectar columnas embebidas: abultamientos locales de la cara del muro, en estado `review`.
  - *Acepta:* PNG con las columnas sobre el corte. Las dimensiones caen en 0,2–1,2 m.

- [ ] **T6.2 `openings`.**
  - Para cada muro, proyectar sus puntos sobre el plano en coordenadas (u, z), hacer un raster de 5 cm y buscar huecos rectangulares.
  - Confirmar cada hueco viendo que a través de él se ven puntos más lejanos, para descartar sombras de escaneo.
  - Clasificar en puerta o ventana según el antepecho.
  - *Acepta:* PNG de elevación de varios muros con los vanos marcados. Si hay referencia, recall de vanos ≥ 60 % en esta primera versión.

- [ ] **T6.3 `spaces`.**
  - Hacer un raster por piso con los muros dibujados, rellenar el espacio libre (flood fill) y obtener polígonos.
  - Calcular para cada espacio un punto semilla y su área.
  - *Acepta:* PNG con los espacios coloreados y sus áreas.

- [ ] **T6.4 Revit: columnas, vanos y recintos.**
  - Columnas: familias de la plantilla, con tipos duplicados por sección.
  - Vanos: en v1, `NewOpening` en el muro; en v2, puertas y ventanas genéricas.
  - Recintos: `NewRoom` en cada punto semilla.
  - Todo con su marcado AUTO o REVISAR.
  - *Acepta:* el RVT tiene columnas, vanos y recintos con áreas.

🎯 **HITO 5:** modelo LOD 200 completo de arquitectura y estructura del edificio de prueba.

---

## Bloque 7 · Confianza, calidad y un solo comando (días 12–13)

- [ ] **T7.1 Confianza por elemento** (`04_algoritmos.md` §8).
  - Combinar en un solo número la cobertura, el residuo RMS, la coherencia entre franjas y los motivos.
  - El umbral para pasar a `review` va en la configuración.
  - *Acepta:* histograma de confianza por clase en `debug/qa/`.

- [ ] **T7.2 `qa`: reporte HTML.**
  - Por elemento: desviación nube–modelo (RMS, % de puntos a 2 cm o menos y a 5 cm o menos) y cobertura.
  - Mapa de calor por piso.
  - Resumen: conteos por clase y por estado.
  - Si hay puntos de control, su error.
  - *Acepta:* `qa.html` se abre en el navegador y es legible.

- [ ] **T7.3 `eval` contra la referencia** (`07_evaluacion.md`).
  - Calcular precisión y exhaustividad por clase, el error de eje y de espesor de los muros, y el error de cota de los niveles.
  - *Acepta:* existe `eval.json` y la fila de métricas en `PROGRESO.md` está actualizada.

- [ ] **T7.4 Comando Revit "Spybee: Exportar correcciones".**
  - Comparar el modelo actual contra `building.json` usando la `Marca`: elementos borrados, creados (sin Marca) y modificados (geometría o tipo).
  - Escribir `corrections.json`.
  - *Acepta:* después de editar a mano 3 muros, borrar 1 y crear 1, el JSON refleja exactamente esos cambios.

- [ ] **T7.5 `all`: pipeline de punta a punta.**
  - Un solo comando que va de `data/raw` a `building.json`, `model.ifc`, `cloud_local.las` y `qa.html`, con tiempos por etapa.
  - *Acepta:* corre sin intervención sobre la nube de prueba. El tiempo total queda registrado.

---

## Bloque 8 · Piloto con operaciones (días 14–15)

Ver `07_evaluacion.md` §4.

- [ ] **T8.1** Un modelador de operaciones toma el RVT generado y corrige hasta dejarlo "entregable LOD 200", **con cronómetro**.
  - Anota el tiempo total y una lista breve de los problemas típicos.
- [ ] **T8.2** Exportar las correcciones. Calcular la **tasa de corrección** (% de elementos tocados) y las **horas por cada 1.000 m²**, y compararlas con el tiempo histórico de modelado manual de un edificio similar.
- [ ] **T8.3** Escribir `data/out/<p>/informe_piloto.md` con:
  - las métricas;
  - el top 5 de fallas, con imágenes;
  - una recomendación de las siguientes 3 mejoras;
  - la decisión: ¿se sigue con más nubes, con IA o con la nube?

🎯 **HITO 6 — resultado del MVP:** ¿llegamos al 80/20? Con qué datos, y qué sigue.

---

## Después del MVP (backlog priorizado)

1. **Más nubes:** correr el pipeline en 3–5 edificios distintos (obra gris, acabados, vivienda, oficinas) y ajustar los parámetros por tipo.
2. **Puertas y ventanas como familias**, con tipos por dimensión, en lugar de aberturas.
3. **Vigas y escaleras.**
4. **IA de segmentación** con pesos propios:
   - etiquetado automático transfiriendo las clases del modelo manual a la nube;
   - entrenamiento con código de Pointcept o LitePT (MIT);
   - el segmentador limpia el desorden antes del paso geométrico.
5. **Plantilla Revit de Spybee** con los tipos de muro y losa reales de operaciones y el mapeo automático de tipos.
6. **Parámetros compartidos** (`Spybee_Confianza`, `Spybee_Estado`) en lugar de Marca y Comentarios, con un filtro de vista.
7. **Portal de carga en la plataforma Spybee y procesamiento en la nube:** el contenedor Docker corre en AWS Batch y el RVT se genera con APS Design Automation.
8. **Comparación de avance escaneo vs BIM** sobre la misma base, para obras en curso.
9. **MEP asistido.**
