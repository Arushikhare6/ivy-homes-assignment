import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';

const FavouritesContext = createContext();

export const FavouritesProvider = ({ children }) => {
  const { user } = useAuth();
  const [favourites, setFavourites] = useState([]);

  const userEmail = user?.email || 'guest';
  const storageKey = `ivy_favourites_${userEmail}`;

  useEffect(() => {
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        setFavourites(JSON.parse(saved));
      } else {
        setFavourites([]);
      }
    } catch (e) {
      setFavourites([]);
    }
  }, [userEmail]);

  const toggleFavourite = (listing) => {
    setFavourites((prev) => {
      const exists = prev.some((item) => item.listing_id === listing.listing_id);
      let updated;
      if (exists) {
        updated = prev.filter((item) => item.listing_id !== listing.listing_id);
      } else {
        updated = [...prev, listing];
      }
      localStorage.setItem(storageKey, JSON.stringify(updated));
      return updated;
    });
  };

  const isFavourite = (listingId) => {
    return favourites.some((item) => item.listing_id === listingId);
  };

  return (
    <FavouritesContext.Provider value={{ favourites, toggleFavourite, isFavourite }}>
      {children}
    </FavouritesContext.Provider>
  );
};

export const useFavourites = () => useContext(FavouritesContext);
