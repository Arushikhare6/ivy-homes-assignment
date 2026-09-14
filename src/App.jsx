import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { FavouritesProvider } from './context/FavouritesContext';
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import ListingsPage from './pages/ListingsPage';
import RentalsPage from './pages/RentalsPage';
import ProjectsPage from './pages/ProjectsPage';
import FavouritesPage from './pages/FavouritesPage';
import InsightsPage from './pages/InsightsPage';

const MainAppContent = () => {
  const { isAuthenticated, loading } = useAuth();
  const [activeTab, setActiveTab] = useState('listings');

  useEffect(() => {
    const handleHash = () => {
      const hash = window.location.hash.replace('#', '');
      if (['listings', 'rentals', 'projects', 'favourites', 'insights'].includes(hash)) {
        setActiveTab(hash);
      }
    };
    handleHash();
    window.addEventListener('hashchange', handleHash);
    return () => window.removeEventListener('hashchange', handleHash);
  }, []);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    window.location.hash = tab;
  };

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#94a3b8' }}>
        <div className="spin" style={{ display: 'inline-block', width: '40px', height: '40px', border: '3px solid rgba(99, 102, 241, 0.3)', borderTopColor: '#6366f1', borderRadius: '50%' }}></div>
      </div>
    );
  }

  // Strict Auth Gate: Render Login Page if not authenticated
  if (!isAuthenticated) {
    return <LoginPage />;
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar activeTab={activeTab} setActiveTab={handleTabChange} />

      <main style={{ flex: 1, paddingBottom: '3rem' }}>
        {activeTab === 'listings' && <ListingsPage />}
        {activeTab === 'rentals' && <RentalsPage />}
        {activeTab === 'projects' && <ProjectsPage />}
        {activeTab === 'favourites' && <FavouritesPage />}
        {activeTab === 'insights' && <InsightsPage />}
      </main>

      <footer style={{ borderTop: '1px solid rgba(255, 255, 255, 0.08)', padding: '1.5rem', textAlign: 'center', color: '#64748b', fontSize: '0.85rem' }}>
        Ivy Homes Property API Audit & Frontend Application • Software Engineering Internship September 2026
      </footer>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <FavouritesProvider>
        <MainAppContent />
      </FavouritesProvider>
    </AuthProvider>
  );
}

export default App;
