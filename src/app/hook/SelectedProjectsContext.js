"use client";
import React, { createContext, useState, useContext } from 'react';

// Crear el contexto
const SelectedProjectsContext = createContext();

// Crear el proveedor
export const SelectedProjectsProvider = ({ children }) => {
    const [selectedProjects, setSelectedProjects] = useState([]);

    // Función para agregar o eliminar un proyecto de los seleccionados
    const handleAddProject = (project) => {
        setSelectedProjects((prevSelectedProjects) => {
            if (prevSelectedProjects.includes(project)) {
                // Si el proyecto ya está seleccionado, eliminarlo
                return prevSelectedProjects.filter((p) => p !== project);
            }
            // Si el proyecto no está seleccionado, agregarlo
            return [...prevSelectedProjects, project];
        });
    };

    return (
        <SelectedProjectsContext.Provider value={{ selectedProjects, handleAddProject }}>
            {children}
        </SelectedProjectsContext.Provider>
    );
};

// Crear un hook para acceder al contexto fácilmente
export const useSelectedProjects = () => {
    const context = useContext(SelectedProjectsContext);
    if (!context) {
        throw new Error('useSelectedProjects debe ser usado dentro de un SelectedProjectsProvider');
    }
    return context;
};
