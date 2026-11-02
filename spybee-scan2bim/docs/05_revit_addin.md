# 05 · Add-in de Revit (C#)

**Por qué un add-in y no importar el IFC:** al importar un IFC, Revit crea elementos poco editables, muchas veces formas directas (DirectShape). El modelador necesita **muros, losas y columnas nativos** para corregir rápido, con los grips de siempre. Por eso un add-in lee `building.json` y crea los elementos con la Revit API.

## Comandos

| Comando (en Complementos → Herramientas externas) | Qué hace | Tarea |
|---|---|---|
| `Spybee: Hola` | Prueba de instalación | T5.1 |
| `Spybee: Generar modelo` | Lee `building.json` y crea niveles, tipos, muros, losas, columnas, vanos y recintos. Además marca los elementos AUTO/REVISAR, crea las vistas y, si aplica, las coordenadas compartidas | T5.2–T5.4, T6.4 |
| `Spybee: Exportar correcciones` | Compara el modelo actual con `building.json` y escribe `corrections.json` | T7.4 |

## Proyecto

```
revit/
├── Spybee.Scan2BIM.Revit/
│   ├── Spybee.Scan2BIM.Revit.csproj
│   ├── Commands/HelloCommand.cs
│   ├── Commands/GenerateModelCommand.cs
│   ├── Commands/ExportCorrectionsCommand.cs
│   ├── Model/BuildingModel.cs        # clases que reflejan building.json (System.Text.Json)
│   ├── Build/ModelBuilder.cs         # lógica de creación (sin UI: reutilizable en Design Automation)
│   ├── Build/TypeFactory.cs          # tipos de muro, losa, columna y abertura por dimensión
│   ├── Build/ReviewMarker.cs         # Marca/Comentarios + overrides de la vista 00_REVISAR
│   └── Util/Units.cs                 # M(metros) → pies
├── Spybee.Scan2BIM.addin
└── install.ps1                       # compila y copia el .addin a %AppData%\Autodesk\Revit\Addins\<año>\
```

### Versión de Revit → framework

| Revit | TargetFramework | JSON |
|---|---|---|
| 2025, 2026 | `net8.0-windows` | `System.Text.Json`, incluido |
| 2021–2024 | `net48` | Paquete NuGet `System.Text.Json`, o `DataContractJsonSerializer` |
| 2027 o superior | Revisar la guía de la API de esa versión | — |

### `.csproj` (Revit 2025 o 2026)

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <RevitVersion>2025</RevitVersion>
    <TargetFramework>net8.0-windows</TargetFramework>
    <UseWindowsForms>true</UseWindowsForms>   <!-- OpenFileDialog -->
    <PlatformTarget>x64</PlatformTarget>
    <ImplicitUsings>disable</ImplicitUsings>   <!-- evita choques de nombres con la Revit API -->
    <Nullable>enable</Nullable>
    <EnableDynamicLoading>true</EnableDynamicLoading>
  </PropertyGroup>
  <ItemGroup>
    <Reference Include="RevitAPI">
      <HintPath>C:\Program Files\Autodesk\Revit $(RevitVersion)\RevitAPI.dll</HintPath>
      <Private>false</Private>
    </Reference>
    <Reference Include="RevitAPIUI">
      <HintPath>C:\Program Files\Autodesk\Revit $(RevitVersion)\RevitAPIUI.dll</HintPath>
      <Private>false</Private>
    </Reference>
  </ItemGroup>
