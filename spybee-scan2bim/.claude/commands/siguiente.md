---
description: Ejecuta la siguiente tarea pendiente del plan, o la tarea indicada (ej. /siguiente T4.2)
argument-hint: "[ID de tarea opcional, ej. T4.2]"
---

1. Lee `PROGRESO.md` y `docs/01_plan_ejecucion.md`.

2. Elige la tarea:
   - si el usuario indicó una tarea (`$ARGUMENTS`), esa;
   - si no, la **primera casilla sin marcar** (`- [ ]`).

3. Lee los documentos de diseño que esa tarea referencia (`docs/02` a `docs/08`).

4. Dile al usuario en 2–4 líneas qué vas a hacer y cuál es el criterio de aceptación.

5. Implementa la tarea. Corre el comando sobre la nube real del proyecto (`data/raw/<proyecto>`), no solo sobre datos de prueba.

6. **Verifica:**
   - abre y mira los PNG de depuración que generó la etapa;
   - comprueba el criterio de aceptación con números;
   - corre `pytest -q` si hay pruebas.

7. Si pasa:
   - marca `- [x]` en el plan;
   - añade una entrada a la bitácora de `PROGRESO.md` con lo que se hizo, los números, las rutas de los PNG y los pendientes;
   - actualiza "Estado actual";
   - haz un commit con git: `T#.# descripción corta`.

8. Si no pasa después de intentos razonables:
   - registra el bloqueo en `PROGRESO.md`;
   - propone una simplificación;
   - pregunta al usuario.

9. Si la tarea cierra un **hito 🎯**, detente: muestra los resultados (PNG, IFC o RVT, métricas) y espera el visto bueno del usuario.

10. Si no es un hito, di cuál es la siguiente tarea y pregunta si continúas. Si el usuario ya pidió avanzar varias tareas seguidas, continúa sin preguntar hasta el siguiente hito.
