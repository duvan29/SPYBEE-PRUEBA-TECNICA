"use client";
import React, { useState, useEffect } from 'react';
import styles from './ProjectList.module.css';
import Image from 'next/image';
import { formatDate } from '@/utils/formateDate';
import { images } from '@/utils/images';
import { useSelectedProjects } from '@/app/hook/SelectedProjectsContext';


const ProjectList = ({ currentItems, handlePageChange, projects, currentPage, itemsPerPage }) => {

    const { selectedProjects, handleAddProject } = useSelectedProjects();

    const getImageByTitle = (title) => {
        const projectNumber = title.split('-')[1];
        return images[projectNumber % images.length];
    };

    const translateStatus = (status) => {
        switch (status) {
            case 'suspended':
                return 'Suspendido';
            case 'active':
                return 'Activo';
            case 'inactive':
                return 'Inactivo';
            case 'pending_payment':
                return 'Pendiente de pago';
            default:
                return status;
        }
    };

    const countItems = (project, itemType) => {
        return project.incidents.filter(incident => incident.item === itemType).length;
    };


    return (
        <div className={styles.row}>
            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>Proyecto</th>
                        <th className={styles.hideOnSmall}>Plan</th>
                        <th>Estado</th>
                        <th className={styles.hideOnSmall}>Equipo</th>
                        <th>Items por vencer</th>
                    </tr>
                </thead>
                <tbody>
                    {currentItems.map((project, index) => {
                        const isSelected = selectedProjects && selectedProjects.includes(project); // Verifica si `selectedProjects` no es `undefined` y si el proyecto está seleccionado
                        return (
                            <tr key={index}
                                style={{
                                    cursor: handleAddProject ? 'pointer' : 'default', // Cambiar el cursor si la función está presente
                                    borderLeft: isSelected ? '2px solid #bf4904' : 'none', // Borde rojo en el lado izquierdo si el proyecto está seleccionado
                                }}
                                onClick={() => handleAddProject(project)} // Agregar el proyecto si la función está presente
                            >
                                <td>
                                    <div className={styles.flexContainer}>
                                        <div className={styles.imageContainer}>
                                            <div className={styles.imageContainer}>
                                                <div className={styles.imageContainer}>
                                                    <Image
                                                        src={getImageByTitle(project.title)}
                                                        alt="logo"
                                                        width={50}
                                                        height={50}
                                                        style={{ maxWidth: "100%", maxHeight: "100%", height: "auto", width: "auto" }}
                                                    />
                                                </div>

                                            </div>
                                        </div>
                                        <div>
                                            <h4>{project.title}</h4>
                                            <p className={styles.infoContainer}>
                                                <div className={styles.infoRow}>
                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className={styles.icon}>
                                                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                                    </svg>
                                                    <span>{formatDate(project.lastVisit)}</span>
                                                </div>
                                                <div className={styles.infoRow}>
                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className={styles.icon}>
                                                        <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                                                    </svg>
                                                    <span>{formatDate(project.lastUpdated)}</span>
                                                </div>
                                            </p>

                                        </div>
                                    </div>
                                </td>
                                <td className={(project.projectPlanData.plan === "big" ? styles.bigPlan : styles.smallPlan) + " " + styles.hideOnSmall}>
                                    <p>
                                        {project.projectPlanData.plan === 'big' ? 'Grande' : 'Pequeño'}
                                    </p>
                                </td>
                                <td className={styles[project.status]}>
                                    <p>
                                        {translateStatus(project.status)}
                                    </p>
                                </td>
                                <td className={styles.hideOnSmall}>
                                    <div className={styles.flexContainerHexagons}>
                                        {project.users.slice(0, 3).map((user, index) => (
                                            <div key={index} className={`${styles.hexagon} ${styles[`hexagon-${index + 1}`]}`}>
                                                {`${user.name.charAt(0)}${user.lastName.charAt(0)}`}
                                            </div>
                                        ))}
                                        {project.users.length > 3 && (
                                            <div className={`${styles.hexagon} ${styles.hexagon4}`}>
                                                {`+${project.users.length - 3}`}
                                            </div>
                                        )}
                                    </div>
                                </td>
                                <td>
                                    <div className={styles.flexContainerItems}>
                                        <div className={styles.item}>
                                            <span className={styles.itemCount}>{countItems(project, 'incidents')}</span>
                                            <span className={styles.itemTitle}>Incidencias</span>
                                        </div>
                                        <div className={styles.item}>
                                            <span className={styles.itemCount}>{countItems(project, 'RFI')}</span>
                                            <span className={styles.itemTitle}>RFI</span>
                                        </div>
                                        <div className={styles.item}>
                                            <span className={styles.itemCount}>{countItems(project, 'task')}</span>
                                            <span className={styles.itemTitle}>Tareas</span>
                                        </div>
                                    </div>
                                </td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
            <div className={styles.pagination}>
                <div className={styles.inlineButtons}>
                    {Array.from({ length: Math.ceil(projects.length / itemsPerPage) }, (_, index) => (
                        <button
                            key={index}
                            className={`${styles.iconButton} ${currentPage === index + 1 ? styles.active : ''}`}
                            onClick={() => handlePageChange(index + 1)}
                        >
                            {index + 1}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ProjectList;