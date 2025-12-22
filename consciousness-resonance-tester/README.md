# Frequency Specificity Test

**Testing whether gamma (40 Hz) entrainment is frequency-specific or if any rhythmic stimulus helps cognitive binding.**

## Research Question

The brain uses gamma oscillations (~40 Hz) for feature binding and conscious perception. External stimulation at 40 Hz (gamma entrainment) has shown effects in some studies. But is this effect:

1. **Frequency-specific?** Only 40 Hz helps, other frequencies don't
2. **Harmonic?** Related frequencies (20 Hz, 80 Hz) also help
3. **Non-specific?** Any rhythmic stimulus improves performance
4. **Interfering?** Near-miss frequencies (38 Hz, 42 Hz) actually hurt

This experiment tests all four hypotheses.

---

## Experimental Design

### 8 Conditions (Randomized Order)

| Condition | Type | Frequency | Hypothesis |
|-----------|------|-----------|------------|
| Silence | Control | — | Baseline |
| Pink Noise | Control | Broadband | Non-specific distraction |
| **40 Hz Binaural** | **Target** | 40 Hz | Should enhance binding |
| 38 Hz Binaural | Near-miss | 38 Hz | Should interfere |
| 42 Hz Binaural | Near-miss | 42 Hz | Should interfere |
| 80 Hz Binaural | Harmonic | 80 Hz | Test octave relationship |
| 20 Hz Binaural | Harmonic | 20 Hz | Test subharmonic |
| 53 Hz Binaural | Unrelated | 53 Hz | Control for "any frequency" |

### Per Phase
- **3-minute pre-exposure**: Audio plays while participant relaxes (allows neural entrainment)
- **6 questions** per condition (3 easy, 2 moderate, 1 hard)
- **~6 minutes total** per condition (3 min pre-exposure + ~3 min questions)
- **48 questions total** + 3 practice
- **45-50 minutes** total duration
- **Stratified difficulty** to control for question difficulty across conditions

### Why Pre-Exposure?

Research shows neural entrainment requires time to stabilize:

| Duration | Effect |
|----------|--------|
| 6+ min | Full alpha entrainment (Thut et al., 2011) |
| 10-30 min | Effective gamma entrainment in clinical studies |
| 3 min | Minimum for measurable EEG changes |

Our 3-minute pre-exposure + ~3 minutes of questions provides ~6 minutes total exposure per condition—balancing scientific rigor with practical session length.

### Measures
- **Accuracy** (correct/total)
- **Response time** (mean, variance)
- **Coefficient of variation** (consistency)
- **Cohen's d** (effect size for comparisons)

---

## Hypotheses & Predictions

| Hypothesis | If True, We Should See |
|------------|----------------------|
| **Gamma-specific** | 40 Hz > all others (accuracy & speed) |
| **Harmonics matter** | 40 Hz ≈ 80 Hz ≈ 20 Hz (octave relationships) |
| **Any rhythm helps** | All binaural ≈ each other > silence |
| **Near-miss interferes** | 38/42 Hz < control (disrupts natural gamma) |

---

## Connection to Consciousness Theory

This experiment tests a key prediction of the thermodynamic amplification model:

1. **Brain oscillations reflect criticality** — networks at the edge of chaos
2. **External entrainment can shift network state** — like the THRML simulation showed
3. **Frequency specificity would support** the idea that gamma (~40 Hz) is special for binding
4. **Harmonic relationships would support** the idea that phase/frequency ratios matter (connects to Euler-Fokker music theory)

---

## Running the Experiment

### Prerequisites
- Node.js 18+
- Modern browser (Chrome/Firefox/Edge)
- **Stereo headphones** (binaural beats require different frequencies in each ear)

### Installation

```powershell
cd consciousness-resonance-tester
npm install
npm run dev
```

Open http://localhost:5173

### Taking the Test

