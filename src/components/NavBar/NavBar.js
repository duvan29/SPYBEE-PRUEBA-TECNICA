import React from 'react';
import styles from './NavBar.module.css';
import Image from 'next/image';

const NavBar = () => {

    return (
        <nav className={styles.navbar}>
            <div className={styles.logo}>
                <Image src="/logo.webp" alt="Logo" width={120} height={60} layout="intrinsic" />
            </div>
            <div className={styles.adminInfo}>
                <div className={styles.hexagon}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                    </svg>
                </div>
                <div className={styles.adminText}>
                    <span className={styles.name}>Duvan </span>
                    <span className={styles.position}>Administrador</span>
                </div>
                <span className={styles.arrow}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-6 h-6">
                        <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                    </svg>
                </span>
            </div>
        </nav>
    );
};

export default NavBar;