</Project>
```

### Manifiesto `.addin`

`install.ps1` reemplaza la ruta del ensamblado (`Assembly`) por la ruta absoluta de la DLL compilada.

```xml
<?xml version="1.0" encoding="utf-8"?>
<RevitAddIns>
  <AddIn Type="Command">
    <Name>Spybee: Hola</Name>
    <Assembly>__DLL_PATH__</Assembly>
    <AddInId>7d1b2c4e-0a51-4f3e-9b2a-5a1c00000001</AddInId>
    <FullClassName>Spybee.Scan2BIM.Revit.Commands.HelloCommand</FullClassName>
    <VendorId>SPYB</VendorId>
    <VendorDescription>Spybee</VendorDescription>
  </AddIn>
  <AddIn Type="Command">
    <Name>Spybee: Generar modelo</Name>
    <Assembly>__DLL_PATH__</Assembly>
    <AddInId>7d1b2c4e-0a51-4f3e-9b2a-5a1c00000002</AddInId>
    <FullClassName>Spybee.Scan2BIM.Revit.Commands.GenerateModelCommand</FullClassName>
    <VendorId>SPYB</VendorId>
    <VendorDescription>Spybee</VendorDescription>
  </AddIn>
  <AddIn Type="Command">
    <Name>Spybee: Exportar correcciones</Name>
    <Assembly>__DLL_PATH__</Assembly>
    <AddInId>7d1b2c4e-0a51-4f3e-9b2a-5a1c00000003</AddInId>
    <FullClassName>Spybee.Scan2BIM.Revit.Commands.ExportCorrectionsCommand</FullClassName>
    <VendorId>SPYB</VendorId>
    <VendorDescription>Spybee</VendorDescription>
  </AddIn>
</RevitAddIns>
```

**Importante:** Revit bloquea la DLL mientras está abierto. **Cierra Revit antes de compilar o instalar.** Para iterar más rápido existe el "Add-In Manager" del SDK de Revit, pero es opcional.

## Lógica de "Generar modelo"

Todo ocurre dentro de **una transacción**, `"Spybee: Generar modelo"`, y termina con un `TaskDialog` de resumen: cuántos elementos se crearon por clase, cuántos fallaron y por qué.

```csharp
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;

[Transaction(TransactionMode.Manual)]
public class GenerateModelCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
    {
        Document doc = data.Application.ActiveUIDocument.Document;
        string? path = Dialogs.PickFile("building.json|*.json");
        if (path == null) return Result.Cancelled;
        BuildingModel model = BuildingModel.Load(path);
        var report = new GenerationReport();
        using (var t = new Transaction(doc, "Spybee: Generar modelo"))
        {
            t.Start();
            new ModelBuilder(doc, model, report).Run();   // niveles → tipos → muros → losas → columnas → regenerar → vanos → recintos → marcas → vistas → coordenadas
            t.Commit();
        }
        TaskDialog.Show("Spybee Scan2BIM", report.ToString());
        return Result.Succeeded;
    }
}
```

### Unidades

Revit trabaja internamente en **pies**. Toda distancia del JSON pasa por:

```csharp
static double M(double meters) => UnitUtils.ConvertToInternalUnits(meters, UnitTypeId.Meters);
```

Los ángulos van en radianes.

### 1. Niveles

- Si ya existe un nivel con la misma cota (±1 cm), reutilizarlo y renombrarlo. Si no, `Level.Create(doc, M(elevation))` y luego `level.Name = "Piso 1"`.
- Las plantillas suelen traer "Nivel 1" y "Nivel 2". Reutilizarlos en vez de duplicarlos.
- Guardar un diccionario `id → Level`.

### 2. Tipos por dimensión (`TypeFactory`)

**Muros:** `Spybee Generico {cm} cm`, de una sola capa.

```csharp
WallType GetWallType(double tM) {
    string name = $"Spybee Generico {Math.Round(tM * 100)} cm";
    var found = new FilteredElementCollector(doc).OfClass(typeof(WallType)).Cast<WallType>()
                  .FirstOrDefault(w => w.Name == name);
    if (found != null) return found;
    var baseType = new FilteredElementCollector(doc).OfClass(typeof(WallType)).Cast<WallType>()
                  .First(w => w.Kind == WallKind.Basic);
    var wt = (WallType)baseType.Duplicate(name);
    wt.SetCompoundStructure(CompoundStructure.CreateSingleLayerCompoundStructure(
        MaterialFunctionAssignment.Structure, M(tM), ElementId.InvalidElementId));
    return wt;
}
```

**Losas:** igual que los muros, con `FloorType` sin losas de cimentación (`!IsFoundationSlab`) y nombre `Spybee Losa {cm} cm`.

### 3. Muros

```csharp
var line = Line.CreateBound(new XYZ(M(x0), M(y0), 0), new XYZ(M(x1), M(y1), 0));
Wall wall = Wall.Create(doc, line, wallType.Id, baseLevel.Id, M(w.Height), M(w.BaseOffset), false, false);
wall.get_Parameter(BuiltInParameter.WALL_HEIGHT_TYPE).Set(topLevel.Id);                 // restricción superior
double topOffset = (baseLevelElev + w.BaseOffset + w.Height) - topLevelElev;             // normalmente ≈ −espesor de la losa
wall.get_Parameter(BuiltInParameter.WALL_TOP_OFFSET).Set(M(topOffset));
```

- La línea de ubicación debe ser el **eje del muro**. Verificar que `WALL_KEY_REF_PARAM` sea 0 (Wall Centerline). Si no lo es, fijarlo.
- Descartar los ejes más cortos que `doc.Application.ShortCurveTolerance` y registrarlos en el reporte.

### 4. Losas (Revit 2022 o superior)

```csharp
var loop = new CurveLoop();
for (int i = 0; i < pts.Count; i++)
    loop.Append(Line.CreateBound(P(pts[i]), P(pts[(i + 1) % pts.Count])));
