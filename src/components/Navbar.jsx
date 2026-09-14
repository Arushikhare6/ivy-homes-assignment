import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import LoginModal from './LoginModal';
import { Home, Building2, Key, Bookmark, BarChart3, LogOut, User, ShieldAlert } from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab }) => {
  const { user, logout, isAuthenticated } = useAuth();
  const [showLoginModal, setShowLoginModal] = useState(false);

  return (
    <>
      <nav className="navbar">
        <div className="nav-brand">
          <Building2 size={28} className="text-indigo-400" />
          <span>Ivy Homes</span>
          <span className="badge badge-live" style={{ fontSize: '0.7rem' }}>Chennai</span>
        </div>

        <div className="nav-links">
          <button
            className={`nav-item ${activeTab === 'listings' ? 'active' : ''}`}
            onClick={() => setActiveTab('listings')}
          >
            <Home size={18} style={{ marginRight: '6px', verticalAlign: 'middle' }} />
            Listings
          </button>
          <button
            className={`nav-item ${activeTab === 'rentals' ? 'active' : ''}`}
            onClick={() => setActiveTab('rentals')}
          >
            <Key size={18} style={{ marginRight: '6px', verticalAlign: 'middle' }} />
            Rentals
          </button>
          <button
            className={`nav-item ${activeTab === 'projects' ? 'active' : ''}`}
            onClick={() => setActiveTab('projects')}
          >
            <Building2 size={18} style={{ marginRight: '6px', verticalAlign: 'middle' }} />
            Projects
          </button>
          <button
            className={`nav-item ${activeTab === 'favourites' ? 'active' : ''}`}
            onClick={() => setActiveTab('favourites')}
          >
            <Bookmark size={18} style={{ marginRight: '6px', verticalAlign: 'middle' }} />
            Saved
          </button>
          <button
            className={`nav-item ${activeTab === 'insights' ? 'active' : ''}`}
            onClick={() => setActiveTab('insights')}
          >
            <BarChart3 size={18} style={{ marginRight: '6px', verticalAlign: 'middle' }} />
            Insights & Audit
          </button>
        </div>

        <div>
          {isAuthenticated ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#cbd5e1', fontSize: '0.9rem' }}>
                <User size={18} />
                <span>{user.email}</span>
              </div>
              <button className="btn btn-secondary" onClick={logout}>
                <LogOut size={16} /> Logout
              </button>
            </div>
          ) : (
            <button className="btn btn-primary" onClick={() => setShowLoginModal(true)}>
              <User size={16} /> Log In
            </button>
          )}
        </div>
      </nav>

      {showLoginModal && <LoginModal onClose={() => setShowLoginModal(false)} />}
    </>
  );
};

export default Navbar;
