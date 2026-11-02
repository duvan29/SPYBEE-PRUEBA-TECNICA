# Spybee Scan2BIM — MVP

Objetivo: **pasarle una nube de puntos y recibir un modelo Revit nativo** (niveles, losas, muros, columnas, vanos y espacios) en el que el modelador solo tenga que corregir lo marcado en rojo. La meta es que la máquina haga ~80 % y la persona corrija ~20 %.

El trabajo lo hace **Claude Code** en este PC, guiado por los archivos de esta carpeta. Tú revisas los resultados en cada hito.

---

## Cómo arrancar (mañana)

### 1. Antes de abrir Claude Code (unos 30 min)

1. Copia esta carpeta al PC. La ruta debe ser corta y sin espacios, por ejemplo `C:\spybee\scan2bim`.
2. Copia la nube de puntos a `data\raw\<nombre-proyecto>\`, por ejemplo `data\raw\torre-norte\`. **No la modifiques nunca**: es el original.
   - Si viene en un formato propietario (`.rcp`/`.rcs` de ReCap, `.fls` de FARO, `.lgs` de Leica), exporta también un **E57** desde el software del escáner. Las instrucciones están en `docs/08_entorno.md`.
3. Si existe el **modelo Revit hecho a mano de ese mismo edificio**, cópialo a `data\reference\<nombre-proyecto>\`. Si puedes, expórtalo también a IFC (Revit → Exportar → IFC). Sirve para medir qué tan bien lo hace la máquina.
4. Ten a mano estos datos. Claude te los va a pedir:
   - versión de Revit instalada (2023, 2024, 2025, 2026…);
   - número de pisos y altura de piso a piso aproximada;
   - si la nube está georreferenciada y en qué sistema (CTM12 / EPSG:9377, MAGNA-SIRGAS, local…);
   - qué escáner y qué software se usaron;
   - estado del edificio al escanear: obra gris, en acabados u ocupado.

### 2. Abrir Claude Code

```powershell
cd C:\spybee\scan2bim
claude
```

Claude Code lee `CLAUDE.md` automáticamente y ahí encuentra todas sus instrucciones.

### 3. Primera sesión

Escribe:

```
/arrancar
```

Claude hace estas cuatro cosas:
1. Revisa el PC.
2. Instala el entorno de Python.
3. Analiza la nube.
4. Te entrega una **ficha de la nube**: puntos, tamaño, pisos, densidad y georreferencia.

### 4. Sesiones siguientes

```
/siguiente
```

Claude toma la siguiente tarea pendiente del plan, la ejecuta, la verifica y actualiza `PROGRESO.md`. En los hitos marcados con 🎯 se detiene a mostrarte el resultado.

Otros comandos:
- `/siguiente T4.2`: ejecuta una tarea específica.
- `/evaluar`: compara el modelo automático contra el manual y actualiza las métricas.
- `/estado`: muestra un resumen de dónde vamos y qué sigue.

---

## Mapa de la carpeta

| Archivo | Para qué |
|---|---|
| `CLAUDE.md` | Instrucciones permanentes para Claude Code: reglas, cómo trabajar, comandos |
| `PROGRESO.md` | Bitácora: estado, métricas, decisiones, preguntas abiertas. **Míralo para saber cómo vamos** |
| `docs/00_contexto.md` | Por qué hacemos esto, alcance del MVP y glosario |
| `docs/01_plan_ejecucion.md` | **El plan**: bloques, tareas, criterios de aceptación e hitos |
| `docs/02_arquitectura.md` | Estructura del código, CLI, carpetas de datos y configuración |
| `docs/03_building_json.md` | Formato intermedio `building.json`, el contrato entre Python y Revit |
| `docs/04_algoritmos.md` | Cómo se detecta cada elemento y con qué parámetros |
| `docs/05_revit_addin.md` | Especificación del add-in de Revit (C#) |
| `docs/06_georreferencia.md` | Coordenadas, CTM12 y cómo queda alineado en Revit |
| `docs/07_evaluacion.md` | Métricas, evaluación contra el modelo manual y protocolo del piloto |
| `docs/08_entorno.md` | Instalación en Windows y solución de problemas |
| `docs/referencia/` | Investigación de mercado y propuesta técnica completa |
| `.claude/commands/` | Los comandos `/arrancar`, `/siguiente`, `/evaluar` y `/estado` |
| `data/` | Nubes y resultados. **No se sube a git** |

## Cronograma esperado

| Días | Resultado visible |
|---|---|
| 1 | Ficha de la nube y nube de trabajo lista |
| 2–3 | 🎯 Niveles y losas en un IFC superpuesto a la nube |
| 4–6 | 🎯 Muros detectados (imágenes de cada piso) |
| 7–8 | 🎯 **Revit nativo** con niveles, muros y losas sobre la nube |
| 9–11 | Columnas, vanos y espacios |
| 12–13 | Confianza, reporte de calidad, evaluación y un solo comando de punta a punta |
| 14–15 | 🎯 Piloto: un modelador corrige con cronómetro y medimos el 80/20 |

Son días de trabajo efectivo. Si la nube es limpia y el edificio es regular, varias etapas salen más rápido.
