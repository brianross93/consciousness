import { useMemo } from 'react';
import { CONDITIONS, CONDITION_GROUPS } from '../hooks/useAudioEnhanced';

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

// Simple t-test (two-sample, assumes equal variance)
function tTest(arr1, arr2) {
  if (arr1.length < 2 || arr2.length < 2) return { t: 0, p: 1 };
  
  const n1 = arr1.length, n2 = arr2.length;
  const m1 = mean(arr1), m2 = mean(arr2);
  const v1 = variance(arr1), v2 = variance(arr2);
  
  // Pooled variance
  const sp2 = ((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2);
  const se = Math.sqrt(sp2 * (1/n1 + 1/n2));
  
  if (se === 0) return { t: 0, p: 1 };
  
  const t = (m1 - m2) / se;
  const df = n1 + n2 - 2;
  
  // Approximate p-value using normal distribution for large df
  const p = 2 * (1 - normalCDF(Math.abs(t)));
  
  return { t, p, df };
}

// Standard normal CDF approximation
function normalCDF(x) {
  const a1 =  0.254829592;
  const a2 = -0.284496736;
  const a3 =  1.421413741;
  const a4 = -1.453152027;
  const a5 =  1.061405429;
  const p  =  0.3275911;

  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x) / Math.sqrt(2);

  const t = 1.0 / (1.0 + p * x);
  const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

  return 0.5 * (1.0 + sign * y);
}

// Effect size (Cohen's d)
function cohensD(arr1, arr2) {
  if (arr1.length < 2 || arr2.length < 2) return 0;
  
  const m1 = mean(arr1), m2 = mean(arr2);
  const v1 = variance(arr1), v2 = variance(arr2);
  const n1 = arr1.length, n2 = arr2.length;
  
  // Pooled standard deviation
  const sp = Math.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2));
  
  if (sp === 0) return 0;
  return (m1 - m2) / sp;
}

