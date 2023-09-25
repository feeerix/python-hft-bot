// React Import
import React, { useState, useEffect } from 'react';

import Head from 'next/head'
import { NextUIProvider, createTheme, useTheme, changeTheme } from '@nextui-org/react';
import TopNavbar from './components/TopNavbar';


const link_list = [
  { href: "/", label: "Home" },
  { href: "/price", label: "Price" },
  { href: "/Backtest", label: "Backtest" },
]

const Home: React.FC = ({}) => {
      // Themes
      const lightTheme = createTheme({
        type: 'dark',
        theme: {
        colors: {}, // optional
        }
    })

    const darkTheme = createTheme({
        type: 'dark',
        theme: {
        colors: {}, // optional
        }
    })

    const theme = useTheme();
    const [isDarkMode, setIsDarkMode] = useState(true);
    
    const handleToggleDarkMode = () => {
        setIsDarkMode(!isDarkMode);
        changeTheme(isDarkMode ? 'light' : 'dark');
    };

  return (
    <>
      <Head>
        <title>Test</title>

      </Head>
      <main>
        
        <TopNavbar 
          links={link_list}
          isDarkMode={isDarkMode}
          handleToggleDarkMode={handleToggleDarkMode}
        />
      
      </main>
    </>
  )
}

export default Home