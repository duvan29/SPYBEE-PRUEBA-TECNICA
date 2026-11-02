---
description: Primera sesión. Diagnóstico del PC, entorno de Python y ficha de la nube de puntos
---

Esta es la **primera sesión** del MVP Scan2BIM de Spybee.

1. Lee `CLAUDE.md`, `README.md`, `docs/00_contexto.md` y `docs/01_plan_ejecucion.md` completos. Después lee `docs/08_entorno.md`.

2. Saluda al usuario en español y explícale en 5 líneas qué vas a hacer hoy: el Bloque 1 del plan.

3. **Pregunta los datos del proyecto** que falten en `PROGRESO.md` y en `data/raw/<proyecto>/info.yaml`:
   - nombre del proyecto;
   - versión de Revit;
   - número de pisos y altura de piso a piso;
   - si la nube está georreferenciada y en qué sistema;
   - escáner y software usados;
   - estado del edificio;
   - si existe el modelo manual de referencia.

   Hazlo en una sola pregunta agrupada. Si el usuario no sabe algo, sigue y anótalo como pregunta abierta.

4. Ejecuta las tareas **T1.1 a T1.5** del plan, en orden y siguiendo el flujo de trabajo de `CLAUDE.md`: verifica, mira los PNG, marca la casilla, actualiza la bitácora y haz commit.
   - Pide permiso antes de instalar cosas pesadas.
   - Si la nube está en un formato que Python no lee (`.rcp`, `.rcs`, `.fls`, `.lgs`), detente y dale al usuario las instrucciones de exportación a E57 de `docs/08_entorno.md`.

5. Al terminar, muestra la **ficha de la nube** (`data/out/<proyecto>/ficha.md`) y los PNG principales. Termina con el hito del Bloque 1: pregunta si la ficha coincide con lo que el equipo sabe del edificio.

$ARGUMENTS
