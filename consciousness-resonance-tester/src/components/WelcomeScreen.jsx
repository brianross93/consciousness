import { useState } from 'react';

function WelcomeScreen({ onStart }) {
  const [headphonesConfirmed, setHeadphonesConfirmed] = useState(false);

  return (
    <div className="container fade-in" style={{ paddingTop: '4rem' }}>
      <div className="card" style={{ textAlign: 'center', maxWidth: '600px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '2rem' }}>
          <h1 style={{ 
            fontSize: '1.75rem', 
            fontWeight: 600,
            marginBottom: '0.5rem',
            background: 'linear-gradient(135deg, var(--accent-cyan), var(--accent-magenta))',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            Consciousness Resonance Tester
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Cognitive Performance Under Auditory Conditions
          </p>
        </div>

        {/* Experiment Overview */}
        <div style={{ 
          textAlign: 'left', 
          background: 'var(--bg-tertiary)', 
          padding: '1.5rem',
          borderRadius: '8px',
          marginBottom: '1.5rem'
        }}>
          <h3 style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Experiment Protocol
          </h3>
          <ul style={{ 
            listStyle: 'none', 
            fontSize: '0.95rem',
            color: 'var(--text-secondary)'
          }}>
            <li style={{ marginBottom: '0.75rem', display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>01</span>
              <span>3 practice questions to familiarize yourself</span>
            </li>
            <li style={{ marginBottom: '0.75rem', display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>02</span>
              <span>5 phases × 10 questions each (50 total)</span>
            </li>
            <li style={{ marginBottom: '0.75rem', display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>03</span>
              <span>Different audio conditions per phase (randomized order)</span>
            </li>
            <li style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>04</span>
              <span>Answer as quickly and accurately as possible</span>
            </li>
          </ul>
        </div>

        {/* Audio Conditions */}
        <div style={{ 
          textAlign: 'left',
          marginBottom: '1.5rem',
          padding: '1rem',
          border: '1px solid var(--border-color)',
          borderRadius: '8px'
        }}>
          <h3 style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Audio Conditions
          </h3>
          <div style={{ fontSize: '0.85rem' }}>
            <div style={{ marginBottom: '0.5rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Control:</span>
              <span style={{ color: 'var(--text-secondary)', marginLeft: '0.5rem' }}>Silence, White Noise</span>
            </div>
            <div style={{ marginBottom: '0.5rem' }}>
              <span style={{ color: 'var(--accent-magenta)' }}>Disruption:</span>
              <span style={{ color: 'var(--text-secondary)', marginLeft: '0.5rem' }}>37 Hz, 35-45 Hz Sweep</span>
            </div>
            <div>
              <span style={{ color: 'var(--accent-cyan)' }}>Entrainment:</span>
              <span style={{ color: 'var(--text-secondary)', marginLeft: '0.5rem' }}>40 Hz Pulse</span>
            </div>
          </div>
        </div>

        {/* Headphone Warning */}
        <div className="headphone-warning">
          <span className="headphone-icon">🎧</span>
          <div>
            <strong>Headphones Required</strong>
            <p style={{ fontSize: '0.8rem', margin: '0.25rem 0 0', opacity: 0.9 }}>
              Low-frequency tones (37 Hz) cannot be reproduced by laptop speakers.
            </p>
          </div>
        </div>

        {/* Confirmation Checkbox */}
        <label style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          gap: '0.75rem',
          cursor: 'pointer',
          marginBottom: '1.5rem',
          padding: '1rem',
          background: headphonesConfirmed ? 'rgba(0, 212, 255, 0.1)' : 'transparent',
          borderRadius: '8px',
          transition: 'background 0.2s'
        }}>
          <input
            type="checkbox"
            checked={headphonesConfirmed}
            onChange={(e) => setHeadphonesConfirmed(e.target.checked)}
            style={{ 
              width: '20px', 
              height: '20px',
              accentColor: 'var(--accent-cyan)'
            }}
          />
          <span style={{ color: 'var(--text-primary)' }}>
            I am wearing headphones and ready to begin
          </span>
        </label>

        {/* Start Button */}
        <button 
          className="btn btn-primary"
          onClick={onStart}
          disabled={!headphonesConfirmed}
          style={{ width: '100%', fontSize: '1.1rem' }}
        >
          Begin Experiment
        </button>

        {/* Duration Note */}
        <p style={{ 
          marginTop: '1rem', 
          fontSize: '0.75rem', 
          color: 'var(--text-muted)'
        }}>
          Estimated duration: 12-18 minutes
        </p>
      </div>

      {/* Footer */}
      <div style={{ 
        textAlign: 'center', 
        marginTop: '2rem',
        fontSize: '0.75rem',
        color: 'var(--text-muted)'
      }}>
        <p>Testing hypothesis: Does gamma-band (40 Hz) interference affect cognitive binding?</p>
      </div>
    </div>
  );
}

export default WelcomeScreen;

