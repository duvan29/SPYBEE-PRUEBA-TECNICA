---
description: Compara el modelo automático contra el modelo manual de referencia y actualiza las métricas
argument-hint: "[proyecto opcional]"
---

1. Lee `docs/07_evaluacion.md`.

2. Busca el proyecto en `$ARGUMENTS`. Si no viene, usa el de `PROGRESO.md`.

3. Revisa que exista la referencia en `data/reference/<proyecto>/`:
   - Si hay un IFC, úsalo.
   - Si solo hay RVT, pide al usuario que lo exporte a IFC desde Revit. Las instrucciones están en `docs/07_evaluacion.md`.
   - Si no hay referencia, haz solo la evaluación sin referencia: desviación nube–modelo y % de elementos a revisar.

4. Ejecuta `python -m scan2bim eval --project <p>`. Si el comando todavía no existe y el plan ya llegó al Bloque 7, impleméntalo según `docs/07_evaluacion.md`.

5. Mira los PNG de comparación de `data/out/<p>/debug/eval/`.

6. Agrega una fila a la tabla de **Métricas** de `PROGRESO.md` con la fecha, la versión (hash corto de git) y las métricas.

7. Resume al usuario en español:
   - qué tan cerca estamos del 80/20;
   - qué clase de elemento falla más y por qué, con ejemplos visuales;
   - qué mejorarías primero.
