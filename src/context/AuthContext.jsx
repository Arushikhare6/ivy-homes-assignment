import React, { createContext, useContext, useState, useEffect } from 'react';
import { getStoredTokens, loginUser, logoutUser, refreshToken } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loginError, setLoginError] = useState(null);

  useEffect(() => {
    const initAuth = () => {
      const tokens = getStoredTokens();
      if (tokens && tokens.user) {
        setUser(tokens.user);
      }
      setLoading(false);
    };

    initAuth();

    // Auto-refresh token every 12 minutes (since 15-minute access token expiry)
    const refreshInterval = setInterval(async () => {
      const tokens = getStoredTokens();
      if (tokens?.refresh_token) {
        try {
          await refreshToken();
        } catch (e) {
          console.error('Silent token refresh failed:', e);
        }
      }
    }, 12 * 60 * 1000);

    return () => clearInterval(refreshInterval);
  }, []);

  const handleLogin = async (email, password) => {
    setLoginError(null);
    try {
      const data = await loginUser(email, password);
      setUser(data.user || { email });
      return true;
    } catch (err) {
      setLoginError(err.message || 'Login failed');
      return false;
    }
  };

  const handleLogout = async () => {
    await logoutUser();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        loginError,
        login: handleLogin,
        logout: handleLogout,
        isAuthenticated: !!user
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
