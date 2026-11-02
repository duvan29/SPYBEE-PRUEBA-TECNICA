# Carpeta de datos

Nada de esta carpeta se sube a git, salvo este archivo.

```
data/
├── raw/<proyecto>/         Nube ORIGINAL tal como la entregó el scan leader. SOLO LECTURA.
│   ├── *.e57 | *.las | *.laz
│   ├── control_points.csv  (opcional) id,este,norte,cota,metodo,precision
│   └── info.yaml           (opcional) metadatos del formulario de entrega
├── reference/<proyecto>/   Modelo hecho a mano del mismo edificio (para evaluar)
│   ├── modelo_manual.rvt
│   └── modelo_manual.ifc   (exportado desde Revit)
├── work/<proyecto>/        Intermedios generados por el pipeline (se pueden borrar y regenerar)
│   ├── cloud_1cm.laz
│   ├── normals.npz
│   └── floors/F01.laz, F02.laz, ...
└── out/<proyecto>/         Resultados
    ├── ficha.md            Ficha de la nube
    ├── building.json       Modelo intermedio
    ├── model.ifc           IFC4
    ├── cloud_local.las     Nube diezmada en coordenadas locales (para vincular en Revit)
    ├── qa.html             Reporte de calidad
    ├── eval.json           Métricas contra la referencia
    └── debug/<etapa>/*.png Imágenes de verificación
```

`<proyecto>` va en minúsculas, sin espacios ni tildes. Ejemplo: `torre-norte`.

Ejemplo de `info.yaml`:

```yaml
nombre: Torre Norte
direccion: Calle 100 # 10-20, Bogotá
pisos: 6
altura_piso_a_piso_m: 2.6
uso: vivienda            # vivienda | oficinas | comercial | industrial | otro
estado: obra_gris        # obra_gris | acabados | ocupado
escaner: XGRIDS L2 Pro
software_registro: LixelStudio
crs: EPSG:9377           # o "local" si no está georreferenciada
cotas: ortometricas      # ortometricas | elipsoidales | locales
fecha_captura: 2026-10-28
lod_pedido: 200
```
