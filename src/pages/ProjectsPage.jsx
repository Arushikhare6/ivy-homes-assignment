import React, { useState, useEffect, useMemo } from 'react';
import { fetchAllProjects, fetchAllListings, getProjectMaxPriceInr } from '../services/api';
import ProjectCard from '../components/ProjectCard';
import { Building2, Search, RefreshCw, AlertCircle, Trophy } from 'lucide-react';

const LOCALITIES = ['All Localities', 't nagar', 'adyar', 'velachery', 'anna nagar', 'porur', 'perungudi', 'thoraipakkam', 'omr', 'tambaram'];

const ProjectsPage = () => {
  const [projects, setProjects] = useState([]);
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [locality, setLocality] = useState('All Localities');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [pData, lData] = await Promise.all([
        fetchAllProjects(),
        fetchAllListings()
      ]);
      setProjects(pData);
      setListings(lData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Listings per project mapping
  const listingsPerProject = useMemo(() => {
    const map = {};
    listings.forEach((l) => {
      if (l.project_id) {
        map[l.project_id] = (map[l.project_id] || 0) + 1;
      }
    });
    return map;
  }, [listings]);

  // Costliest Project Analysis
  const costliestProject = useMemo(() => {
    if (projects.length === 0) return null;
    let max = projects[0];
    let maxPriceInr = getProjectMaxPriceInr(max);

    projects.forEach((p) => {
      const priceInr = getProjectMaxPriceInr(p);
      if (priceInr > maxPriceInr) {
        maxPriceInr = priceInr;
        max = p;
      }
    });

    return { project: max, priceInr: maxPriceInr };
  }, [projects]);

  const filtered = useMemo(() => {
    return projects.filter((p) => {
      if (search.trim()) {
        const q = search.toLowerCase();
        const name = (p.apartment_name || '').toLowerCase();
        const dev = (p.developer_name || '').toLowerCase();
        const loc = (p.locality || '').toLowerCase();
        if (!name.includes(q) && !dev.includes(q) && !loc.includes(q)) return false;
      }
      if (locality !== 'All Localities') {
        if ((p.locality || '').toLowerCase() !== locality.toLowerCase()) return false;
      }
      return true;
    });
  }, [projects, search, locality]);

  const wrongInventoryCount = useMemo(() => {
    return projects.filter(p => {
      const reported = p.total_listings || 0;
      const actual = listingsPerProject[p.project_id] || 0;
      return reported !== actual;
    }).length;
  }, [projects, listingsPerProject]);

  return (
    <div className="container">
      <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: '800' }} className="text-gradient">
            Builder Projects in Chennai
          </h1>
          <p className="text-muted" style={{ fontSize: '0.95rem' }}>
            New developments and upcoming townships with corrected price units and inventory audit.
          </p>
        </div>
        <button className="btn btn-secondary" onClick={loadData} disabled={loading}>
          <RefreshCw size={16} className={loading ? 'spin' : ''} /> Refresh Data
        </button>
      </div>

      {/* Highlights Bar */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem', marginBottom: '1.5rem' }}>
        {costliestProject && (
          <div className="glass-card" style={{ padding: '1rem 1.25rem', background: 'rgba(139, 92, 246, 0.1)', border: '1px solid rgba(139, 92, 246, 0.3)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#c084fc', fontSize: '0.8rem', fontWeight: '700', textTransform: 'uppercase' }}>
              <Trophy size={16} /> Costliest Project in City (Q7)
            </div>
            <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#f8fafc', marginTop: '0.2rem' }}>
              {costliestProject.project.apartment_name} ({costliestProject.project.project_id})
            </div>
            <div style={{ fontSize: '0.9rem', color: '#cbd5e1' }}>
              Max Price: ₹{(costliestProject.priceInr / 10000000).toFixed(2)} Cr (₹{costliestProject.priceInr.toLocaleString('en-IN')})
            </div>
          </div>
        )}

        <div className="glass-card" style={{ padding: '1rem 1.25rem', background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.3)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#fbbf24', fontSize: '0.8rem', fontWeight: '700', textTransform: 'uppercase' }}>
            <AlertCircle size={16} /> Inventory Count Contradictions (Q10)
          </div>
          <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#f8fafc', marginTop: '0.2rem' }}>
            {wrongInventoryCount} of {projects.length} Projects Disagree
          </div>
          <div style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>
            Documented total_listings vs actual matching listings count
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="glass-card" style={{ padding: '1rem 1.25rem', marginBottom: '1.5rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        <div style={{ position: 'relative' }}>
          <Search size={18} style={{ position: 'absolute', left: '12px', top: '12px', color: '#64748b' }} />
          <input
            type="text"
            placeholder="Search project name, developer..."
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
          <p style={{ marginTop: '1rem', color: '#94a3b8' }}>Loading project dataset...</p>
        </div>
      ) : (
        <>
          <div style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '1rem' }}>
            Showing {filtered.length} of {projects.length} builder projects
          </div>

          <div className="grid-2">
            {filtered.map((p) => (
              <ProjectCard key={p.project_id} project={p} actualListingsCount={listingsPerProject[p.project_id] || 0} />
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default ProjectsPage;
