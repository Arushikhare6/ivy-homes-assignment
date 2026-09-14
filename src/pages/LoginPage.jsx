import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Building2, Lock, Mail, CheckCircle, AlertCircle, ShieldCheck, KeyRound } from 'lucide-react';

const DEMO_ACCOUNTS = [
  { email: 'demo1@ivy.homes', label: 'Demo User 1' },
  { email: 'demo2@ivy.homes', label: 'Demo User 2' },
  { email: 'demo3@ivy.homes', label: 'Demo User 3' }
];
const DEMO_PASSWORD = '5ec43320d2';

const LoginPage = () => {
  const { login, loginError } = useAuth();
  const [email, setEmail] = useState('demo1@ivy.homes');
  const [password, setPassword] = useState(DEMO_PASSWORD);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    await login(email, password);
    setIsSubmitting(false);
  };

  const selectDemoAccount = (demoEmail) => {
    setEmail(demoEmail);
    setPassword(DEMO_PASSWORD);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1.5rem', background: 'radial-gradient(at 50% 0%, rgba(99, 102, 241, 0.2) 0px, transparent 70%)' }}>
      <div className="glass-card" style={{ width: '100%', maxWidth: '460px', padding: '2.5rem' }}>
        {/* Header Branding */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '56px', height: '56px', borderRadius: '16px', background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2))', border: '1px solid rgba(99, 102, 241, 0.3)', marginBottom: '1rem' }}>
            <Building2 size={30} className="text-indigo-400" />
          </div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: '800', marginBottom: '0.3rem' }} className="text-gradient">
            Ivy Homes Portal
          </h1>
          <p className="text-muted" style={{ fontSize: '0.9rem' }}>
            Property API Gateway • City Chennai
          </p>
        </div>

        {/* Error Alert */}
        {loginError && (
          <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', color: '#f87171', padding: '0.75rem 1rem', borderRadius: '10px', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.85rem' }}>
            <AlertCircle size={18} />
            <span>{loginError}</span>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1.25rem' }}>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '0.4rem', fontWeight: '500' }}>
              Email Address
            </label>
            <div style={{ position: 'relative' }}>
              <Mail size={18} style={{ position: 'absolute', left: '12px', top: '12px', color: '#64748b' }} />
              <input
                type="email"
                className="input-field"
                style={{ paddingLeft: '2.5rem' }}
                placeholder="demo1@ivy.homes"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div style={{ marginBottom: '1.75rem' }}>
            <label style={{ display: 'block', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '0.4rem', fontWeight: '500' }}>
              Password
            </label>
            <div style={{ position: 'relative' }}>
              <Lock size={18} style={{ position: 'absolute', left: '12px', top: '12px', color: '#64748b' }} />
              <input
                type="password"
                className="input-field"
                style={{ paddingLeft: '2.5rem' }}
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', justifyContent: 'center', padding: '0.85rem', fontSize: '1rem' }}
            disabled={isSubmitting}
          >
            <KeyRound size={18} />
            {isSubmitting ? 'Authenticating...' : 'Sign In to Access Portal'}
          </button>
        </form>

        {/* Quick Demo Account Selector */}
        <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <ShieldCheck size={14} className="text-indigo-400" />
            <span>Select Demo Account Credentials:</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {DEMO_ACCOUNTS.map((acc) => (
              <button
                key={acc.email}
                type="button"
                onClick={() => selectDemoAccount(acc.email)}
                className={`btn ${email === acc.email ? 'btn-primary' : 'btn-secondary'}`}
                style={{ justifyContent: 'space-between', padding: '0.6rem 1rem', fontSize: '0.85rem' }}
              >
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  {email === acc.email && <CheckCircle size={14} />}
                  {acc.label}
                </span>
                <span style={{ fontSize: '0.75rem', opacity: 0.8, fontFamily: 'monospace' }}>{acc.email}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
