// SummaryComponent.js
import React from "react";
import styles from "./SummaryComponent.module.css";  // Importa el archivo de estilos
import { CircularProgressbar } from "react-circular-progressbar";
import 'react-circular-progressbar/dist/styles.css';  // Importa el estilo predeterminado

const SummaryComponent = ({ projects }) => {

    const countTotalItems = (projects, itemType) => {
        return projects.reduce((total, project) => {
            return total + project.incidents.filter(incident => incident.item === itemType).length;
        }, 0);
    };

    const countOpenItems = (projects, itemType) => {
        return projects.reduce((total, project) => {
            return total + project.incidents.filter(incident => incident.item === itemType && incident.status === "active").length;
        }, 0);
    };

    // Contar el total y abierto de todos los tipos
    const totalIncidencias = countTotalItems(projects, 'incidents');
    const totalRFI = countTotalItems(projects, 'RFI');
    const totalTareas = countTotalItems(projects, 'task');

    const openIncidencias = countOpenItems(projects, 'incidents');
    const openRFI = countOpenItems(projects, 'RFI');
    const openTareas = countOpenItems(projects, 'task');

    const getPercentage = (total, open) => {
        return total > 0 ? Math.round((open / total) * 100) : 0;
    };

    const getExpiringIncidents = (projects, daysUntilExpiration = 7) => {
        const currentDate = new Date();
        const expirationThreshold = new Date(currentDate.getTime() + daysUntilExpiration * 24 * 60 * 60 * 1000); // Fecha límite dentro de 7 días

        // Filtra los incidentes de todos los proyectos cuya fecha límite está dentro de los próximos 'daysUntilExpiration' días
        const expiringIncidents = projects.flatMap((project) =>
            project.incidents.filter((incident) => {
                const limitDate = new Date(incident.limitDate);
                return limitDate > currentDate && limitDate <= expirationThreshold;
            })
        );

        return expiringIncidents;
    };

    // Obtener los incidentes próximos a vencer
    const expiringIncidents = getExpiringIncidents(projects);



    return (
        <div className={styles.container}>
            <h3 className={styles.heading}>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className={styles.icon}>
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
                </svg>
                Resumen
            </h3>
            <div className={styles.buttons}>
                <div className={styles.buttons2}>
                    <button className={styles.buttonG}>
                        General
                    </button>
                    <button className={styles.button}>
                        Mis actulizaciones
                    </button>
                </div>
                <button className={styles.button}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className={styles.icon}>
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z" />
                    </svg>
                    Filtros
                </button>
            </div>
            <section className={styles.section}>
                <div>
                    <h4 className={styles.sectionHeader}>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className={styles.icon}>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>
                        Próximo a vencer</h4>
                    <p className={styles.sectionLink}>Ver todos</p>
                </div>
                <div className={styles.container2}>
                    <div className={styles.section}>
                        <h3 className={styles.title}>Incidencias <span className={styles.count}>{totalIncidencias}</span></h3>
                        <h3 className={styles.title2}>Total Abiertas</h3>
                        <div className={styles.chart}>
                            <CircularProgressbar
                                value={getPercentage(totalIncidencias, openIncidencias)}
                                text={`${openIncidencias}`}
                                styles={{
                                    path: { stroke: '#ff6347' },
                                    trail: { stroke: '#a0a0a0' },
                                    text: { fill: '#a0a0a0', fontSize: '30px' }
                                }}
                                strokeWidth={10}  // Esto ajusta el grosor del trazo
                            />
                        </div>
                    </div>

                    <div className={styles.section}>
                        <h3 className={styles.title}>RFI <span className={styles.count}>{totalRFI}</span></h3>
                        <h3 className={styles.title2}>Total Abiertos</h3>
                        <div className={styles.chart}>
                            <CircularProgressbar
                                value={getPercentage(totalRFI, openRFI)}
                                text={`${openRFI}`}
                                styles={{
                                    path: { stroke: '#ff6347' },
                                    trail: { stroke: '#a0a0a0' },
                                    text: { fill: '#a0a0a0', fontSize: '30px' }
                                }}
                                className={styles.chartSize}
                                strokeWidth={10}  // Esto ajusta el grosor del trazo
                            />
                        </div>
                    </div>

                    <div className={styles.section}>
                        <h3 className={styles.title}>Tareas <span className={styles.count}>{totalTareas}</span></h3>
                        <h3 className={styles.title2}>Total Abiertas</h3>
                        <div className={styles.chart}>
                            <CircularProgressbar
                                value={getPercentage(totalTareas, openTareas)}
                                text={`${openTareas}`}
                                styles={{
                                    path: { stroke: '#ff6347' },
                                    trail: { stroke: '#a0a0a0' },
                                    text: { fill: '#a0a0a0', fontSize: '30px' }
                                }}
                                strokeWidth={10}  // Esto ajusta el grosor del trazo
                            />
                        </div>
                    </div>
                </div>

                <div>
                    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "20px", }}>
                        <thead>
                            <tr
                                style={{
                                    backgroundColor: "#f5f5f5",
                                    borderTopLeftRadius: "10px",
                                    borderTopRightRadius: "10px",
                                    textAlign: "left",
                                    padding: "10px",
                                    boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)", // Sombra sutil en la cabecera
                                }}
                            >
                                <th style={{ padding: "10px 12px", textAlign: "left", fontWeight: "bold" }}>Proyecto</th>
                                <th style={{ padding: "10px 12px", textAlign: "left", fontWeight: "bold" }}>Item</th>
                                <th style={{
                                    padding: "10px 12px", textAlign: "left", fontWeight: "bold", whiteSpace: "nowrap"  // Evitar el wrap
                                }}>Fecha Limite</th>
                            </tr>
                        </thead>
                        <tbody>
                            {expiringIncidents.map((incident) => (
                                <tr style={{ borderBottom: '1px solid #e0e0e0', backgroundColor: '#fff' }} key={incident._id}>
                                    <td className={styles.projectName} style={{ padding: "8px", verticalAlign: "top" }}>
                                        <span style={{ fontSize: "18px", color: "#000" }}>
                                            {incident.owner}
                                        </span>
                                        <span style={{ fontSize: "12px", color: "#666" }}>
                                            {incident.description}
                                        </span>
                                    </td>
                                    <td style={{ padding: "8px", verticalAlign: "top", fontSize: "15px" }}>{incident.item}</td>
                                    <td style={{ padding: "8px", verticalAlign: "top" }}>
                                        <div style={{ marginBottom: "5px" }}>
                                            {/* Fecha */}
                                            {new Date(incident.limitDate).toLocaleDateString("es-CO", {
                                                day: "2-digit",
                                                month: "2-digit",
                                                year: "numeric",
                                            })}
                                        </div>
                                        <div style={{ display: "flex", alignItems: "center", justifyContent: "flex-start" }}>
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className={styles.iconS}>
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                            </svg>
                                            {new Date(incident.limitDate).toLocaleTimeString("es-CO", {
                                                hour: "2-digit",
                                                minute: "2-digit",
                                                hour12: false, // Formato 24 horas
                                            })}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                </div>
                <section className={styles.section}>
                    <div>
                        <h4 className={styles.sectionHeader}>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className={styles.icon}>
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z" />
                            </svg>

                            Próximo eventos</h4>
                        <p className={styles.sectionLink}>Ver todos</p>
                    </div>
                    <div>
                        <table style={{ width: "100%", borderCollapse: "collapse" }}>
                            <thead>
                                <tr
                                    style={{
                                        backgroundColor: "#f5f5f5",
                                        borderTopLeftRadius: "10px",
                                        borderTopRightRadius: "10px",
                                        textAlign: "left",
                                        padding: "10px",
                                        boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)", // Sombra sutil en la cabecera
                                    }}
                                >
                                    <th style={{ padding: "10px 12px", textAlign: "left", fontWeight: "bold" }}>Proyecto</th>
                                    <th style={{ padding: "10px 12px", textAlign: "left", fontWeight: "bold" }}>Equipo</th>
                                    <th style={{
                                        padding: "10px 12px", textAlign: "left", fontWeight: "bold", whiteSpace: "nowrap"  // Evitar el wrap
                                    }}>Fecha Limite</th>
                                </tr>
                            </thead>
                            <tbody>
                                {projects.slice(0, 5).map((incident) => (
                                    <tr style={{ borderBottom: '1px solid #e0e0e0', backgroundColor: '#fff' }} key={incident._id}>
                                        <td className={styles.projectName} style={{ padding: "8px", verticalAlign: "top" }}>
                                            <span style={{ fontSize: "18px", color: "#000" }}>
                                                {incident.title}
                                            </span>
                                            <span style={{ fontSize: "12px", color: "#666" }}>
                                                {incident.city}
                                            </span>
                                        </td>
                                        <td >
                                            <div className={styles.flexContainerHexagons}>
                                                {incident.users.slice(0, 2).map((user, index) => (
                                                    <div key={index} className={`${styles.hexagon} ${styles[`hexagon-${index + 1}`]}`}>
                                                        {`${user.name.charAt(0)}${user.lastName.charAt(0)}`}
                                                    </div>
                                                ))}
                                                {incident.users.length > 2 && (
                                                    <div className={`${styles.hexagon} ${styles.hexagon3}`}>
                                                        {`+${incident.users.length - 2}`}
                                                    </div>
                                                )}
                                            </div>
                                        </td>
                                        <td style={{ padding: "8px", verticalAlign: "top" }}>
                                            <div style={{ marginBottom: "5px" }}>
                                                {/* Fecha */}
                                                {new Date(incident.lastUpdated).toLocaleDateString("es-CO", {
                                                    day: "2-digit",
                                                    month: "2-digit",
                                                    year: "numeric",
                                                })}
                                            </div>
                                            <div style={{ display: "flex", alignItems: "center", flexDirection: "row", justifyContent: "flex-start" }}>
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className={styles.iconS}>
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                                </svg>
                                                <span>
                                                    {new Date(incident.lastUpdated).toLocaleTimeString("es-CO", {
                                                        hour: "2-digit",
                                                        minute: "2-digit",
                                                        hour12: false, // Formato 24 horas
                                                    })}
                                                </span>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                    </div>
                </section>

            </section>
        </div>
    );
};

export default SummaryComponent;