1. **Wear stereo headphones** — required for binaural beats
2. **Disable ANC** — active noise cancellation may interfere
3. **Quiet environment** — minimize distractions
4. **Complete all 8 phases** — takes 45-50 minutes
5. **Run 5-10 sessions** — single sessions are too noisy for conclusions

---

## Interpreting Results

### Key Comparisons

| Comparison | What It Tests |
|------------|---------------|
| 40 Hz vs Control | Does gamma entrainment work at all? |
| 40 Hz vs Near-miss (38/42) | Is the effect frequency-specific? |
| 40 Hz vs Harmonics (20/80) | Do octave relationships matter? |
| Control vs Near-miss | Does off-frequency stimulation interfere? |

### Effect Sizes (Cohen's d)

| d Value | Interpretation |
|---------|---------------|
| < 0.2 | Negligible |
| 0.2-0.5 | Small |
| 0.5-0.8 | Medium |
| > 0.8 | Large |

### What Supports Each Hypothesis?

**Gamma-specific entrainment:**
- 40 Hz accuracy > control by 10%+
- 40 Hz accuracy > near-miss by 10%+
- Effect size (d) > 0.5

**Harmonic relationships matter:**
- 40 Hz ≈ 80 Hz ≈ 20 Hz (within 5%)
- But all three > unrelated (53 Hz)

**Near-miss interference:**
- 38/42 Hz accuracy < control
- Higher response time variance for near-miss conditions

---

## Data Storage

Results saved to `localStorage` under key `resonanceResultsV2`:

```json
{
  "sessionId": 1703123456789,
  "timestamp": "2025-12-22T...",
  "phaseOrder": [3, 7, 1, 5, 2, 8, 4, 6],
  "conditions": { ... },
  "results": {
    "phases": {
      "1": { "correct": 5, "times": [...], "questions": [...] },
      ...
    }
  },
  "version": 2
}
```

Click **"Export All Data"** to download JSON for analysis.

---

## Technical Implementation

### Audio Engine

All binaural beats use 200 Hz base frequency:
- Left ear: 200 Hz
- Right ear: 200 Hz + beat frequency
- Brain perceives the difference as a beat

```
40 Hz binaural: Left=200 Hz, Right=240 Hz → 40 Hz beat
38 Hz binaural: Left=200 Hz, Right=238 Hz → 38 Hz beat
80 Hz binaural: Left=200 Hz, Right=280 Hz → 80 Hz beat
```

### Tech Stack
- **React 18** — UI
- **Vite** — Build
- **Web Audio API** — Precise audio generation
- **localStorage** — Result persistence

---

## Limitations

1. **N=1 per session** — need multiple sessions for statistical power
2. **No EEG verification** — we assume entrainment but don't measure it
3. **Headphone variability** — different headphones may reproduce frequencies differently
4. **Learning effects** — may improve at question types over sessions
5. **Expectation effects** — knowing hypothesis may bias results

### Mitigations
- Randomized phase order
- Stratified question distribution
- Effect size calculation (more robust than raw percentages)
- Multiple session aggregation

---

## Future Improvements

- [ ] Add EEG integration to verify entrainment
- [ ] Add HRV measurement for physiological correlate
- [ ] Test additional harmonic frequencies (60 Hz = 3:2 ratio)
- [ ] Add Stroop task for different binding measure
- [ ] Implement proper double-blind (fake condition names)
- [ ] Statistical power analysis for required sample size

---

## Related Research

| Study | Finding |
|-------|---------|
| Tsai Lab (MIT) | 40 Hz light/sound reduces amyloid in Alzheimer's |
| Tallon-Baudry et al. | Gamma correlates with feature binding |
| Garcia-Argibay (2019) | Meta-analysis: small but significant binaural effects |
| Beggs & Plenz (2003) | Neural avalanches follow power laws (criticality) |

---

## License

Research and educational use. Part of the [Consciousness Investigation](../README.md) project.

---

*Testing frequency specificity of gamma entrainment through behavioral measurement.*
