import FiltersSection from '@/components/FiltersSection/FiltersSection';
import NavBar from '@/components/NavBar/NavBar';
import ProjectList from '@/components/ProjectList/ProjectList';
import React from 'react';

const Home = () => {
  return (
    <div>
      <NavBar />
      <main >
        <section className="project-list-section">
          <FiltersSection />
        </section>
      </main>
    </div>
  );
};

export default Home;