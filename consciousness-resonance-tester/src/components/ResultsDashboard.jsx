import { useMemo } from 'react';

// Statistical helper functions
function mean(arr) {
  if (!arr.length) return 0;
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function variance(arr) {
  if (arr.length < 2) return 0;
  const m = mean(arr);
  return arr.reduce((acc, val) => acc + Math.pow(val - m, 2), 0) / (arr.length - 1);
}

function standardDeviation(arr) {
  return Math.sqrt(variance(arr));
}

function coefficientOfVariation(arr) {
  const m = mean(arr);
  if (m === 0) return 0;
  return (standardDeviation(arr) / m) * 100;
}

// Phase labels
const PHASE_LABELS = {
  1: { name: 'Silence', description: 'Baseline', color: 'var(--text-muted)' },
  2: { name: 'White Noise', description: 'Control', color: 'var(--accent-green)' },
  3: { name: '74 Hz Tone', description: 'Disrupt γ×2', color: 'var(--accent-magenta)' },
  4: { name: '70-90 Hz Sweep', description: 'Swept γ×2', color: 'var(--accent-yellow)' },
  5: { name: '40 Hz Binaural', description: 'Entrain γ', color: 'var(--accent-cyan)' }
};

function ResultsDashboard({ results, phaseOrder, audio, onRestart }) {
  // Calculate statistics for each phase (5 phases now)
  const phaseStats = useMemo(() => {
    const stats = {};
    
    for (const phase of [1, 2, 3, 4, 5]) {
      const data = results.phases[phase];
      const times = data.times || [];
      const questions = data.questions || [];
      
      // Calculate difficulty breakdown
      const byDifficulty = {
        easy: questions.filter(q => q.difficulty === 'easy'),
        moderate: questions.filter(q => q.difficulty === 'moderate'),
        hard: questions.filter(q => q.difficulty === 'hard')
      };
      
      stats[phase] = {
        correct: data.correct,
        total: times.length,
        accuracy: times.length > 0 ? (data.correct / times.length) * 100 : 0,
        meanTime: mean(times),
        variance: variance(times),
        stdDev: standardDeviation(times),
        cv: coefficientOfVariation(times),
        minTime: times.length > 0 ? Math.min(...times) : 0,
        maxTime: times.length > 0 ? Math.max(...times) : 0,
        byDifficulty: {
          easy: {
            correct: byDifficulty.easy.filter(q => q.correct).length,
            total: byDifficulty.easy.length
          },
          moderate: {
            correct: byDifficulty.moderate.filter(q => q.correct).length,
            total: byDifficulty.moderate.length
          },
          hard: {
            correct: byDifficulty.hard.filter(q => q.correct).length,
            total: byDifficulty.hard.length
          }
        }
      };
    }
    
    return stats;
  }, [results]);

  // Phase groupings
  const disruptPhases = [3, 4];  // Interference
  const controlPhases = [1, 2];  // Baseline
  const entrainPhase = 5;        // Enhancement

  // Compare disruption vs control accuracy
  const disruptAccuracy = mean([phaseStats[3].accuracy, phaseStats[4].accuracy]);
  const controlAccuracy = mean([phaseStats[1].accuracy, phaseStats[2].accuracy]);
  const entrainAccuracy = phaseStats[5].accuracy;
  const accuracyDiff = controlAccuracy - disruptAccuracy;
  const entrainBoost = entrainAccuracy - controlAccuracy;

  // Compare disruption vs control variance
  const disruptVariance = mean([phaseStats[3].variance, phaseStats[4].variance]);
  const controlVariance = mean([phaseStats[1].variance, phaseStats[2].variance]);
  const entrainVariance = phaseStats[5].variance;
  const varianceRatio = controlVariance > 0 ? disruptVariance / controlVariance : 0;

  // Hypothesis evaluation
  const disruptionDetected = accuracyDiff > 5 || varianceRatio > 1.3;
  const entrainmentDetected = entrainBoost > 3 || (entrainVariance < controlVariance * 0.8);

  // Get all past results from localStorage
  const pastResults = useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem('resonanceResults') || '[]');
    } catch {
      return [];
    }
  }, []);

  return (
    <div className="container fade-in" style={{ paddingTop: '2rem' }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ 
          fontSize: '1.5rem', 
          fontWeight: 600,
          marginBottom: '0.5rem',
          background: 'linear-gradient(135deg, var(--accent-cyan), var(--accent-magenta))',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          Experiment Complete
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Session #{pastResults.length}
        </p>
      </div>

      {/* Summary Stats Grid */}
      <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(5, 1fr)', marginBottom: '1.5rem' }}>
        <div className="stat-card">
          <div className="stat-value" style={{ color: accuracyDiff > 0 ? 'var(--accent-magenta)' : 'var(--text-muted)' }}>
            {accuracyDiff > 0 ? '-' : '+'}{Math.abs(accuracyDiff).toFixed(1)}%
          </div>
          <div className="stat-label">Disruption Effect</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: entrainBoost > 0 ? 'var(--accent-cyan)' : 'var(--text-muted)' }}>
            {entrainBoost > 0 ? '+' : ''}{entrainBoost.toFixed(1)}%
          </div>
          <div className="stat-label">Entrainment Boost</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: varianceRatio > 1.2 ? 'var(--accent-magenta)' : 'var(--text-muted)' }}>
            {varianceRatio.toFixed(2)}×
          </div>
          <div className="stat-label">Variance Ratio</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {results.phases[1].correct + results.phases[2].correct + results.phases[3].correct + results.phases[4].correct + results.phases[5].correct}/50
          </div>
          <div className="stat-label">Total Correct</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            <span style={{ color: disruptionDetected ? 'var(--accent-magenta)' : 'var(--text-muted)' }}>
              {disruptionDetected ? '↓' : '—'}
            </span>
            {' / '}
            <span style={{ color: entrainmentDetected ? 'var(--accent-cyan)' : 'var(--text-muted)' }}>
              {entrainmentDetected ? '↑' : '—'}
            </span>
          </div>
          <div className="stat-label">Disrupt / Entrain</div>
        </div>
      </div>

      {/* Detailed Results Table */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ 
          fontSize: '0.875rem', 
          color: 'var(--text-muted)', 
          marginBottom: '1rem',
          textTransform: 'uppercase',
          letterSpacing: '0.05em'
        }}>
          Phase Breakdown
        </h3>
        
        <table className="results-table">
          <thead>
            <tr>
              <th>Phase</th>
              <th>Accuracy</th>
              <th>Mean Time</th>
              <th>Variance</th>
              <th>CV%</th>
              <th>Range</th>
            </tr>
          </thead>
          <tbody>
            {phaseOrder.map((phase, idx) => {
              const stats = phaseStats[phase];
              const label = PHASE_LABELS[phase];
              const isGamma = disruptPhases.includes(phase);
              
              return (
                <tr key={phase}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span style={{ 
                        width: '8px', 
                        height: '8px', 
                        borderRadius: '50%',
                        background: label.color
                      }}></span>
                      <div>
                        <div style={{ fontWeight: 500 }}>{label.name}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          {label.description}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className={isGamma && stats.accuracy < controlAccuracy ? 'highlight' : ''} 
                      style={phase === 5 && stats.accuracy > controlAccuracy ? { color: 'var(--accent-cyan)' } : {}}>
                    {stats.correct}/{stats.total} ({stats.accuracy.toFixed(0)}%)
                  </td>
                  <td>
                    {stats.meanTime.toFixed(2)}s
                  </td>
                  <td className={isGamma && stats.variance > controlVariance ? 'highlight' : ''}>
                    {stats.variance.toFixed(3)}
                  </td>
                  <td>
                    {stats.cv.toFixed(1)}%
                  </td>
                  <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    {stats.minTime.toFixed(1)}–{stats.maxTime.toFixed(1)}s
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Difficulty Breakdown */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ 
          fontSize: '0.875rem', 
          color: 'var(--text-muted)', 
          marginBottom: '1rem',
          textTransform: 'uppercase',
          letterSpacing: '0.05em'
        }}>
          Accuracy by Difficulty
        </h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
          {['easy', 'moderate', 'hard'].map(diff => {
            const color = diff === 'easy' ? 'var(--accent-green)' : diff === 'moderate' ? 'var(--accent-yellow)' : 'var(--accent-magenta)';
            const controlCorrect = (phaseStats[1].byDifficulty[diff]?.correct || 0) + (phaseStats[2].byDifficulty[diff]?.correct || 0);
            const controlTotal = (phaseStats[1].byDifficulty[diff]?.total || 0) + (phaseStats[2].byDifficulty[diff]?.total || 0);
            const disruptCorrect = (phaseStats[3].byDifficulty[diff]?.correct || 0) + (phaseStats[4].byDifficulty[diff]?.correct || 0);
            const disruptTotal = (phaseStats[3].byDifficulty[diff]?.total || 0) + (phaseStats[4].byDifficulty[diff]?.total || 0);
            const entrainCorrect = phaseStats[5].byDifficulty[diff]?.correct || 0;
            const entrainTotal = phaseStats[5].byDifficulty[diff]?.total || 0;
            
            return (
              <div key={diff} style={{ 
                background: 'var(--bg-tertiary)', 
                padding: '1rem', 
                borderRadius: '8px',
                borderTop: `3px solid ${color}`
              }}>
                <div style={{ 
                  fontSize: '0.75rem', 
                  color: color, 
                  textTransform: 'uppercase',
                  marginBottom: '0.5rem',
                  fontWeight: 600
                }}>
                  {diff}
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  <div>Control: {controlCorrect}/{controlTotal}</div>
                  <div>Disrupt: {disruptCorrect}/{disruptTotal}</div>
                  <div style={{ color: 'var(--accent-cyan)' }}>Entrain: {entrainCorrect}/{entrainTotal}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Interpretation */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ 
          fontSize: '0.875rem', 
          color: 'var(--text-muted)', 
          marginBottom: '1rem',
          textTransform: 'uppercase',
          letterSpacing: '0.05em'
        }}>
          Interpretation
        </h3>
        
        <div style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: 1.7 }}>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1rem', fontStyle: 'italic' }}>
            <strong>Disruption</strong> (37Hz, 35-45Hz sweep) vs <strong>Control</strong> (Silence, White Noise) vs <strong>Entrainment</strong> (40Hz pulse)
          </p>
          
          {accuracyDiff > 10 ? (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--accent-magenta)' }}>Strong disruption:</strong> Accuracy dropped by {accuracyDiff.toFixed(1)}% during gamma interference phases.
            </p>
          ) : accuracyDiff > 5 ? (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--accent-yellow)' }}>Moderate disruption:</strong> Accuracy dropped by {accuracyDiff.toFixed(1)}% during gamma interference.
            </p>
          ) : accuracyDiff > 0 ? (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--text-muted)' }}>Weak disruption:</strong> Only {accuracyDiff.toFixed(1)}% accuracy drop during interference.
            </p>
          ) : (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--text-muted)' }}>No disruption:</strong> Gamma interference did not reduce accuracy.
            </p>
          )}

          {entrainBoost > 5 ? (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--accent-cyan)' }}>Strong entrainment:</strong> 40Hz pulse improved accuracy by {entrainBoost.toFixed(1)}% vs control!
            </p>
          ) : entrainBoost > 2 ? (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--accent-cyan)' }}>Possible entrainment:</strong> 40Hz pulse showed {entrainBoost.toFixed(1)}% accuracy boost.
            </p>
          ) : entrainBoost < -5 ? (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--accent-yellow)' }}>Unexpected:</strong> 40Hz pulse reduced accuracy by {Math.abs(entrainBoost).toFixed(1)}% — may also be disruptive at this intensity.
            </p>
          ) : (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--text-muted)' }}>No entrainment effect:</strong> 40Hz pulse performed similarly to control.
            </p>
          )}

          {varianceRatio > 1.5 ? (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--accent-magenta)' }}>High cognitive destabilization:</strong> Response time variance was {varianceRatio.toFixed(2)}× higher during interference.
            </p>
          ) : varianceRatio > 1.2 ? (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--accent-yellow)' }}>Moderate destabilization:</strong> Response time variance was {varianceRatio.toFixed(2)}× higher during interference.
            </p>
          ) : (
            <p style={{ marginBottom: '1rem' }}>
              <strong style={{ color: 'var(--text-muted)' }}>Stable variance:</strong> Response time consistency similar across conditions.
            </p>
          )}

          <p style={{ 
            fontSize: '0.85rem', 
            color: 'var(--text-muted)',
            fontStyle: 'italic',
            borderTop: '1px solid var(--border-color)',
            paddingTop: '1rem',
            marginTop: '1rem'
          }}>
            Note: Single-session results have high noise. Run multiple sessions for reliable conclusions.
            Currently: {pastResults.length} session(s) recorded.
          </p>
        </div>
      </div>

      {/* Phase Order (for debugging/verification) */}
      <div style={{ 
        fontSize: '0.75rem', 
        color: 'var(--text-muted)', 
        textAlign: 'center',
        marginBottom: '1.5rem',
        fontFamily: 'IBM Plex Mono'
      }}>
        Phase order: {phaseOrder.map(p => PHASE_LABELS[p].name).join(' → ')}
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
        <button className="btn btn-primary" onClick={onRestart}>
          Run Another Session
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => {
            const data = JSON.stringify(pastResults, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `resonance-results-${Date.now()}.json`;
            a.click();
          }}
        >
          Export All Data
        </button>
      </div>

      {/* Raw Data (collapsible) */}
      <details style={{ marginTop: '2rem' }}>
        <summary style={{ 
          cursor: 'pointer', 
          color: 'var(--text-muted)',
          fontSize: '0.875rem',
          marginBottom: '1rem'
        }}>
          View Raw Response Times
        </summary>
        <div style={{ 
          background: 'var(--bg-tertiary)', 
          padding: '1rem', 
          borderRadius: '8px',
          fontFamily: 'IBM Plex Mono',
          fontSize: '0.75rem',
          overflowX: 'auto'
        }}>
          <pre style={{ margin: 0 }}>
            {JSON.stringify({
              phaseOrder,
              phases: Object.fromEntries(
                Object.entries(results.phases).map(([phase, data]) => [
                  `${phase} (${PHASE_LABELS[phase].name})`,
                  {
                    correct: data.correct,
                    times: data.times.map(t => t.toFixed(3)),
                    questions: data.questions || []
                  }
                ])
              )
            }, null, 2)}
          </pre>
        </div>
      </details>

      {/* Methodology Note */}
      <div style={{
        marginTop: '1.5rem',
        padding: '1rem',
        background: 'var(--bg-tertiary)',
        borderRadius: '8px',
        fontSize: '0.8rem',
        color: 'var(--text-muted)'
      }}>
        <strong style={{ color: 'var(--text-secondary)' }}>Methodology:</strong> Questions are randomly shuffled and distributed across phases each session to control for question difficulty. Phase order is also randomized.
      </div>
    </div>
  );
}

export default ResultsDashboard;

