import React, { useState, useEffect } from 'react';
import submissionData from '../../submission.json';
import { fetchAllListings, fetchAnalyticsSummary, formatCurrency } from '../services/api';
import { BarChart3, ShieldAlert, CheckCircle, AlertTriangle, Eye, PieChart, MapPin, Building2, Server, HelpCircle } from 'lucide-react';

const CATEGORIES = [
  'ALL',
  'auth',
  'pagination',
  'units',
  'filters',
  'sorting',
  'timestamps',
  'duplicates',
  'data_quality',
  'fraud',
  'consistency',
  'missing_endpoint',
  'undocumented_endpoint'
];

const InsightsPage = () => {
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [evidenceModal, setEvidenceModal] = useState(null);
  const [summaryData, setSummaryData] = useState(null);
  const [loadingSummary, setLoadingSummary] = useState(true);

  const answers = submissionData.answers || {};
  const findings = submissionData.findings || [];

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    setLoadingSummary(true);
    try {
      const listingsData = await fetchAllListings();
      const summary = await fetchAnalyticsSummary(listingsData);
      setSummaryData(summary);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingSummary(false);
    }
  };

  const filteredFindings = selectedCategory === 'ALL'
    ? findings
    : findings.filter(f => f.category === selectedCategory);

  return (
    <div className="container">
      {/* Page Title */}
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.2rem', fontWeight: '800' }} className="text-gradient">
          Insights & API Audit Dashboard
        </h1>
        <p className="text-muted" style={{ fontSize: '1rem' }}>
          Real-time city analytics, empirical verification of 10 assignment questions, and complete audit of 18 documentation discrepancies for City Chennai.
        </p>
      </div>

      {/* SECTION 1: PROMISED ANALYTICS SUMMARY (/v1/analytics/summary) */}
      <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '2.5rem', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <h2 style={{ fontSize: '1.4rem', fontWeight: '700', color: '#f8fafc' }}>
                Promised City Analytics (<code style={{ color: '#a5b4fc' }}>/v1/analytics/summary</code>)
              </h2>
              <span className="badge badge-corrupt" style={{ textTransform: 'none' }}>
                <Server size={12} /> Server Endpoint Status: HTTP 404 Not Found (Doc Lie #12)
              </span>
            </div>
            <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: '0.2rem' }}>
              Documented endpoint promises city aggregates. Since server returns 404, our frontend dynamically computes the promised metrics client-side.
            </p>
          </div>
        </div>

        {loadingSummary ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#94a3b8' }}>
            <div className="spin" style={{ display: 'inline-block', width: '30px', height: '30px', border: '3px solid rgba(99, 102, 241, 0.3)', borderTopColor: '#6366f1', borderRadius: '50%' }}></div>
            <p style={{ marginTop: '0.5rem', fontSize: '0.85rem' }}>Computing city aggregates from 4,100 listings...</p>
          </div>
        ) : summaryData ? (
          <>
            {/* Top 4 Promised Metric Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
              <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase' }}>City Name</div>
                <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#818cf8', textTransform: 'capitalize' }}>{summaryData.city}</div>
                <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>Assigned Region</div>
              </div>

              <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase' }}>Total Active Listings</div>
                <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#34d399' }}>{summaryData.total_listings}</div>
                <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>Out of {summaryData.total_records_retrieved} total records</div>
              </div>

              <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase' }}>City Median Price</div>
                <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#c084fc' }}>{formatCurrency(summaryData.median_price)}</div>
                <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>₹{summaryData.median_price?.toLocaleString('en-IN')}</div>
              </div>

              <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase' }}>Median Price / Sq.Ft.</div>
                <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#f472b6' }}>₹{summaryData.median_price_per_sqft?.toLocaleString('en-IN')}</div>
                <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>Per Carpet Sq.Ft.</div>
              </div>
            </div>

            {/* Locality Breakdown & BHK Distribution Grids */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '1.5rem' }}>
              {/* By Locality */}
              <div style={{ background: 'rgba(15, 23, 42, 0.4)', padding: '1.25rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                <h4 style={{ fontSize: '1rem', fontWeight: '700', marginBottom: '0.75rem', color: '#cbd5e1', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <MapPin size={16} className="text-indigo-400" /> Locality Breakdown (`by_locality`)
                </h4>
                <div style={{ maxHeight: '240px', overflowY: 'auto' }}>
                  <table style={{ width: '100%', fontSize: '0.85rem', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ color: '#94a3b8', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', textAlign: 'left' }}>
                        <th style={{ padding: '0.4rem' }}>Locality</th>
                        <th style={{ padding: '0.4rem', textAlign: 'right' }}>Listings</th>
                        <th style={{ padding: '0.4rem', textAlign: 'right' }}>Median Price</th>
                      </tr>
                    </thead>
                    <tbody>
                      {summaryData.by_locality?.map((loc, idx) => (
                        <tr key={idx} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                          <td style={{ padding: '0.4rem', textTransform: 'capitalize', color: '#f8fafc' }}>{loc.locality}</td>
                          <td style={{ padding: '0.4rem', textAlign: 'right', color: '#a5b4fc', fontWeight: '600' }}>{loc.count}</td>
                          <td style={{ padding: '0.4rem', textAlign: 'right', color: '#34d399' }}>{formatCurrency(loc.median_price)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* By BHK */}
              <div style={{ background: 'rgba(15, 23, 42, 0.4)', padding: '1.25rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                <h4 style={{ fontSize: '1rem', fontWeight: '700', marginBottom: '0.75rem', color: '#cbd5e1', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <PieChart size={16} className="text-purple-400" /> Bedroom Distribution (`by_bhk`)
                </h4>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.75rem' }}>
                  {summaryData.by_bhk?.map((b, idx) => (
                    <div key={idx} style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '0.6rem 0.8rem', borderRadius: '8px' }}>
                      <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>{b.bedroom} BHK Configuration</div>
                      <div style={{ fontSize: '1.1rem', fontWeight: '700', color: '#f8fafc' }}>{b.count} Listings</div>
                      <div style={{ fontSize: '0.75rem', color: '#c084fc' }}>Median: {formatCurrency(b.median_price)}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </>
        ) : null}
      </div>

      {/* SECTION 2: TEN ASSIGNMENT ANSWERS (PART 2) */}
      <h2 style={{ fontSize: '1.4rem', fontWeight: '700', marginBottom: '1rem', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <BarChart3 className="text-indigo-400" /> Part 2 — Ten Assignment Answers (Chennai)
      </h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', marginBottom: '3rem' }}>
        {/* Q1 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #6366f1' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q1. total_listing_records</div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#f8fafc', margin: '0.2rem 0' }}>{answers.total_listing_records}</div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Total records retrievable from /v1/listings via offset pagination</div>
        </div>

        {/* Q2 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #8b5cf6' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q2. unique_properties</div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#f8fafc', margin: '0.2rem 0' }}>{answers.unique_properties}</div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Distinct physical properties deduplicated by location & specs</div>
        </div>

        {/* Q3 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #10b981' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q3. active_listings</div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#f8fafc', margin: '0.2rem 0' }}>{answers.active_listings}</div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Listings where is_live === true ({((answers.active_listings / (answers.total_listing_records || 1)) * 100).toFixed(1)}% of total)</div>
        </div>

        {/* Q4 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #f59e0b' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q4. corrupt_listing_ids</div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#fbbf24', margin: '0.2rem 0' }}>{answers.corrupt_listing_ids?.length || 0} IDs</div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Listings with physically impossible attributes</div>
        </div>

        {/* Q5 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #3b82f6' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q5. total_monthly_rent (T Nagar)</div>
          <div style={{ fontSize: '1.6rem', fontWeight: '800', color: '#60a5fa', margin: '0.2rem 0' }}>₹{(answers.total_monthly_rent || 0).toLocaleString('en-IN')}</div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Sum of monthly rent across all rentals in assigned locality</div>
        </div>

        {/* Q6 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #ec4899' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q6. avg_price_per_sqft_2bhk</div>
          <div style={{ fontSize: '1.6rem', fontWeight: '800', color: '#f472b6', margin: '0.2rem 0' }}>₹{(answers.avg_price_per_sqft_2bhk || 0).toLocaleString('en-IN')} / sqft</div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Mean price/carpet_area for active 2BHKs (excl. corrupt & fake)</div>
        </div>

        {/* Q7 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #a855f7' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q7. costliest_project</div>
          <div style={{ fontSize: '1.4rem', fontWeight: '800', color: '#c084fc', margin: '0.2rem 0' }}>
            {answers.costliest_project?.project_id} (₹{((answers.costliest_project?.price_max_inr || 0) / 10000000).toFixed(2)} Cr)
          </div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Project with highest maximum price in city</div>
        </div>

        {/* Q8 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #14b8a6' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q8. listings_last_7_days</div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#2dd4bf', margin: '0.2rem 0' }}>{answers.listings_last_7_days}</div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Listings posted in [2026-09-03, 2026-09-10 IST)</div>
        </div>

        {/* Q9 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #ef4444' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q9. fake_listing_ids</div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#f87171', margin: '0.2rem 0' }}>{answers.fake_listing_ids?.length || 0} IDs</div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Lead-gen listings with scam contacts or rent as sale price</div>
        </div>

        {/* Q10 */}
        <div className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #f97316' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Q10. projects_with_wrong_listing_count</div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#fb923c', margin: '0.2rem 0' }}>{answers.projects_with_wrong_listing_count}</div>
          <div style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>Projects where reported total_listings disagrees with actual</div>
        </div>
      </div>

      {/* SECTION 3: LIST THE LIES (PART 3) */}
      <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: '700', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <ShieldAlert className="text-rose-400" /> Part 3 — Where the Documentation Lies ({findings.length} Discrepancies)
          </h2>
          <p className="text-muted" style={{ fontSize: '0.9rem' }}>
            Categorized audit findings verified directly against the running API.
          </p>
        </div>
      </div>

      {/* Category Filter Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', overflowX: 'auto', paddingBottom: '0.75rem', marginBottom: '1.5rem' }}>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`btn ${selectedCategory === cat ? 'btn-primary' : 'btn-secondary'}`}
            style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem', whitespace: 'nowrap' }}
          >
            {cat.toUpperCase()} {cat !== 'ALL' && `(${findings.filter(f => f.category === cat).length})`}
          </button>
        ))}
      </div>

      {/* Findings List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {filteredFindings.map((finding, idx) => (
          <div key={idx} className="glass-card" style={{ padding: '1.25rem', borderLeft: '4px solid #818cf8' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <code style={{ background: 'rgba(99, 102, 241, 0.2)', color: '#a5b4fc', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.9rem', fontWeight: '700' }}>
                  {finding.endpoint}
                </code>
                <span className="badge badge-live" style={{ background: 'rgba(255, 255, 255, 0.08)', color: '#cbd5e1', borderColor: 'var(--border-color)' }}>
                  {finding.category}
                </span>
              </div>

              {finding.evidence && finding.evidence.length > 0 && (
                <button
                  className="btn btn-secondary"
                  style={{ padding: '0.25rem 0.6rem', fontSize: '0.75rem' }}
                  onClick={() => setEvidenceModal(finding)}
                >
                  <Eye size={12} /> View Evidence ({finding.evidence.length})
                </button>
              )}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '0.75rem', background: 'rgba(15, 23, 42, 0.4)', padding: '0.8rem', borderRadius: '8px', fontSize: '0.85rem' }}>
              <div>
                <strong style={{ color: '#f87171', display: 'block', marginBottom: '0.2rem' }}>⚠️ Documented Claim:</strong>
                <span style={{ color: '#cbd5e1' }}>{finding.documented}</span>
              </div>
              <div>
                <strong style={{ color: '#34d399', display: 'block', marginBottom: '0.2rem' }}>✅ Actual API Behavior:</strong>
                <span style={{ color: '#cbd5e1' }}>{finding.actual}</span>
              </div>
            </div>

            <div style={{ marginTop: '0.75rem', fontSize: '0.8rem', color: '#94a3b8', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
              <span><strong>How Found:</strong> {finding.how_found}</span>
              <span><strong>Impact:</strong> {finding.impact}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Evidence Inspector Modal */}
      {evidenceModal && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '600px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: '700', marginBottom: '0.5rem', color: '#f8fafc' }}>
              Evidence Inspector — {evidenceModal.endpoint} ({evidenceModal.category})
            </h3>
            <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginBottom: '1rem' }}>
              Demonstrating record IDs / project IDs / numbers for finding: "{evidenceModal.actual}"
            </p>

            <div style={{ background: 'rgba(15, 23, 42, 0.8)', padding: '1rem', borderRadius: '8px', maxHeight: '300px', overflowY: 'auto', fontFamily: 'monospace', fontSize: '0.85rem', color: '#34d399', border: '1px solid var(--border-color)' }}>
              {JSON.stringify(evidenceModal.evidence, null, 2)}
            </div>

            <button className="btn btn-primary" style={{ marginTop: '1rem', width: '100%', justifyContent: 'center' }} onClick={() => setEvidenceModal(null)}>
              Close Evidence Inspector
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default InsightsPage;
