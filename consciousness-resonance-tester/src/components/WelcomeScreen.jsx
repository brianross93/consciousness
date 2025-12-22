import { useState } from 'react';

function WelcomeScreen({ onStart, onOpenTinnitusMatcher }) {
  const [headphonesConfirmed, setHeadphonesConfirmed] = useState(false);

  return (
    <div className="container fade-in" style={{ paddingTop: '4rem' }}>
      <div className="card" style={{ textAlign: 'center', maxWidth: '650px', margin: '0 auto' }}>
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
            Frequency Specificity Test
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Testing whether gamma entrainment is frequency-specific or if any rhythm helps
          </p>
        </div>

        {/* Research Question */}
        <div style={{ 
          background: 'var(--bg-tertiary)', 
          padding: '1rem',
          borderRadius: '8px',
          marginBottom: '1.5rem',
          borderLeft: '4px solid var(--accent-cyan)'
        }}>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-primary)', margin: 0 }}>
            <strong>Question:</strong> Does 40 Hz specifically enhance cognitive binding, 
            or does any rhythmic stimulus help?
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
            Protocol
          </h3>
          <ul style={{ 
            listStyle: 'none', 
            fontSize: '0.95rem',
            color: 'var(--text-secondary)'
          }}>
            <li style={{ marginBottom: '0.75rem', display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>01</span>
              <span>3 practice questions</span>
            </li>
            <li style={{ marginBottom: '0.75rem', display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>02</span>
              <span><strong>8 conditions</strong> × 6 questions each (48 total)</span>
            </li>
            <li style={{ marginBottom: '0.75rem', display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>03</span>
              <span><strong>3 min pre-exposure</strong> per condition (lets brain entrain)</span>
            </li>
            <li style={{ marginBottom: '0.75rem', display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>04</span>
              <span>Binaural beats at different frequencies (randomized)</span>
            </li>
            <li style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
              <span style={{ color: 'var(--accent-cyan)' }}>05</span>
              <span>Answer pattern recognition questions quickly & accurately</span>
            </li>
          </ul>
        </div>

        {/* Conditions Grid */}
        <div style={{ 
          textAlign: 'left',
          marginBottom: '1.5rem',
          padding: '1rem',
          border: '1px solid var(--border-color)',
          borderRadius: '8px'
        }}>
          <h3 style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            8 Test Conditions
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', fontSize: '0.85rem' }}>
            <div>
              <div style={{ color: 'var(--text-muted)', fontWeight: 500, marginBottom: '0.5rem' }}>Control</div>
              <div style={{ color: 'var(--text-secondary)' }}>• Silence</div>
              <div style={{ color: 'var(--text-secondary)' }}>• Pink Noise</div>
            </div>
            <div>
              <div style={{ color: 'var(--accent-green)', fontWeight: 500, marginBottom: '0.5rem' }}>Target</div>
              <div style={{ color: 'var(--text-secondary)' }}>• <strong>40 Hz</strong> (gamma)</div>
            </div>
            <div>
              <div style={{ color: 'var(--accent-yellow)', fontWeight: 500, marginBottom: '0.5rem' }}>Near-Miss</div>
              <div style={{ color: 'var(--text-secondary)' }}>• 38 Hz (2 Hz low)</div>
              <div style={{ color: 'var(--text-secondary)' }}>• 42 Hz (2 Hz high)</div>
            </div>
            <div>
              <div style={{ color: 'var(--accent-cyan)', fontWeight: 500, marginBottom: '0.5rem' }}>Harmonics</div>
              <div style={{ color: 'var(--text-secondary)' }}>• 20 Hz (subharmonic)</div>
              <div style={{ color: 'var(--text-secondary)' }}>• 80 Hz (overtone)</div>
            </div>
            <div style={{ gridColumn: 'span 2' }}>
              <div style={{ color: 'var(--accent-purple)', fontWeight: 500, marginBottom: '0.5rem' }}>Unrelated</div>
              <div style={{ color: 'var(--text-secondary)' }}>• 53 Hz (not harmonically related)</div>
            </div>
          </div>
        </div>

        {/* What We're Testing */}
        <div style={{ 
          textAlign: 'left',
          marginBottom: '1.5rem',
          padding: '1rem',
          background: 'rgba(0, 212, 255, 0.05)',
          borderRadius: '8px',
          fontSize: '0.85rem'
        }}>
          <h3 style={{ fontSize: '0.75rem', color: 'var(--accent-cyan)', marginBottom: '0.75rem', textTransform: 'uppercase' }}>
            Hypotheses
          </h3>
          <div style={{ color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            <p style={{ margin: '0 0 0.5rem' }}>
              <strong>If gamma-specific:</strong> 40 Hz &gt; all others
            </p>
            <p style={{ margin: '0 0 0.5rem' }}>
              <strong>If harmonics matter:</strong> 40 ≈ 80 ≈ 20 Hz (octave relationships help)
            </p>
            <p style={{ margin: '0 0 0.5rem' }}>
              <strong>If any rhythm helps:</strong> All binaural ≈ each other &gt; silence
            </p>
            <p style={{ margin: 0 }}>
              <strong>If near-miss interferes:</strong> 38/42 Hz &lt; control (disrupts natural gamma)
            </p>
          </div>
        </div>

        {/* Headphone Warning */}
        <div className="headphone-warning">
          <span className="headphone-icon">🎧</span>
          <div>
            <strong>Stereo Headphones Required</strong>
            <p style={{ fontSize: '0.8rem', margin: '0.25rem 0 0', opacity: 0.9 }}>
              Binaural beats require different frequencies in each ear. Speakers won't work.
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
            I am wearing stereo headphones and ready to begin
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
          Estimated duration: 45-50 minutes
        </p>
      </div>

      {/* Tools Section */}
      {onOpenTinnitusMatcher && (
        <div style={{ 
          textAlign: 'center', 
          marginTop: '2rem',
          padding: '1rem',
          borderTop: '1px solid var(--border-color)'
        }}>
          <p style={{ 
            fontSize: '0.75rem', 
            color: 'var(--text-muted)',
            marginBottom: '0.75rem'
          }}>
            Additional Tools
          </p>
          <button 
            onClick={onOpenTinnitusMatcher}
            style={{
              background: 'transparent',
              border: '1px solid var(--border-color)',
              color: 'var(--text-secondary)',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '0.85rem',
              transition: 'all 0.2s'
            }}
            onMouseOver={(e) => {
              e.target.style.borderColor = 'var(--accent-cyan)';
              e.target.style.color = 'var(--accent-cyan)';
            }}
            onMouseOut={(e) => {
              e.target.style.borderColor = 'var(--border-color)';
              e.target.style.color = 'var(--text-secondary)';
            }}
          >
            🔊 Tinnitus Frequency Matcher
          </button>
        </div>
      )}

      {/* Footer */}
      <div style={{ 
        textAlign: 'center', 
        marginTop: '2rem',
        fontSize: '0.75rem',
        color: 'var(--text-muted)'
      }}>
        <p>Part of the Consciousness Investigation project</p>
        <p style={{ marginTop: '0.25rem' }}>Run multiple sessions for reliable results</p>
      </div>
    </div>
  );
}

export default WelcomeScreen;