function ResultsDashboard({ results, phaseOrder, audio, onRestart }) {
  // Calculate statistics for each phase
  const phaseStats = useMemo(() => {
    const stats = {};
    
    for (let phase = 1; phase <= 8; phase++) {
      const data = results.phases[phase];
      if (!data) continue;
      
      const times = data.times || [];
      const questions = data.questions || [];
      
      const byDifficulty = {
        easy: questions.filter(q => q.difficulty === 'easy'),
        moderate: questions.filter(q => q.difficulty === 'moderate'),
        hard: questions.filter(q => q.difficulty === 'hard')
      };
      
      stats[phase] = {
        condition: CONDITIONS[phase],
        correct: data.correct,
        total: times.length,
        accuracy: times.length > 0 ? (data.correct / times.length) * 100 : 0,
        meanTime: mean(times),
        variance: variance(times),
        stdDev: standardDeviation(times),
        cv: coefficientOfVariation(times),
        times: times,
        byDifficulty
      };
    }
    
    return stats;
  }, [results]);

  // Group analysis
  const groupStats = useMemo(() => {
    const groups = {};
    
    for (const [groupName, phases] of Object.entries(CONDITION_GROUPS)) {
      const allTimes = [];
      const allAccuracies = [];
      let totalCorrect = 0;
      let totalQuestions = 0;
      
      for (const phase of phases) {
        if (phaseStats[phase]) {
          allTimes.push(...phaseStats[phase].times);
          allAccuracies.push(phaseStats[phase].accuracy);
          totalCorrect += phaseStats[phase].correct;
          totalQuestions += phaseStats[phase].total;
        }
      }
      
      groups[groupName] = {
        phases,
        meanAccuracy: mean(allAccuracies),
        totalCorrect,
        totalQuestions,
        overallAccuracy: totalQuestions > 0 ? (totalCorrect / totalQuestions) * 100 : 0,
        meanTime: mean(allTimes),
        variance: variance(allTimes),
        times: allTimes
      };
    }
    
    return groups;
  }, [phaseStats]);

  // Key comparisons
  const comparisons = useMemo(() => {
    const targetTimes = phaseStats[3]?.times || [];
    const controlTimes = [...(groupStats.control?.times || [])];
    const nearMissTimes = [...(groupStats.near_miss?.times || [])];
    const harmonicTimes = [...(groupStats.harmonic?.times || [])];
    const unrelatedTimes = phaseStats[8]?.times || [];
    
    return {
      // Is 40 Hz better than control?
      targetVsControl: {
        accuracyDiff: (phaseStats[3]?.accuracy || 0) - (groupStats.control?.overallAccuracy || 0),
        timeDiff: (groupStats.control?.meanTime || 0) - (phaseStats[3]?.meanTime || 0),
        tTest: tTest(targetTimes, controlTimes),
        cohensD: cohensD(targetTimes, controlTimes)
      },
      // Is 40 Hz better than near-misses (38, 42 Hz)?
      targetVsNearMiss: {
        accuracyDiff: (phaseStats[3]?.accuracy || 0) - (groupStats.near_miss?.overallAccuracy || 0),
        tTest: tTest(targetTimes, nearMissTimes),
        cohensD: cohensD(targetTimes, nearMissTimes)
      },
      // Are harmonics (20, 80 Hz) similar to target?
      targetVsHarmonic: {
        accuracyDiff: (phaseStats[3]?.accuracy || 0) - (groupStats.harmonic?.overallAccuracy || 0),
        tTest: tTest(targetTimes, harmonicTimes),
        cohensD: cohensD(targetTimes, harmonicTimes)
      },
      // Is 40 Hz better than unrelated (53 Hz)?
      targetVsUnrelated: {
        accuracyDiff: (phaseStats[3]?.accuracy || 0) - (phaseStats[8]?.accuracy || 0),
        tTest: tTest(targetTimes, unrelatedTimes),
        cohensD: cohensD(targetTimes, unrelatedTimes)
      },
      // Do near-misses interfere vs control?
      nearMissVsControl: {
        accuracyDiff: (groupStats.control?.overallAccuracy || 0) - (groupStats.near_miss?.overallAccuracy || 0),
        tTest: tTest(controlTimes, nearMissTimes),
        cohensD: cohensD(controlTimes, nearMissTimes)
      }
    };
  }, [phaseStats, groupStats]);

  // Hypothesis evaluation
  const hypotheses = useMemo(() => {
    const c = comparisons;
    
    return {
      gammaSpecific: {
        label: "Gamma-Specific Entrainment",
        description: "40 Hz is better than control AND better than near-misses",
        supported: c.targetVsControl.accuracyDiff > 5 && c.targetVsNearMiss.accuracyDiff > 5,
        evidence: c.targetVsControl.accuracyDiff > 0 && c.targetVsNearMiss.accuracyDiff > 0 
          ? "Partial" : "None"
      },
      harmonicsHelp: {
        label: "Harmonic Relationships Matter",
        description: "20 Hz and 80 Hz perform similarly to 40 Hz (within 10%)",
        supported: Math.abs(c.targetVsHarmonic.accuracyDiff) < 10,
        evidence: Math.abs(c.targetVsHarmonic.accuracyDiff) < 15 ? "Partial" : "None"
      },
      nearMissInterferes: {
        label: "Near-Miss Interference",
        description: "38 Hz and 42 Hz perform WORSE than control",
        supported: c.nearMissVsControl.accuracyDiff > 5,
        evidence: c.nearMissVsControl.accuracyDiff > 0 ? "Partial" : "None"
      },
      anyRhythmHelps: {
        label: "Any Rhythm Helps",
        description: "All binaural conditions similar, all better than silence",
        supported: false, // Need to check all binaural vs silence
        evidence: "Check data"
      }
    };
  }, [comparisons]);

  // Get past results
  const pastResults = useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem('resonanceResultsV2') || '[]');
    } catch {
      return [];
    }
  }, []);

  return (
    <div className="container fade-in" style={{ paddingTop: '2rem', maxWidth: '900px' }}>
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
          Frequency Specificity Test Complete
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Session #{pastResults.length} • 8 conditions tested
        </p>
      </div>

      {/* Hypothesis Results */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ 
          fontSize: '0.875rem', 
          color: 'var(--text-muted)', 
          marginBottom: '1rem',
          textTransform: 'uppercase',
          letterSpacing: '0.05em'
        }}>
          Hypothesis Testing
        </h3>
        
        <div style={{ display: 'grid', gap: '1rem' }}>
          {Object.entries(hypotheses).map(([key, h]) => (
            <div key={key} style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '1rem',
              padding: '1rem',
              background: 'var(--bg-tertiary)',
              borderRadius: '8px',
              borderLeft: `4px solid ${h.supported ? 'var(--accent-green)' : h.evidence === 'Partial' ? 'var(--accent-yellow)' : 'var(--text-muted)'}`
            }}>
              <div style={{
                width: '24px',
                height: '24px',
                borderRadius: '50%',
                background: h.supported ? 'var(--accent-green)' : h.evidence === 'Partial' ? 'var(--accent-yellow)' : 'var(--bg-secondary)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.75rem',
                flexShrink: 0
              }}>
                {h.supported ? '✓' : h.evidence === 'Partial' ? '~' : '—'}
              </div>
              <div>
                <div style={{ fontWeight: 500, marginBottom: '0.25rem' }}>{h.label}</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{h.description}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Key Comparisons */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ 
          fontSize: '0.875rem', 
          color: 'var(--text-muted)', 
          marginBottom: '1rem',
          textTransform: 'uppercase',
          letterSpacing: '0.05em'
        }}>
          Key Comparisons
        </h3>
        
        <table className="results-table" style={{ fontSize: '0.85rem' }}>
          <thead>
            <tr>
              <th>Comparison</th>
              <th>Accuracy Δ</th>
              <th>Effect Size (d)</th>
              <th>Interpretation</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>40 Hz</strong> vs Control</td>
              <td style={{ color: comparisons.targetVsControl.accuracyDiff > 0 ? 'var(--accent-green)' : 'var(--accent-magenta)' }}>
                {comparisons.targetVsControl.accuracyDiff > 0 ? '+' : ''}{comparisons.targetVsControl.accuracyDiff.toFixed(1)}%
              </td>
              <td>{Math.abs(comparisons.targetVsControl.cohensD).toFixed(2)}</td>
              <td style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                {comparisons.targetVsControl.accuracyDiff > 10 ? 'Strong entrainment' :
                 comparisons.targetVsControl.accuracyDiff > 3 ? 'Possible entrainment' :
                 comparisons.targetVsControl.accuracyDiff < -3 ? 'Possible disruption' : 'No effect'}
              </td>
            </tr>
            <tr>
              <td><strong>40 Hz</strong> vs Near-misses (38/42)</td>
              <td style={{ color: comparisons.targetVsNearMiss.accuracyDiff > 0 ? 'var(--accent-green)' : 'var(--text-muted)' }}>
                {comparisons.targetVsNearMiss.accuracyDiff > 0 ? '+' : ''}{comparisons.targetVsNearMiss.accuracyDiff.toFixed(1)}%
              </td>
              <td>{Math.abs(comparisons.targetVsNearMiss.cohensD).toFixed(2)}</td>
              <td style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                {comparisons.targetVsNearMiss.accuracyDiff > 10 ? 'Frequency-specific!' :
                 comparisons.targetVsNearMiss.accuracyDiff > 3 ? 'Possibly specific' : 'Not frequency-specific'}
              </td>
            </tr>
            <tr>
              <td><strong>40 Hz</strong> vs Harmonics (20/80)</td>
              <td style={{ color: Math.abs(comparisons.targetVsHarmonic.accuracyDiff) < 5 ? 'var(--accent-cyan)' : 'var(--text-muted)' }}>
                {comparisons.targetVsHarmonic.accuracyDiff > 0 ? '+' : ''}{comparisons.targetVsHarmonic.accuracyDiff.toFixed(1)}%
              </td>
              <td>{Math.abs(comparisons.targetVsHarmonic.cohensD).toFixed(2)}</td>
              <td style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                {Math.abs(comparisons.targetVsHarmonic.accuracyDiff) < 5 ? 'Harmonics equivalent!' :
                 Math.abs(comparisons.targetVsHarmonic.accuracyDiff) < 10 ? 'Harmonics similar' : 'Harmonics different'}
              </td>
            </tr>
            <tr>
              <td>Control vs <strong>Near-misses</strong></td>
              <td style={{ color: comparisons.nearMissVsControl.accuracyDiff > 0 ? 'var(--accent-magenta)' : 'var(--text-muted)' }}>
                {comparisons.nearMissVsControl.accuracyDiff > 0 ? '-' : '+'}{Math.abs(comparisons.nearMissVsControl.accuracyDiff).toFixed(1)}%
              </td>
              <td>{Math.abs(comparisons.nearMissVsControl.cohensD).toFixed(2)}</td>
              <td style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                {comparisons.nearMissVsControl.accuracyDiff > 5 ? 'Near-miss interferes!' :
                 comparisons.nearMissVsControl.accuracyDiff > 0 ? 'Slight interference' : 'No interference'}
              </td>
            </tr>
          </tbody>
        </table>
        
        <div style={{ marginTop: '1rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          Effect size: |d| &lt; 0.2 = negligible, 0.2-0.5 = small, 0.5-0.8 = medium, &gt; 0.8 = large
        </div>
      </div>

      {/* Per-Condition Results */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ 
          fontSize: '0.875rem', 
          color: 'var(--text-muted)', 
          marginBottom: '1rem',
          textTransform: 'uppercase',
          letterSpacing: '0.05em'
        }}>
          All Conditions
        </h3>
        
        <table className="results-table">
          <thead>
            <tr>
              <th>Condition</th>
              <th>Type</th>
              <th>Accuracy</th>
              <th>Mean Time</th>
              <th>CV%</th>
            </tr>
          </thead>
          <tbody>
            {[1, 2, 3, 4, 5, 6, 7, 8].map(phase => {
              const stats = phaseStats[phase];
              if (!stats) return null;
              const cond = stats.condition;
              
              const typeColors = {
                control: 'var(--text-muted)',
                target: 'var(--accent-green)',
                near_miss: 'var(--accent-yellow)',
                harmonic: 'var(--accent-cyan)',
                unrelated: 'var(--accent-purple)'
              };
              
              return (
                <tr key={phase}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span style={{ 
                        width: '8px', 
                        height: '8px', 
                        borderRadius: '50%',
                        background: typeColors[cond?.type] || 'var(--text-muted)'
                      }}></span>
                      <div>
                        <div style={{ fontWeight: 500 }}>{cond?.name}</div>
                        {cond?.frequency && typeof cond.frequency === 'number' && (
                          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                            {cond.frequency} Hz
                          </div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td>
                    <span style={{
                      padding: '0.125rem 0.5rem',
                      borderRadius: '4px',
                      fontSize: '0.7rem',
                      background: `${typeColors[cond?.type]}22`,
                      color: typeColors[cond?.type]
                    }}>
                      {cond?.type?.replace('_', ' ')}
                    </span>
                  </td>
                  <td style={{ 
                    fontWeight: phase === 3 ? 600 : 400,
                    color: phase === 3 ? 'var(--accent-green)' : 'inherit'
                  }}>
                    {stats.correct}/{stats.total} ({stats.accuracy.toFixed(0)}%)
                  </td>
                  <td>{stats.meanTime.toFixed(2)}s</td>
                  <td>{stats.cv.toFixed(1)}%</td>
                </tr>
              );
            })}
          </tbody>
        </table>
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
          What This Means
        </h3>
        
        <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.7 }}>
          {hypotheses.gammaSpecific.supported ? (
            <p style={{ marginBottom: '1rem', color: 'var(--accent-green)' }}>
              <strong>✓ Strong evidence for gamma-specific entrainment!</strong> 40 Hz outperformed both control conditions and near-miss frequencies.
            </p>
          ) : hypotheses.gammaSpecific.evidence === 'Partial' ? (
            <p style={{ marginBottom: '1rem', color: 'var(--accent-yellow)' }}>
              <strong>~ Partial evidence for gamma entrainment.</strong> 40 Hz showed some benefit, but not clearly frequency-specific. More sessions needed.
            </p>
          ) : (
            <p style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>
              <strong>— No clear gamma entrainment effect</strong> in this session. This could be due to individual variation, noise, or the effect may be smaller than detectable with N=1.
            </p>
          )}

          {hypotheses.harmonicsHelp.supported && (
            <p style={{ marginBottom: '1rem', color: 'var(--accent-cyan)' }}>
              <strong>✓ Harmonic relationship detected!</strong> 20 Hz (subharmonic) and 80 Hz (overtone) performed similarly to 40 Hz. This supports the hypothesis that frequency ratios matter.
            </p>
          )}

          {hypotheses.nearMissInterferes.supported && (
            <p style={{ marginBottom: '1rem', color: 'var(--accent-magenta)' }}>
              <strong>✓ Near-miss interference detected!</strong> 38 Hz and 42 Hz (just off gamma) performed worse than control. This suggests off-frequency stimulation may actively disrupt binding.
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
            <strong>Important:</strong> Single-session results are noisy. Run 5-10 sessions minimum for reliable conclusions. 
            Effect sizes (Cohen's d) are more reliable than raw percentages for small samples.
            <br/><br/>
            Sessions recorded: {pastResults.length}
          </p>
        </div>
      </div>

      {/* Phase Order */}
      <div style={{ 
        fontSize: '0.75rem', 
        color: 'var(--text-muted)', 
        textAlign: 'center',
        marginBottom: '1.5rem',
        fontFamily: 'IBM Plex Mono'
      }}>
        Phase order: {phaseOrder.map(p => CONDITIONS[p]?.name || p).join(' → ')}
      </div>

      {/* Actions */}
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
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
            a.download = `frequency-specificity-results-${Date.now()}.json`;
            a.click();
          }}
        >
          Export All Data
        </button>
      </div>

      {/* Raw Data */}
      <details style={{ marginTop: '2rem' }}>
        <summary style={{ 
          cursor: 'pointer', 
          color: 'var(--text-muted)',
          fontSize: '0.875rem',
          marginBottom: '1rem'
        }}>
          View Raw Data
        </summary>
        <div style={{ 
          background: 'var(--bg-tertiary)', 
          padding: '1rem', 
          borderRadius: '8px',
          fontFamily: 'IBM Plex Mono',
          fontSize: '0.7rem',
          overflowX: 'auto'
        }}>
          <pre style={{ margin: 0 }}>
            {JSON.stringify({
              phaseOrder,
              comparisons: {
                targetVsControl: { ...comparisons.targetVsControl, tTest: undefined },
                targetVsNearMiss: { ...comparisons.targetVsNearMiss, tTest: undefined },
                targetVsHarmonic: { ...comparisons.targetVsHarmonic, tTest: undefined },
                nearMissVsControl: { ...comparisons.nearMissVsControl, tTest: undefined }
              },
              phases: Object.fromEntries(
                Object.entries(results.phases).map(([phase, data]) => [
                  `${phase}: ${CONDITIONS[phase]?.name}`,
                  {
                    correct: data.correct,
                    total: data.times?.length || 0,
                    accuracy: data.times?.length ? ((data.correct / data.times.length) * 100).toFixed(1) + '%' : 'N/A',
                    times: data.times?.map(t => t.toFixed(3)) || []
                  }
                ])
              )
            }, null, 2)}
          </pre>
        </div>
      </details>
    </div>
  );
}

export default ResultsDashboard;
