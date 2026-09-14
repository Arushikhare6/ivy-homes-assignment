import React, { useState, useEffect } from 'react';
import { fetchSingleListing, formatCurrency, isListingCorrupt, isListingFake } from '../services/api';
import { useFavourites } from '../context/FavouritesContext';
import { ArrowLeft, MapPin, Bed, Bath, Maximize2, Layers, Bookmark, Phone, User, ShieldCheck, AlertTriangle, ExternalLink } from 'lucide-react';

const ListingDetailPage = ({ listingId, onBack, allListings = [] }) => {
  const [listing, setListing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { isFavourite, toggleFavourite } = useFavourites();

  useEffect(() => {
    loadListing();
  }, [listingId]);

  const loadListing = async () => {
    setLoading(true);
    setError(null);
    try {
      // Doc Lie: GET /v1/listing/{id} is 404, working endpoint is /v1/listings/{id}
      const data = await fetchSingleListing(listingId);
      setListing(data);
    } catch (err) {
      setError(err.message || 'Failed to load listing details');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '4rem' }}>
        <div className="spin" style={{ display: 'inline-block', width: '40px', height: '40px', border: '3px solid rgba(99, 102, 241, 0.3)', borderTopColor: '#6366f1', borderRadius: '50%' }}></div>
        <p style={{ marginTop: '1rem', color: '#94a3b8' }}>Loading property details for {listingId}...</p>
      </div>
    );
  }

  if (error || !listing) {
    return (
      <div className="container">
        <button className="btn btn-secondary" onClick={onBack} style={{ marginBottom: '1rem' }}>
          <ArrowLeft size={16} /> Back to Listings
        </button>
        <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', color: '#f87171', padding: '1.5rem', borderRadius: '12px' }}>
          <h3>Unable to Load Listing</h3>
          <p>{error || 'Listing not found.'}</p>
        </div>
      </div>
    );
  }

  const corrupt = isListingCorrupt(listing);
  const fake = isListingFake(listing, allListings);
  const favorited = isFavourite(listing.listing_id);

  const pricePerSqft = listing.price && listing.carpet_area && listing.carpet_area > 0
    ? Math.round(listing.price / listing.carpet_area)
    : null;

  return (
    <div className="container" style={{ maxWidth: '900px' }}>
      <button className="btn btn-secondary" onClick={onBack} style={{ marginBottom: '1.5rem' }}>
        <ArrowLeft size={16} /> Back to Listings
      </button>

      <div className="glass-card" style={{ padding: '2rem' }}>
        {/* Header Badges */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {listing.is_live ? (
              <span className="badge badge-live">Active Listing</span>
            ) : (
              <span className="badge badge-inactive">Withdrawn / Inactive</span>
            )}
            {corrupt && <span className="badge badge-corrupt"><AlertTriangle size={14} /> Corrupt Data Attributes</span>}
            {fake && <span className="badge badge-fake"><AlertTriangle size={14} /> Lead-Gen Listing</span>}
            {listing.is_verified && <span className="badge badge-live" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#818cf8', borderColor: 'rgba(99, 102, 241, 0.3)' }}><ShieldCheck size={14} /> Verified</span>}
          </div>

          <button
            className={`btn ${favorited ? 'btn-secondary' : 'btn-primary'}`}
            onClick={() => toggleFavourite(listing)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
          >
            <Bookmark size={16} fill={favorited ? '#ef4444' : 'none'} />
            {favorited ? 'Saved in Favourites' : 'Save Listing'}
          </button>
        </div>

        {/* Title */}
        <h1 style={{ fontSize: '1.8rem', fontWeight: '800', marginBottom: '0.4rem', color: '#f8fafc' }}>
          {listing.apartment_name || listing.title || 'Independent Property'}
        </h1>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#94a3b8', fontSize: '0.95rem', marginBottom: '1.5rem', textTransform: 'capitalize' }}>
          <MapPin size={16} style={{ color: '#818cf8' }} />
          <span>{listing.locality}, Chennai • Website Source: {listing.website || 'Direct'}</span>
        </div>

        {/* Price Section */}
        <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1.25rem', borderRadius: '12px', marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Asking Sale Price</div>
            <div style={{ fontSize: '2rem', fontWeight: '800', color: '#818cf8' }}>
              {formatCurrency(listing.price)}
            </div>
          </div>
          {pricePerSqft && (
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Calculated Rate</div>
              <div style={{ fontSize: '1.2rem', fontWeight: '700', color: '#f8fafc' }}>
                ₹{pricePerSqft.toLocaleString('en-IN')} <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>/ sq.ft.</span>
              </div>
            </div>
          )}
        </div>

        {/* Specifications Grid */}
        <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '1rem', color: '#cbd5e1' }}>Property Specifications</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginBottom: '0.2rem' }}>Bedrooms (BHK)</div>
            <div style={{ fontSize: '1.2rem', fontWeight: '700', color: '#f8fafc' }}>{listing.bedroom || 0} Bedrooms</div>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginBottom: '0.2rem' }}>Bathrooms</div>
            <div style={{ fontSize: '1.2rem', fontWeight: '700', color: '#f8fafc' }}>{listing.bathroom || 0} Bathrooms</div>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginBottom: '0.2rem' }}>Carpet Area</div>
            <div style={{ fontSize: '1.2rem', fontWeight: '700', color: '#f8fafc' }}>{listing.carpet_area || 0} sq.ft.</div>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginBottom: '0.2rem' }}>Super Built-Up Area</div>
            <div style={{ fontSize: '1.2rem', fontWeight: '700', color: '#f8fafc' }}>{listing.super_built_up_area || 'N/A'} sq.ft.</div>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginBottom: '0.2rem' }}>Floor</div>
            <div style={{ fontSize: '1.2rem', fontWeight: '700', color: '#f8fafc' }}>Floor {listing.floor} of {listing.total_floors || 'N/A'}</div>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginBottom: '0.2rem' }}>Furnishing</div>
            <div style={{ fontSize: '1.2rem', fontWeight: '700', color: '#f8fafc', textTransform: 'capitalize' }}>{listing.furnishing || 'N/A'}</div>
          </div>
        </div>

        {/* Description */}
        <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '0.5rem', color: '#cbd5e1' }}>Seller Description</h3>
        <p style={{ color: '#cbd5e1', lineHeight: '1.6', marginBottom: '2rem', background: 'rgba(15, 23, 42, 0.4)', padding: '1rem', borderRadius: '10px' }}>
          {listing.description || 'No description provided.'}
        </p>

        {/* Seller Info & External Link */}
        <div style={{ background: 'rgba(99, 102, 241, 0.08)', border: '1px solid rgba(99, 102, 241, 0.2)', padding: '1.25rem', borderRadius: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ fontSize: '0.8rem', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: '600' }}>Contact Seller</div>
            <div style={{ fontSize: '1.1rem', fontWeight: '700', color: '#f8fafc', marginTop: '0.2rem' }}>
              {listing.posted_by_name || 'Verified Agent'} ({listing.posted_by || 'agent'})
            </div>
            <div style={{ color: '#cbd5e1', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.4rem', marginTop: '0.2rem' }}>
              <Phone size={14} />
              <span>{listing.posted_by_contact || 'N/A'}</span>
            </div>
          </div>

          {listing.listing_url && (
            <a href={listing.listing_url} target="_blank" rel="noreferrer" className="btn btn-primary" style={{ textDecoration: 'none' }}>
              Original Portal Link <ExternalLink size={14} />
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

export default ListingDetailPage;