var loops = new List<CurveLoop> { loop };      // + loops interiores para huecos
Floor floor = Floor.Create(doc, loops, floorType.Id, level.Id);
floor.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM)?.Set(M(s.TopOffset));
```

Antes de crear el `CurveLoop`, eliminar los vértices duplicados o colineales.

### 5. Columnas

- Buscar en el documento una familia de **columna estructural** rectangular y una circular.
- **Si no hay**, mostrar un `TaskDialog` que pida cargarla (Insertar → Cargar familia) o elegir el `.rfa` con un diálogo. Luego `doc.LoadFamily(path, out Family f)`.
- Duplicar el tipo por sección: `Spybee Col 30x50`. Los parámetros de dimensión cambian según la familia y el idioma:
  - candidatos para rectangulares: `b`, `h`, `Width`, `Depth`, `Ancho`, `Anchura`, `Profundidad`;
  - para circulares: `b`, `Diameter`, `Diámetro`.

  Registrar en el reporte cuáles se encontraron.

```csharp
if (!sym.IsActive) sym.Activate();
var pt = new XYZ(M(cx), M(cy), 0);
FamilyInstance col = doc.Create.NewFamilyInstance(pt, sym, baseLevel, StructuralType.Column);
col.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM).Set(topLevel.Id);
ElementTransformUtils.RotateElement(doc, col.Id, Line.CreateBound(pt, pt + XYZ.BasisZ), rotRad);
```

### 6. Vanos

Antes de crear vanos, llamar a `doc.Regenerate()`.

**v1, aberturas rectangulares en el muro:** son simples y robustas, y en obra gris representan bien un vano sin carpintería.

```csharp
// u0 = offset_along, u1 = offset_along + width, sobre el eje del muro; z absolutas
XYZ a = PointOnAxis(wall, u0, baseElev + sill);
XYZ b = PointOnAxis(wall, u1, baseElev + sill + height);
Opening op = doc.Create.NewOpening(wall, a, b);
```

**v2, puertas y ventanas genéricas** (backlog):
- `doc.Create.NewFamilyInstance(pointOnAxis, symbol, wall, level, StructuralType.NonStructural)`.
- Los tipos se duplican por ancho × alto (`FAMILY_WIDTH_PARAM`, `FAMILY_HEIGHT_PARAM`).
- Las ventanas llevan antepecho (`INSTANCE_SILL_HEIGHT_PARAM`).

### 7. Recintos

Después de regenerar: `Room room = doc.Create.NewRoom(level, new UV(M(seed.x), M(seed.y)));`. Si falla porque el punto no queda en un área cerrada, registrarlo en el reporte y seguir.

### 8. Marcado AUTO/REVISAR (v1, sin parámetros compartidos)

- `ALL_MODEL_MARK` = `id` (por ejemplo `W-0001`). Si el elemento no tiene Marca (recintos, aberturas), poner el `id` en Comentarios.
- `ALL_MODEL_INSTANCE_COMMENTS` = `"AUTO conf=0.93"` o `"REVISAR conf=0.62 motivo=one_face,low_coverage"`.
- Usar siempre `?.Set(...)`: no todos los elementos tienen esos parámetros.

### 9. Vistas

- Una planta por nivel, `Spybee - Piso N`, con `ViewPlan.Create(doc, vftFloorPlan.Id, level.Id)`.
- Una vista 3D `00_REVISAR` con `View3D.CreateIsometric(doc, vft3D.Id)`. Si el nombre ya existe, reutilizar la vista.
- En `00_REVISAR` y en las plantas Spybee, aplicar un **override en rojo** a cada elemento REVISAR:

```csharp
// Relleno sólido SIN depender del nombre (el nombre cambia con el idioma de Revit):
ElementId solid = new FilteredElementCollector(doc).OfClass(typeof(FillPatternElement))
    .Cast<FillPatternElement>().First(f => f.GetFillPattern().IsSolidFill).Id;
