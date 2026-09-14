import React from 'react';
import { formatProjectPrice } from '../services/api';
import { Building2, MapPin, Calendar, CheckCircle2, AlertCircle, Layers } from 'lucide-react';

const ProjectCard = ({ project, actualListingsCount }) => {
  const minPriceStr = formatProjectPrice(project.price_min);
  const maxPriceStr = formatProjectPrice(project.price_max);

  const reportedListings = project.total_listings || 0;
  const isCountWrong = actualListingsCount !== undefined && reportedListings !== actualListingsCount;

  return (
    <div className="glass-card" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
          <div>
            <span className="badge badge-live" style={{ background: 'rgba(139, 92, 246, 0.15)', color: '#c084fc', borderColor: 'rgba(139, 92, 246, 0.3)' }}>
              {project.project_status || 'Under Construction'}
            </span>
          </div>

          {isCountWrong && (
            <span className="badge badge-corrupt" title={`Reported ${reportedListings} listings, but API actually serves ${actualListingsCount} matching listings`}>
              <AlertCircle size={12} /> Inventory Mismatch
            </span>
          )}
        </div>

        <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: '#f8fafc', marginBottom: '0.3rem' }}>
          {project.apartment_name}
        </h3>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#94a3b8', fontSize: '0.85rem', marginBottom: '1rem', textTransform: 'capitalize' }}>
          <MapPin size={14} style={{ color: '#c084fc' }} />
          <span>{project.locality}, Chennai • Developer: {project.developer_name || 'N/A'}</span>
        </div>

        {/* Price Range */}
        <div style={{ marginBottom: '1rem', background: 'rgba(15, 23, 42, 0.5)', padding: '0.8rem', borderRadius: '10px' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.2rem' }}>Price Range</div>
          <div style={{ fontSize: '1.3rem', fontWeight: '800', color: '#c084fc' }}>
            {minPriceStr} - {maxPriceStr}
          </div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1', marginTop: '0.2rem' }}>
            Area: {project.min_area_sqft || 0} - {project.max_area_sqft || 0} sq.ft.
          </div>
        </div>

        {/* Stats Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.5rem', fontSize: '0.8rem', marginBottom: '1rem' }}>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '0.5rem', borderRadius: '6px' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.75rem' }}>Total Units</div>
            <div style={{ fontWeight: '700', color: '#f8fafc' }}>{project.total_units || 'N/A'}</div>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '0.5rem', borderRadius: '6px' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.75rem' }}>Reported Listings</div>
            <div style={{ fontWeight: '700', color: isCountWrong ? '#f59e0b' : '#34d399' }}>
              {reportedListings} {isCountWrong && `(Actual: ${actualListingsCount})`}
            </div>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '0.5rem', borderRadius: '6px' }}>
            <div style={{ color: '#94a3b8', fontSize: '0.75rem' }}>Towers / Floors</div>
            <div style={{ fontWeight: '700', color: '#f8fafc' }}>{project.total_towers || 1} T / {project.total_floors || 1} F</div>
          </div>
        </div>

        {/* Amenities */}
        {project.amenities && project.amenities.length > 0 && (
          <div style={{ display: 'flex', gap: '0.3rem', flexWrap: 'wrap', marginBottom: '0.5rem' }}>
            {project.amenities.slice(0, 4).map((a, idx) => (
              <span key={idx} style={{ background: 'rgba(255, 255, 255, 0.06)', padding: '0.15rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem', color: '#cbd5e1' }}>
                {a}
              </span>
            ))}
            {project.amenities.length > 4 && (
              <span style={{ fontSize: '0.75rem', color: '#94a3b8', alignSelf: 'center' }}>+{project.amenities.length - 4} more</span>
            )}
          </div>
        )}
      </div>

      {/* RERA */}
      {project.rera_number && (
        <div style={{ fontSize: '0.75rem', color: '#64748b', paddingTop: '0.6rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
          RERA: {project.rera_number}
        </div>
      )}
    </div>
  );
};

export default ProjectCard;
