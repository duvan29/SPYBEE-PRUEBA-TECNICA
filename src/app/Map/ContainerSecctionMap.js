import MapboxGLComponent from '@/components/Mapbox-GL/Mapbox-GL';
import ProjectList from '@/components/ProjectList/ProjectList';
import SummaryComponent from '@/components/SummaryComponent/SummaryComponent';
import styles from './ContainerSectionMap.module.css';

const ContainerSectionMap = ({ currentItems, handlePageChange, projects, currentPage, itemsPerPage, map }) => {

    return (
        <div className={styles.flexWrap}>
            <div id="map">
                {map &&
                    <MapboxGLComponent
                        projects={projects} />
                }
                <ProjectList
                    currentItems={currentItems}
                    currentPage={currentPage}
                    handlePageChange={handlePageChange}
                    projects={projects}
                    itemsPerPage={itemsPerPage}
                />
            </div>
            <div>
                <SummaryComponent
                    projects={projects}
                />
            </div>
        </div>
    );
};

export default ContainerSectionMap;