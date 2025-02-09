"use client";
import React, { useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import { useSelectedProjects } from "@/app/hook/SelectedProjectsContext";

mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN;

const MapboxGLComponent = () => {
  const { selectedProjects } = useSelectedProjects();
  const projects = selectedProjects;

  const mapContainer = useRef(null);
  const map = useRef(null);

  useEffect(() => {
    if (!mapContainer.current) return;

    // Inicializar el mapa
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/satellite-v9", // Modo satelital
      center: [-74.0817, 4.6097], // Bogotá, Colombia
      zoom: 11, // Ajusta el zoom para que se vea bien la ciudad
      interactive: true, // Aseguramos la interactividad
    });

    // Crear un array para almacenar los marcadores
    const markers = [];

    // Verificar si hay proyectos y si tienen incidentes
    if (projects && projects.length > 0) {
      projects.forEach((project) => {
        if (project.incidents && project.incidents.length > 0) {
          // Iterar sobre los incidentes
          project.incidents.forEach((incident) => {
            // Asegúrate de que las coordenadas existan antes de usarlas
            if (incident.coordinates && incident.coordinates.lng && incident.coordinates.lat) {
              const incidentCoordinates = [incident.coordinates.lng, incident.coordinates.lat]; // Usa las coordenadas del incidente

              const incidentMarker = new mapboxgl.Marker({ color: "red" }) // Marcadores rojos para incidentes
                .setLngLat(incidentCoordinates) // Usar las coordenadas del incidente
                .setPopup(
                  new mapboxgl.Popup().setHTML(`
                    <p>${project.name}</p>
                  `)
                )
                .addTo(map.current);

              markers.push(incidentMarker);
            } else {
              console.warn(`Incidente sin coordenadas válidas: ${incident.description}`);
            }
          });
        } else {
          console.warn(`No incidentes en el proyecto: ${project.name}`);
        }
      });
    } else {
      console.warn("No hay proyectos seleccionados.");
    }

    // Limpiar al desmontar el componente
    return () => map.current.remove();
  }, [projects]);

  return (
    <div
      ref={mapContainer}
      style={{
        width: "100%",      // Se ajusta al 100% del ancho disponible
        height: "300px",    // La altura siempre será de 300px
        overflow: "hidden",
        marginBottom: "10px",
        borderRadius: "15px"
      }}
    />
  );
};

export default MapboxGLComponent;
