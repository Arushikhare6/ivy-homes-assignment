import React, { useState } from 'react';
import { useFavourites } from '../context/FavouritesContext';
import { useAuth } from '../context/AuthContext';
import ListingCard from '../components/ListingCard';
import ListingDetailPage from './ListingDetailPage';
import { Bookmark, Heart, AlertCircle } from 'lucide-react';

const FavouritesPage = () => {
  const { favourites } = useFavourites();
  const { user } = useAuth();
  const [selectedListing, setSelectedListing] = useState(null);

  if (selectedListing) {
    return <ListingDetailPage listingId={selectedListing.listing_id} onBack={() => setSelectedListing(null)} />;
  }

  return (
    <div className="container">
      <div style={{ marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: '800' }} className="text-gradient">
          Saved Listings ({favourites.length})
        </h1>
        <p className="text-muted" style={{ fontSize: '0.95rem' }}>
          Personalized list saved for {user ? user.email : 'guest user'}. Persisted across page refreshes and re-logins.
        </p>
      </div>

      {/* Doc Lie Audit Notice */}
      <div className="glass-card" style={{ padding: '1rem 1.25rem', marginBottom: '1.5rem', background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.25)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <AlertCircle size={20} className="text-rose-400" />
        <div style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>
          <strong style={{ color: '#f87171' }}>API Audit Note:</strong> The documented server endpoints <code style={{ color: '#a5b4fc' }}>/v1/favourites</code> return HTTP 404 Not Found. This frontend automatically persists your saved listings client-side per logged-in demo user.
        </div>
      </div>

      {favourites.length === 0 ? (
        <div className="glass-card" style={{ padding: '4rem', textAlign: 'center', maxWidth: '500px', margin: '2rem auto' }}>
          <Heart size={48} style={{ color: '#64748b', marginBottom: '1rem' }} />
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '0.5rem' }}>No Saved Listings Yet</h3>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
            Click the bookmark icon on any property card to save it to your account.
          </p>
        </div>
      ) : (
        <div className="grid-3">
          {favourites.map((l) => (
            <ListingCard key={l.listing_id} listing={l} onSelect={(item) => setSelectedListing(item)} />
          ))}
        </div>
      )}
    </div>
  );
};

export default FavouritesPage;
