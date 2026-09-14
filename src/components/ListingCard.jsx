import React from 'react';
import { useFavourites } from '../context/FavouritesContext';
import { formatCurrency, isListingCorrupt, isListingFake } from '../services/api';
import { Bookmark, MapPin, Bed, Bath, Maximize2, Layers, AlertTriangle, ShieldCheck, Phone } from 'lucide-react';

const ListingCard = ({ listing, onSelect, allListings = [] }) => {
  const { isFavourite, toggleFavourite } = useFavourites();

  const corrupt = isListingCorrupt(listing);
  const fake = isListingFake(listing, allListings);
  const favorited = isFavourite(listing.listing_id);

  const pricePerSqft = listing.price && listing.carpet_area && listing.carpet_area > 0
    ? Math.round(listing.price / listing.carpet_area)
    : null;

  return (
    <div className="glass-card" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', position: 'relative' }}>
      <div>
        {/* Header Badges */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
          <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
            {listing.is_live ? (
              <span className="badge badge-live">Active</span>
            ) : (
              <span className="badge badge-inactive">Withdrawn</span>
            )}

            {corrupt && <span className="badge badge-corrupt" title="Corrupt data attributes"><AlertTriangle size={12} /> Corrupt Data</span>}
            {fake && <span className="badge badge-fake" title="Non-genuine / Lead-gen listing"><AlertTriangle size={12} /> Lead-Gen</span>}
            {listing.is_verified && <span className="badge badge-live" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#818cf8', borderColor: 'rgba(99, 102, 241, 0.3)' }}><ShieldCheck size={12} /> Verified</span>}
          </div>

          <button
            onClick={(e) => {
              e.stopPropagation();
              toggleFavourite(listing);
            }}
            style={{
              background: favorited ? 'rgba(239, 68, 68, 0.2)' : 'rgba(255, 255, 255, 0.05)',
              border: '1px solid ' + (favorited ? 'rgba(239, 68, 68, 0.4)' : 'var(--border-color)'),
              color: favorited ? '#ef4444' : '#94a3b8',
              borderRadius: '50%',
              width: '36px',
              height: '36px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            <Bookmark size={18} fill={favorited ? '#ef4444' : 'none'} />
          </button>
        </div>

        {/* Title & Apartment */}
        <h3
          onClick={() => onSelect && onSelect(listing)}
          style={{ fontSize: '1.15rem', fontWeight: '700', color: '#f8fafc', cursor: 'pointer', marginBottom: '0.4rem', lineHeight: '1.3' }}
        >
          {listing.apartment_name || listing.title || 'Independent Property'}
        </h3>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#94a3b8', fontSize: '0.85rem', marginBottom: '1rem', textTransform: 'capitalize' }}>
          <MapPin size={14} style={{ color: '#818cf8' }} />
          <span>{listing.locality}, Chennai</span>
        </div>

        {/* Price & Price/sqft */}
        <div style={{ marginBottom: '1rem' }}>
          <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#818cf8' }}>
            {formatCurrency(listing.price)}
          </div>
          {pricePerSqft && (
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
              ₹{pricePerSqft.toLocaleString('en-IN')}/sq.ft. (Carpet Area)
            </div>
          )}
        </div>

        {/* Property Features */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem', background: 'rgba(15, 23, 42, 0.5)', padding: '0.6rem', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.8rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: '#cbd5e1' }}>
            <Bed size={14} style={{ color: '#94a3b8' }} />
            <span>{listing.bedroom || 0} BHK</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: '#cbd5e1' }}>
            <Bath size={14} style={{ color: '#94a3b8' }} />
            <span>{listing.bathroom || 0} Bath</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: '#cbd5e1' }}>
            <Maximize2 size={14} style={{ color: '#94a3b8' }} />
            <span>{listing.carpet_area || 0} sqft</span>
          </div>
        </div>
      </div>

      {/* Footer Info */}
      <div style={{ paddingTop: '0.75rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8rem', color: '#94a3b8' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
          <Phone size={12} />
          <span>{listing.posted_by_name || listing.posted_by || 'Seller'}</span>
        </div>
        <button
          onClick={() => onSelect && onSelect(listing)}
          className="btn btn-secondary"
          style={{ padding: '0.3rem 0.75rem', fontSize: '0.75rem' }}
        >
          View Details
        </button>
      </div>
    </div>
  );
};

export default ListingCard;
