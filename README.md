# Proyecto de Listado de Proyectos con Mapbox-GL y Funcionalidad de Búsqueda

Este repositorio contiene una solución que implementa un sistema de visualización y filtrado de proyectos usando **ReactJS**, **NextJS**, **Zustand**, **Mapbox-GL** y **CSS modules**. La aplicación tiene un listado paginado de proyectos que se puede filtrar y buscar, con un mapa interactivo que muestra los marcadores de las ubicaciones de los proyectos.

## Objetivo

El objetivo es crear una interfaz que permita ver, buscar, y filtrar proyectos, así como navegar a la ubicación de cada proyecto en un mapa interactivo. Para ello, se utilizó un JSON con los detalles de los proyectos.

## Funcionalidades

### 1. Listado de proyectos:
- Se crea un listado paginado de proyectos. Cada proyecto muestra su nombre, plan, estado, equipo y el número de ítems por vencer (incidentes, RFI y tareas).
- La tabla de proyectos está paginada y muestra solo 10 elementos por página.

### 2. Búsqueda:
- Se implementa un campo de búsqueda (input) que permite filtrar los proyectos por nombre, cantidad de incidencias, RFI y tareas.

### 3. Filtrado de resultados:
- Los proyectos se pueden ordenar alfabéticamente o por la cantidad de incidencias, RFI o tareas.

### 4. Mapa interactivo con Mapbox-GL:
- Se utiliza **Mapbox-GL** para mostrar un mapa con marcadores en las ubicaciones de los proyectos, cuyas coordenadas son proporcionadas en el JSON.
- Al hacer clic en un proyecto de la tabla, el mapa navega hacia la ubicación de ese proyecto.