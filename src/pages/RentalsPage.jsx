import React, { useState, useEffect, useMemo } from 'react';
import { fetchAllRentals, formatCurrency } from '../services/api';
import { Key, MapPin, Bed, Bath, Maximize2, RefreshCw, Search } from 'lucide-react';

const LOCALITIES = ['All Localities', 't nagar', 'adyar', 'velachery', 'anna nagar', 'porur', 'perungudi', 'thoraipakkam', 'omr', 'tambaram'];

const RentalsPage = () => {
  const [rentals, setRentals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [locality, setLocality] = useState('All Localities');

  useEffect(() => {
    loadRentals();
  }, []);

  const loadRentals = async () => {
    setLoading(true);
    try {
      const data = await fetchAllRentals();
      setRentals(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const filtered = useMemo(() => {
    return rentals.filter((r) => {
      if (search.trim()) {
        const q = search.toLowerCase();
        const title = (r.title || r.apartment_name || '').toLowerCase();
        const loc = (r.locality || '').toLowerCase();
        if (!title.includes(q) && !loc.includes(q)) return false;
      }
      if (locality !== 'All Localities') {
        if ((r.locality || '').toLowerCase() !== locality.toLowerCase()) return false;
      }
      return true;
    });
  }, [rentals, search, locality]);

  // Compute T Nagar total monthly rent for prompt reference
  const tNagarRentals = rentals.filter(r => (r.locality || '').toLowerCase().trim() === 't nagar');
  const tNagarTotalRent = tNagarRentals.reduce((sum, r) => sum + (r.price || 0), 0);

  return (
    <div className="container">
      <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: '800' }} className="text-gradient">
            Rental Properties in Chennai
          </h1>
          <p className="text-muted" style={{ fontSize: '0.95rem' }}>
            Verified monthly rental listings with security deposit and carpet area transparency.
          </p>
        </div>
        <button className="btn btn-secondary" onClick={loadRentals} disabled={loading}>
          <RefreshCw size={16} className={loading ? 'spin' : ''} /> Refresh
        </button>
      </div>

      {/* Assigned Locality Rent Insight Bar */}
      <div className="glass-card" style={{ padding: '1rem 1.25rem', marginBottom: '1.5rem', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid rgba(99, 102, 241, 0.25)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <span style={{ fontSize: '0.85rem', color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: '700' }}>Assigned Locality Audit (T Nagar)</span>
          <div style={{ fontSize: '1.2rem', fontWeight: '800', color: '#f8fafc' }}>
            Total Monthly Rent Sum: ₹{tNagarTotalRent.toLocaleString('en-IN')} <span style={{ fontSize: '0.85rem', fontWeight: '400', color: '#94a3b8' }}>({tNagarRentals.length} active rental records)</span>
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="glass-card" style={{ padding: '1rem 1.25rem', marginBottom: '1.5rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        <div style={{ position: 'relative' }}>
          <Search size={18} style={{ position: 'absolute', left: '12px', top: '12px', color: '#64748b' }} />
          <input
            type="text"
            placeholder="Search apartment, locality..."
            className="input-field"
            style={{ paddingLeft: '2.5rem' }}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <select className="select-field" value={locality} onChange={(e) => setLocality(e.target.value)}>
          {LOCALITIES.map((loc) => (
            <option key={loc} value={loc}>{loc.toUpperCase()}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '4rem' }}>
          <div className="spin" style={{ display: 'inline-block', width: '40px', height: '40px', border: '3px solid rgba(99, 102, 241, 0.3)', borderTopColor: '#6366f1', borderRadius: '50%' }}></div>
          <p style={{ marginTop: '1rem', color: '#94a3b8' }}>Loading rental dataset...</p>
        </div>
      ) : (
        <>
          <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '1rem' }}>
            Showing {filtered.length} of {rentals.length} rental properties
          </div>

          <div className="grid-3">
            {filtered.map((r) => (
              <div key={r.listing_id} className="glass-card" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <span className="badge badge-live"><Key size={12} /> Rental</span>
                    <span style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'capitalize' }}>{r.furnishing}</span>
                  </div>

                  <h3 style={{ fontSize: '1.15rem', fontWeight: '700', color: '#f8fafc', marginBottom: '0.3rem' }}>
                    {r.title || `${r.bedroom} BHK in ${r.apartment_name}`}
                  </h3>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#94a3b8', fontSize: '0.85rem', marginBottom: '1rem', textTransform: 'capitalize' }}>
                    <MapPin size={14} style={{ color: '#818cf8' }} />
                    <span>{r.locality}, Chennai</span>
                  </div>

                  <div style={{ marginBottom: '1rem' }}>
                    <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#10b981' }}>
                      ₹{(r.price || 0).toLocaleString('en-IN')} <span style={{ fontSize: '0.85rem', color: '#94a3b8', fontWeight: '400' }}>/ month</span>
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                      Security Deposit: ₹{(r.deposit || 0).toLocaleString('en-IN')}
                    </div>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem', background: 'rgba(15, 23, 42, 0.5)', padding: '0.6rem', borderRadius: '8px', fontSize: '0.8rem' }}>
                    <div style={{ color: '#cbd5e1' }}>{r.bedroom || 0} BHK</div>
                    <div style={{ color: '#cbd5e1' }}>{r.bathroom || 0} Bath</div>
                    <div style={{ color: '#cbd5e1' }}>{r.carpet_area || 0} sqft</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default RentalsPage;
