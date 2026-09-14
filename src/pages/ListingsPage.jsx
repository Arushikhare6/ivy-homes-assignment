import React, { useState, useEffect, useMemo } from 'react';
import { fetchAllListings, isListingCorrupt, isListingFake } from '../services/api';
import ListingCard from '../components/ListingCard';
import ListingDetailPage from './ListingDetailPage';
import { Search, Filter, RefreshCw, AlertCircle, ShieldCheck } from 'lucide-react';

const LOCALITIES = ['All Localities', 't nagar', 'adyar', 'velachery', 'anna nagar', 'porur', 'perungudi', 'thoraipakkam', 'omr', 'tambaram'];
const BHK_OPTIONS = ['All BHKs', '1 BHK', '2 BHK', '3 BHK', '4+ BHK'];
const FURNISHING_OPTIONS = ['All Furnishing', 'unfurnished', 'semi-furnished', 'fully-furnished'];

const ListingsPage = () => {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Selected Listing for Detail Modal / Page
  const [selectedListing, setSelectedListing] = useState(null);

  // Filters State
  const [search, setSearch] = useState('');
  const [locality, setLocality] = useState('All Localities');
  const [bhk, setBhk] = useState('All BHKs');
  const [furnishing, setFurnishing] = useState('All Furnishing');
  const [hideCorruptAndFake, setHideCorruptAndFake] = useState(true);
  const [onlyActive, setOnlyActive] = useState(true);
  const [sortBy, setSortBy] = useState('default');

  // Pagination state
  const [page, setPage] = useState(1);
  const pageSize = 12;

  useEffect(() => {
    loadListings();
  }, []);

  const loadListings = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAllListings();
      setListings(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch listings');
    } finally {
      setLoading(false);
    }
  };

  // Frontend Enforced Filtering
  const filteredListings = useMemo(() => {
    return listings.filter((l) => {
      // 1. Corrupt & Fake Filter
      if (hideCorruptAndFake) {
        if (isListingCorrupt(l) || isListingFake(l, listings)) return false;
      }

      // 2. Active Only Filter
      if (onlyActive && l.is_live !== true) return false;

      // 3. Search query
      if (search.trim()) {
        const q = search.toLowerCase();
        const title = (l.apartment_name || l.title || '').toLowerCase();
        const loc = (l.locality || '').toLowerCase();
        const desc = (l.description || '').toLowerCase();
        if (!title.includes(q) && !loc.includes(q) && !desc.includes(q)) return false;
      }

      // 4. Locality
      if (locality !== 'All Localities') {
        if ((l.locality || '').toLowerCase() !== locality.toLowerCase()) return false;
      }

      // 5. BHK
      if (bhk !== 'All BHKs') {
        const numBhk = parseInt(bhk[0], 10);
        if (bhk.includes('+')) {
          if ((l.bedroom || 0) < numBhk) return false;
        } else {
          if (l.bedroom !== numBhk) return false;
        }
      }

      // 6. Furnishing
      if (furnishing !== 'All Furnishing') {
        if ((l.furnishing || '').toLowerCase() !== furnishing.toLowerCase()) return false;
      }

      return true;
    }).sort((a, b) => {
      if (sortBy === 'price_asc') return (a.price || 0) - (b.price || 0);
      if (sortBy === 'price_desc') return (b.price || 0) - (a.price || 0);
      if (sortBy === 'area_desc') return (b.carpet_area || 0) - (a.carpet_area || 0);
      return 0;
    });
  }, [listings, search, locality, bhk, furnishing, hideCorruptAndFake, onlyActive, sortBy]);

  const totalPages = Math.ceil(filteredListings.length / pageSize) || 1;
  const paginatedListings = filteredListings.slice((page - 1) * pageSize, page * pageSize);

  if (selectedListing) {
    return <ListingDetailPage listingId={selectedListing.listing_id} onBack={() => setSelectedListing(null)} allListings={listings} />;
  }

  return (
    <div className="container">
      {/* Title & Stats */}
      <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: '800' }} className="text-gradient">
            Sale Listings in Chennai
          </h1>
          <p className="text-muted" style={{ fontSize: '0.95rem' }}>
            Browse verified apartments, houses, and plots with frontend data cleaning.
          </p>
        </div>

        <button className="btn btn-secondary" onClick={loadListings} disabled={loading}>
          <RefreshCw size={16} className={loading ? 'spin' : ''} /> Refresh Data
        </button>
      </div>

      {/* Filter Controls Bar */}
      <div className="glass-card" style={{ padding: '1.25rem', marginBottom: '1.5rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
          {/* Search */}
          <div style={{ position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '12px', top: '12px', color: '#64748b' }} />
            <input
              type="text"
              placeholder="Search apartment, locality..."
              className="input-field"
              style={{ paddingLeft: '2.5rem' }}
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            />
          </div>

          {/* Locality */}
          <select className="select-field" value={locality} onChange={(e) => { setLocality(e.target.value); setPage(1); }}>
            {LOCALITIES.map((loc) => (
              <option key={loc} value={loc}>{loc.toUpperCase()}</option>
            ))}
          </select>

          {/* BHK */}
          <select className="select-field" value={bhk} onChange={(e) => { setBhk(e.target.value); setPage(1); }}>
            {BHK_OPTIONS.map((b) => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>

          {/* Furnishing */}
          <select className="select-field" value={furnishing} onChange={(e) => { setFurnishing(e.target.value); setPage(1); }}>
            {FURNISHING_OPTIONS.map((f) => (
              <option key={f} value={f}>{f.replace('-', ' ').toUpperCase()}</option>
            ))}
          </select>

          {/* Sort By */}
          <select className="select-field" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="default">Sort by: Default</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="area_desc">Carpet Area: Largest</option>
          </select>
        </div>

        {/* Data Quality Toggles */}
        <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', paddingTop: '0.75rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)', fontSize: '0.85rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: '#cbd5e1' }}>
            <input
              type="checkbox"
              checked={hideCorruptAndFake}
              onChange={(e) => setHideCorruptAndFake(e.target.checked)}
              style={{ accentColor: 'var(--accent-primary)', width: '16px', height: '16px' }}
            />
            <ShieldCheck size={16} className="text-emerald-400" />
            <span>Filter Out Corrupt & Fake Listings</span>
          </label>

          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: '#cbd5e1' }}>
            <input
              type="checkbox"
              checked={onlyActive}
              onChange={(e) => setOnlyActive(e.target.checked)}
              style={{ accentColor: 'var(--accent-primary)', width: '16px', height: '16px' }}
            />
            <span>Show Active (`is_live: true`) Only</span>
          </label>
        </div>
      </div>

      {/* Loading & Error States */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '4rem' }}>
          <div className="spin" style={{ display: 'inline-block', width: '40px', height: '40px', border: '3px solid rgba(99, 102, 241, 0.3)', borderTopColor: '#6366f1', borderRadius: '50%' }}></div>
          <p style={{ marginTop: '1rem', color: '#94a3b8' }}>Fetching dataset from Ivy Homes Property API...</p>
        </div>
      )}

      {error && (
        <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', color: '#f87171', padding: '1rem', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Grid of Listings */}
      {!loading && !error && (
        <>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', fontSize: '0.9rem', color: '#94a3b8' }}>
            <span>Showing {paginatedListings.length} of {filteredListings.length} matching listings (Total retrievable: {listings.length})</span>
            <span>Page {page} of {totalPages}</span>
          </div>

          <div className="grid-3">
            {paginatedListings.map((l) => (
              <ListingCard key={l.listing_id} listing={l} onSelect={(item) => setSelectedListing(item)} allListings={listings} />
            ))}
          </div>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', marginTop: '2rem' }}>
              <button
                className="btn btn-secondary"
                onClick={() => setPage((p) => Math.max(p - 1, 1))}
                disabled={page === 1}
              >
                Previous
              </button>
              <span style={{ display: 'flex', alignItems: 'center', padding: '0 1rem', color: '#94a3b8', fontSize: '0.9rem' }}>
                Page {page} of {totalPages}
              </span>
              <button
                className="btn btn-secondary"
                onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
                disabled={page === totalPages}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ListingsPage;
