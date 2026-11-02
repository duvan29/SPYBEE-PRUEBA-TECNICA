# Spybee Scan2BIM — instrucciones para Claude Code

## Qué es este proyecto

Spybee (construction tech, Colombia) hace Scan-to-BIM: el scan leader escanea con LiDAR y después un equipo modela a mano en Revit durante semanas o meses. Este proyecto es el **MVP de un pipeline automático**:

**nube de puntos (E57/LAS/LAZ) → Python detecta niveles, losas, muros, columnas, vanos y espacios → `building.json` → IFC4 + Revit nativo (add-in C#) → el modelador corrige solo lo marcado como REVISAR**

- Meta: ~80 % del modelo correcto en automático y ~20 % de correcciones.
- Alcance: LOD 200 de arquitectura y estructura.
- MEP, muros curvos, escaleras y familias específicas del cliente están **fuera** del MVP.
- El contexto completo está en `docs/00_contexto.md`.

El usuario habla español: responde siempre en español. El código, los identificadores y los comentarios técnicos van en inglés; los mensajes al usuario y los documentos, en español.

## Cómo trabajar en cada sesión

1. Lee `PROGRESO.md` (estado actual) y busca en `docs/01_plan_ejecucion.md` la **primera tarea sin marcar** (`- [ ]`), o la que pida el usuario.
2. Antes de programar una etapa, lee su documento de diseño:

   | Etapa | Documento |
   |---|---|
   | Estructura del código, CLI, configuración | `docs/02_arquitectura.md` |
   | Formato de salida | `docs/03_building_json.md` |
   | Detección (niveles, losas, muros, columnas, vanos, espacios) | `docs/04_algoritmos.md` |
   | Revit | `docs/05_revit_addin.md` |
   | Coordenadas | `docs/06_georreferencia.md` |
   | Métricas | `docs/07_evaluacion.md` |
   | Instalación | `docs/08_entorno.md` |

3. Antes de empezar, cuenta en 2–4 líneas qué vas a hacer.
4. Implementa la tarea y **verifícala contra su criterio de aceptación**:
   - corre el comando sobre la nube real;
   - **abre y mira los PNG de depuración** con la herramienta de lectura de imágenes.

   Los PNG son la forma principal de comprobar que la geometría tiene sentido. No des una tarea por terminada sin haberlos mirado.
5. Marca la casilla en `docs/01_plan_ejecucion.md`, añade una entrada a la bitácora de `PROGRESO.md` (qué se hizo, resultado, problemas) y haz un commit pequeño con git.
6. En los **hitos 🎯**, detente: muestra al usuario los resultados (rutas de los PNG, IFC o RVT, métricas) y espera su visto bueno antes de seguir.
7. Si algo te bloquea más de ~1 hora de intentos, no insistas a ciegas:
   - registra el bloqueo en `PROGRESO.md`;
   - propone una versión simplificada que permita avanzar (por ejemplo, un parámetro fijo o un caso manual);
   - pregunta al usuario.

**Prioridad: velocidad con resultados visibles.** Primero algo que funcione de punta a punta sobre la nube real, y después mejorarlo. No sobre-diseñes.

## Reglas duras

- **`data/raw/` es de solo lectura.** Nunca modifiques, muevas ni borres nada ahí.
- **Nunca cargues la nube completa sin submuestrear.**
  - Lee por bloques o por escaneo y submuestrea a 1 cm antes de acumular.
  - Antes de leer, compara el tamaño del archivo contra la RAM libre.
- **Unidades:** metros en todo Python. Revit trabaja internamente en **pies**: convierte siempre con `UnitUtils.ConvertToInternalUnits(valor, UnitTypeId.Meters)`.
- **Coordenadas:**
  - Lee en float64.
  - Si son grandes (más de 100 km, típico de CTM12), resta un `offset` redondo y trabaja en coordenadas locales. El offset se guarda en `building.json`.
  - Ver `docs/06_georreferencia.md`.
- **No rotes la nube.** La dirección dominante de los muros se usa solo para regularizar, no para transformar los datos.
- **`building.json` es el contrato** entre Python y Revit. Si cambias el formato, actualiza `docs/03_building_json.md` y sube `schema_version`.
- **Parámetros en `config/default.yaml`**, no metidos en el código.
- Cada etapa escribe sus PNG de depuración en `data/out/<proyecto>/debug/<etapa>/`.
- No imprimas arreglos gigantes. En los logs van resúmenes: conteos, rangos y tiempos.
- **Windows y PowerShell:** usa `pathlib` para las rutas y no asumas comandos de Linux.
- **Licencias:**
  - Solo dependencias que permitan uso comercial: MIT, BSD, Apache-2.0, y LGPL usada como librería.
  - **No uses pesos ni datasets con licencia CC BY-NC**: Sonata, Utonia, SpatialLM, OneFormer3D, ScanNet, Structured3D.
- **No subas nubes ni modelos de clientes a servicios externos** sin autorización explícita del usuario.
- Antes de instalar algo pesado, pregunta: CUDA, Visual Studio o librerías de varios GB.

## Comandos del pipeline (cuando existan)

```powershell
conda activate scan2bim
python -m scan2bim inspect  --project <p>   # ficha de la nube
python -m scan2bim prep     --project <p>   # nube de trabajo 1 cm + normales
python -m scan2bim levels   --project <p>   # niveles y división por pisos
python -m scan2bim slabs    --project <p>
python -m scan2bim walls    --project <p>
python -m scan2bim columns  --project <p>
python -m scan2bim openings --project <p>
python -m scan2bim spaces   --project <p>
python -m scan2bim export   --project <p>   # building.json + model.ifc + nube local para Revit
python -m scan2bim qa       --project <p>   # reporte de calidad HTML
python -m scan2bim eval     --project <p>   # comparación contra data/reference
python -m scan2bim all      --project <p>   # todo de punta a punta
pytest -q
```

Revit: add-in en `revit/`, compilado con `dotnet build`. Los comandos aparecen en Revit en **Complementos → Herramientas externas**. Ver `docs/05_revit_addin.md`.

## Estructura

```
config/       parámetros (default.yaml)
scan2bim/     paquete Python del pipeline
revit/        add-in C# de Revit
tests/        pytest
data/raw/<p>/        nube original (SOLO LECTURA)
data/reference/<p>/  modelo manual RVT/IFC (para evaluar)
data/work/<p>/       intermedios (LAZ, npz)
data/out/<p>/        building.json, model.ifc, qa.html, debug/*.png
```
