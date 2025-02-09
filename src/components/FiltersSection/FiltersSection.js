"use client";

import React, { useEffect, useState } from 'react';
import styles from './FiltersSection.module.css';
import ProjectList from '../ProjectList/ProjectList';
import MapboxGLComponent from '../Mapbox-GL/Mapbox-GL';
import ContainerSectionMap from '@/app/Map/ContainerSecctionMap';

const FiltersSection = () => {
  const [selectedOption, setSelectedOption] = useState('list');
  const [projects, setProjects] = useState([]);
  const [filteredProjects, setFilteredProjects] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  useEffect(() => {
    fetch('/mock_data.json')
      .then(response => response.json())
      .then(data => {
        setProjects(data);
        setFilteredProjects(data);
      });
  }, []);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredProjects.slice(indexOfFirstItem, indexOfLastItem);

  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = () => {
    const filtered = projects.filter(project =>
      project.title && project.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredProjects(filtered);
    setCurrentPage(1);
  };

  const [isOpen, setIsOpen] = useState(false);
  const [selectedOptionFilter, setSelectedOptionFilter] = useState(null);

  const options = [
    { value: "alphabetical", label: "Orden Alfabético" },
    { value: "incidents", label: "Numero de Incidentes" },
    { value: "RFI", label: "Numero de RFI" },
    { value: "tasks", label: "Numero de Tareas" }
  ];

  const handleSelect = (value) => {
    setSelectedOptionFilter(value);
    handleSort(value);
    setIsOpen(false);
  };

  const handleSort = (sortType) => {
    const sortedProjects = [...filteredProjects]; // Copia del array sin mutarlo

    sortedProjects.sort((a, b) => {
      switch (sortType) {
        case "alphabetical":
          return a.title.localeCompare(b.title, "es", { sensitivity: "base" });

        case "incidents":
          return (b.incidents?.filter(e => e.item === 'incidents').length ?? 0) - (a.incidents?.filter(item => item.item === 'incidents').length ?? 0);

        case "RFI":
          return (b.incidents?.filter(e => e.item === 'RFI').length ?? 0) - (a.incidents?.filter(item => item.item === 'RFI').length ?? 0);

        case "tasks":
          return (b.incidents?.filter(e => e.item === 'task').length ?? 0) - (a.incidents?.filter(item => item.item === 'task').length ?? 0);

        default:
          return 0;
      }
    });
    setFilteredProjects(sortedProjects);
    setCurrentPage(1);
  };




  return (
    <>
      <section className={styles.filtersSection}>
        <div className={styles.title}>
          <h1>Mis Proyectos</h1>
          <span>{filteredProjects.length} proyectos</span>
        </div>
        <div className={styles.buttonsContainer}>

          <div className={styles.dropdownContainer}>
            <button className={`${styles.squareButton} ${isOpen ? styles.active : ''}`} onClick={() => setIsOpen(!isOpen)}>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth="1.5"
                stroke="currentColor"
                className={styles.icon}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75"
                />
              </svg>
            </button>

            {isOpen && (
              <div className={styles.dropdownMenu}>
                {options.map((option) => (
                  <div
                    key={option.value}
                    className={`${styles.dropdownItem} ${selectedOption === option.value ? styles.selected : ""}`}
                    onClick={() => handleSelect(option.value)}
                  >
                    {option.label}
                  </div>
                ))}
              </div>
            )}
          </div>


          <div className={styles.inlineButtons}>
            <button
              className={`${styles.iconButton} ${selectedOption === 'list' ? styles.active : ''}`}
              onClick={() => setSelectedOption('list')}
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
              </svg>
            </button>
            <button
              className={`${styles.iconButton} ${selectedOption === 'block' ? styles.active : ''}`}
              onClick={() => setSelectedOption('block')}
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
              </svg>
            </button>
            <button
              className={`${styles.iconButton} ${selectedOption === 'location' ? styles.active : ''}`}
              onClick={() => setSelectedOption('location')}
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
              </svg>
            </button>
          </div>
          <div className={styles.searchContainer}>
            <input
              type="text"
              placeholder="Buscar proyecto"
              className={styles.searchInput}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <button className={styles.searchButton} onClick={handleSearch}>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
              </svg>
            </button>
          </div>
          <div className={styles.createContainer}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className={styles.plus}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            <span className={styles.createButton}>Crear proyecto</span>
          </div>

        </div>
      </section>
      {selectedOption === 'list' &&
        <ProjectList currentItems={currentItems} currentPage={currentPage} handlePageChange={handlePageChange} projects={filteredProjects} itemsPerPage={itemsPerPage} />
      }
      {selectedOption === 'block' && <ContainerSectionMap currentItems={currentItems} currentPage={currentPage} handlePageChange={handlePageChange} projects={filteredProjects} itemsPerPage={itemsPerPage} />}
      {selectedOption === 'location' && <ContainerSectionMap currentItems={currentItems} currentPage={currentPage} handlePageChange={handlePageChange} projects={filteredProjects} itemsPerPage={itemsPerPage} map={true} />
      }
    </>
  );
};

export default FiltersSection;