var ogs = new OverrideGraphicSettings();
ogs.SetProjectionLineColor(new Color(200, 0, 0));
ogs.SetSurfaceForegroundPatternId(solid);
ogs.SetSurfaceForegroundPatternColor(new Color(255, 90, 90));
ogs.SetCutForegroundPatternId(solid);
ogs.SetCutForegroundPatternColor(new Color(255, 90, 90));
view.SetElementOverrides(elementId, ogs);
```

### 10. Coordenadas compartidas y nube (ver `06_georreferencia.md`)

- Si `georef.crs != "local"`, asignar el `offset` real a la posición del proyecto: el punto de reconocimiento (Survey Point) queda en las coordenadas reales del origen interno.

```csharp
var pos = new ProjectPosition(M(offset.x), M(offset.y), M(offset.z), trueNorthRad);  // este, norte, cota, ángulo
doc.ActiveProjectLocation.SetProjectPosition(XYZ.Zero, pos);
```

  **Verificar el signo del ángulo** con un punto de control. En el MVP `true_north_deg` vale 0, así que este paso no debería dar problemas.

- **Nube (opcional automatizar):**
  - `PointCloudType.Create(doc, "rcp", rutaRcp)` y `PointCloudInstance.Create(doc, tipo.Id, Transform.Identity)`.
  - En el MVP basta con instrucciones al usuario: Insertar → Nube de puntos → `cloud_local.las` (o el RCP convertido con ReCap) → posicionamiento **Automático – Origen a origen**.

## "Exportar correcciones"

1. Pedir el `building.json` original.
2. Recolectar los elementos de las categorías muros, suelos, pilares estructurales, recintos y aberturas.
3. Indexar los elementos por `Marca`, o por el `id` en Comentarios.
4. Para cada `id` original:
   - **deleted**, si ya no existe;
   - **modified**, si cambió:
     - el eje del muro movido más de 2 cm, en cualquier extremo;
     - el espesor (ancho del tipo) cambió;
     - la altura o la restricción cambiaron más de 2 cm;
     - el contorno de la losa (por área) cambió más de 1 %;
     - la columna se movió o cambió de tipo;
   - **unchanged**, en cualquier otro caso.
5. Los elementos de esas categorías **sin `id` Spybee** son **created**.
6. Escribir `corrections.json` junto al `building.json`:

```json
{
  "source": "building.json", "rvt": "Torre Norte.rvt", "exported": "2026-11-15T17:40:00-05:00",
  "summary": { "walls": {"total_auto": 412, "unchanged": 350, "modified": 41, "deleted": 21, "created": 17}, "...": {} },
  "items": [
    { "id": "W-0007", "class": "wall", "action": "modified", "changes": {"axis_shift_m": 0.06, "thickness": [0.15, 0.12]} },
    { "id": null, "class": "wall", "action": "created", "revit_id": 512345, "axis": [[1,2],[3,2]], "thickness": 0.10 }
  ]
}
```

La **tasa de corrección** se calcula como `(modified + deleted + created) / (total_auto + created)`.

## Después del MVP

- Parámetros compartidos `Spybee_Id`, `Spybee_Confianza`, `Spybee_Estado` y un filtro de vista en lugar de overrides por elemento.
- Un panel acoplable "Revisar" con la lista ordenada por confianza, que haga zoom al elemento y lo marque como corregido.
- Plantilla `.rte` de Spybee con los tipos reales de operaciones, y mapeo automático de espesor y material al tipo real.
- Separar `ModelBuilder` sin UI para empaquetarlo en **APS Design Automation** (Revit en la nube).
