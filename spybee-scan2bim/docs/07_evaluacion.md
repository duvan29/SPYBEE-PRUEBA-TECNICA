# 07 · Evaluación, métricas y piloto

La pregunta que tiene que responder el MVP: **¿la máquina hace ~80 % y la persona corrige ~20 %?** Hay tres formas de medirlo, de menor a mayor esfuerzo:

1. **Sin referencia:** métricas internas, como la desviación nube–modelo y el % de elementos en REVISAR.
2. **Con referencia:** comparar contra el modelo hecho a mano del mismo edificio (`eval`).
3. **Piloto real:** un modelador corrige el RVT generado, con cronómetro. **Es la medida que importa.**

---

## §1 Preparar la referencia

En Revit, con el modelo manual abierto:
1. Ir a Archivo → Exportar → IFC.
2. Elegir **IFC4 Reference View** o IFC2x3 Coordination View 2.0.
3. En la configuración, escoger "Exportar elementos visibles en la vista: no" y el sistema de coordenadas **"Coordenadas compartidas"** si el modelo está georreferenciado. Si no lo está, "Origen interno".
4. Guardar en `data/reference/<p>/modelo_manual.ifc`.

**Alineación:**
- El modelo manual se modeló sobre la misma nube. Si el modelador la vinculó de origen a origen, el IFC exportado en coordenadas internas queda en el marco de la nube original.
- `eval` debe:
  1. convertir la referencia al marco local restando el `offset` si hace falta;
  2. **verificar la alineación**, comparando la mediana de la distancia de los ejes de los muros de la referencia a la nube;
  3. si el error es mayor a 10 cm, estimar una transformación 2D rígida con ICP entre los ejes de la referencia y los automáticos, aplicarla y **reportarla**.

**Unidades del IFC:** Revit puede exportar en mm. Usar `ifcopenshell.util.unit.calculate_unit_scale(f)` para pasar a metros.

**Lectura de la referencia con IfcOpenShell:**
- **Muros (`IfcWall`):**
  - eje a partir de la representación `Axis` más `ifcopenshell.util.placement.get_local_placement(...)`;
  - espesor a partir del material (`IfcMaterialLayerSetUsage`) o de la geometría.
  - Si no hay `Axis`, usar la geometría (`ifcopenshell.geom`): rectángulo mínimo de la huella.
- **Losas (`IfcSlab`):** huella 2D con `ifcopenshell.geom` y proyección; la cota es la z superior.
- **Columnas (`IfcColumn`):** centro y sección de la huella.
- **Vanos:** `IfcOpeningElement` y `IfcDoor`/`IfcWindow`, con su posición sobre el muro anfitrión.
- **Niveles:** `IfcBuildingStorey.Elevation`.

## §2 Emparejamiento y métricas (`eval`)

| Clase | Regla de emparejamiento (uno a uno, greedy por mejor puntaje) | Métricas |
|---|---|---|
| Niveles | Diferencia de cota ≤ 5 cm | Recall, error medio de cota |
| Muros | Mismo piso, ángulo ≤ 5°, distancia entre ejes ≤ 10 cm, solape ≥ 50 % del más corto | Precisión, recall, mediana y p90 del error del eje (cm), % con espesor correcto (±1 cm), % de longitud cubierta |
| Losas | Mismo nivel, IoU de huella ≥ 0,7 | P/R, IoU medio, error de espesor |
| Columnas | Mismo piso, centros a ≤ 15 cm | P/R, error de sección |
| Vanos | Mismo muro emparejado, centro a ≤ 30 cm, ancho ±15 cm | P/R por tipo (puerta, ventana) |
| Espacios | IoU ≥ 0,7 | P/R, error de área (%) |

Además:
- **Calibración de la confianza:** precisión de los elementos `auto` frente a los `review`. Los `auto` deberían ser correctos en ≥ 95 %.
- **Tiempo de cómputo** por etapa.

**Salidas:**
- `data/out/<p>/eval.json`;
- PNG en `debug/eval/`: por piso, la referencia en gris, los aciertos automáticos en verde, los falsos positivos en rojo y los faltantes en azul;
- una fila nueva en `PROGRESO.md`.

## §3 Metas del MVP

| Métrica | Meta del MVP | Comentario |
|---|---|---|
| Recall de niveles | 100 % | Error de cota ≤ 3 cm |
| P/R de muros | ≥ 90 % / ≥ 85 % | Meta del producto: 95 % |
| Error del eje de muros (mediana) | ≤ 2 cm | p90 ≤ 5 cm |
| Espesor correcto de muros | ≥ 80 % | Los muros vistos por una sola cara tiran el número hacia abajo |
| P/R de losas | ≥ 95 % | |
| P/R de columnas | ≥ 85 % | Exentas. Las embebidas se miden aparte |
| P/R de vanos | ≥ 70 % | Es la clase más difícil y entra al 20 % a revisar |
| Precisión de los `auto` | ≥ 95 % | Si no se cumple, subir el umbral de confianza |
| Tiempo de cómputo, 5.000 m² | ≤ 90 min | En el PC actual |
| **Tasa de corrección (piloto)** | **≤ 20–30 %** | Ver §4 |
| **Horas humanas por 1.000 m² (piloto)** | **Medir; meta ≤ 2,5 h en LOD 200 de arquitectura y estructura** | Comparar con el tiempo histórico manual |

Las metas se ajustan con los datos reales y cada cambio se registra en "Decisiones" de `PROGRESO.md`.

## §4 Protocolo del piloto (Bloque 8)

1. **Elegir al modelador.** Que conozca el estándar de operaciones y no haya participado en el desarrollo.
2. **Darle:**
   - el RVT generado con la nube vinculada;
   - la vista `00_REVISAR`;
   - el `qa.html`;
   - la instrucción: "déjalo entregable LOD 200 de arquitectura y estructura según el estándar Spybee".
3. **Cronometrar** el tiempo efectivo, sin pausas, separado en:
   - revisar los elementos en rojo;
   - corregir los elementos no marcados que estaban mal (errores silenciosos: importantes);
   - agregar lo que faltó.
4. **Al terminar:** ejecutar `Spybee: Exportar correcciones` → `corrections.json`.
5. **Entrevista de 10 minutos:**
   - ¿qué fue lo más molesto?;
   - ¿en qué confiaste y en qué no?;
   - ¿qué te ahorró más tiempo?
6. **Calcular:**
   - la tasa de corrección por clase;
   - las horas por cada 1.000 m²;
   - el **% de errores silenciosos**: elementos `auto` que hubo que corregir. Este es el número más importante para la confianza.
7. **Comparar con la línea base:**
   - horas reales de modelado manual de un edificio similar, según el registro de operaciones o la factura del tercero;
   - costo por m² del tercero.
8. **Escribir** `informe_piloto.md` (ver T8.3).
