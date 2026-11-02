# 00 · Contexto del proyecto

## El problema

En Spybee, el Scan-to-BIM funciona así hoy:

1. El ingeniero o scan leader va a la obra y escanea con LiDAR.
2. Registra la nube en el software del escáner.
3. El equipo de operaciones, o un tercero contratado, **modela todo a mano en Revit** encima de la nube.

El tiempo no se va en el escaneo. En el mercado, el modelado manual se lleva **entre el 85 % y el 95 % del trabajo**. Un caso documentado registró 8 noches de escaneo, 8 días de registro y 300 días de modelado. Un proyecto típico de unos 5.000 m² toma entre 6 y 12 semanas de punta a punta. Tercerizar el modelado cuesta entre US$1,6 y 2,7 por m² en LOD 200 y entre US$2,7 y 4,8 por m² en LOD 300, según las tarifas publicadas por proveedores internacionales. Para 5.000 m² eso suma entre US$8.000 y 24.000.

## La solución que construimos en este MVP

Un pipeline que recibe **la nube que entrega el scan leader** y produce, en automático:

1. un **`building.json`** con todos los elementos detectados y una **confianza** de 0 a 1 para cada uno;
2. un **IFC4**, para verlo en cualquier visor y como formato abierto;
3. un **modelo Revit nativo**, generado por un add-in propio. Tiene muros, losas, columnas y vanos de verdad, no geometría importada. Lo dudoso queda marcado **REVISAR** y pintado en rojo en una vista `00_REVISAR`, con la nube vinculada encima;
4. un **reporte de calidad**, con la desviación nube–modelo de cada elemento.

El modelador abre el RVT y corrige solo lo que está en rojo. **Meta: ~80 % automático y ~20 % de corrección**, medido en horas humanas y no solo en número de elementos.

## Alcance del MVP

| Entra (LOD 200, arquitectura y estructura) | No entra (después) |
|---|---|
| Niveles y cotas de piso | MEP: tubería, ductos, bandejas |
| Losas: contorno y espesor | Muros curvos, muros cortina, fachadas acristaladas complejas |
| Muros rectos, incluso no ortogonales, con espesor y altura | Escaleras, rampas, vigas descolgadas |
| Columnas rectangulares y circulares | Elementos ocultos (dentro de muros, sobre cielos rasos) |
| Vanos rectangulares: aberturas, puertas y ventanas genéricas | Familias y tipos específicos del cliente (LOD 300+) |
| Espacios, con su área | IA o deep learning: va después, con datos propios |
| Georreferencia, si la nube la trae | Infraestructura en la nube (AWS, Design Automation) |

**Decisión clave:** el MVP es **geométrico**. Usa RANSAC, cortes 2D, histogramas y ajuste de primitivas. No necesita entrenar IA y funciona desde la primera nube. La IA se agrega cuando haya 20–50 pares nube + modelo manual, sobre todo para limpiar el desorden de obra: andamios, material y personas.

## Particularidades de Colombia a tener en cuenta

- **Sistemas constructivos frecuentes:**
  - pórticos de concreto con mampostería de 10–15 cm;
  - en vivienda, sobre todo VIS, **sistema industrializado** con muros de concreto vaciado de 8–12 cm y sin columnas.

  El algoritmo debe soportar ambos casos.
- En obra gris, una columna embebida en un muro de ladrillo es casi coplanar con él. El color o la intensidad pueden ayudar a distinguirla. En el MVP, se marca como REVISAR.
- **Altura de piso a piso típica:** 2,3–2,7 m en vivienda y 3,0–4,0 m en oficinas o comercio.
- **Sistema de coordenadas oficial:** Origen Nacional CTM12, **EPSG:9377** (IGAC, Resolución 471 de 2020).
- **Entregables usuales:** RVT, IFC y DWG. Los planos en DWG se usan para trámites ante la curaduría.

## Lecciones de la investigación de mercado

Los documentos completos están en `docs/referencia/`.

- **Ningún producto del mercado entrega un LOD 300 sin revisión humana.** Los servicios más rápidos (IPX, Matterport, Moving Atoms) prometen de unas horas a 48 h, siempre con personas revisando. Por eso nuestro enfoque es una propuesta automática más una revisión guiada.
- **Cloud2BIM** es un pipeline abierto (licencia MIT) que hace algo parecido: losas por histograma, muros, vanos rectangulares y salida IFC con IfcOpenShell. Es una **referencia útil para leer**: https://github.com/VaclavNezerka/Cloud2BIM. Si se copia código, hay que conservar el aviso de licencia MIT.
- Los mejores modelos de IA abiertos para nubes (Sonata, Utonia, SpatialLM, OneFormer3D) tienen pesos **CC BY-NC, que no permiten uso comercial**. Cuando entre la IA, se entrenan pesos propios con el código de Pointcept o LitePT, que es MIT.
- La importación de IFC en Revit genera elementos poco editables. Por eso el Revit se genera con un **add-in propio que crea elementos nativos**.

## Glosario

| Término | Significado |
|---|---|
| **Nube de puntos** | Millones de puntos XYZ, con color e intensidad, que salen del escáner |
| **E57 / LAS / LAZ** | Formatos abiertos de nube. LAZ es LAS comprimido |
| **RCP/RCS, FLS, LGS** | Formatos propietarios de Autodesk ReCap, FARO y Leica. Hay que exportarlos a E57 |
| **Registro** | Unir los escaneos individuales en una sola nube coherente |
| **SLAM / TLS** | Escáner móvil que se lleva caminando / escáner terrestre fijo sobre trípode |
| **LOD** | Level of Development: cuánto detalle tiene el modelo. 200 es geometría aproximada con tipos genéricos; 300 es geometría precisa con tipos definidos |
| **LOA** | Level of Accuracy (USIBD): tolerancia de precisión. LOA20 es 15 mm–5 cm; LOA30 es 5–15 mm |
| **IFC** | Formato BIM abierto. IFC4 es la versión estándar actual |
| **RVT** | Archivo nativo de Revit |
| **Coordenadas compartidas** | Mecanismo de Revit para ubicar el modelo en coordenadas reales sin mover la geometría |
| **HITL** | Human-in-the-loop: la máquina propone y una persona aprueba o corrige |
| **P/R** | Precisión y exhaustividad (recall): qué fracción de lo detectado es correcto, y qué fracción de lo real se detectó |
