# Consciousness Resonance Tester

**A cognitive experiment testing whether gamma-band audio interference affects cognitive binding.**

## Hypothesis

The brain uses **gamma oscillations (~40 Hz)** to bind separate features into unified percepts. If we can disrupt this binding with interfering frequencies — or enhance it with entrainment — we should see measurable effects on cognitive performance.

| Condition | Prediction |
|-----------|------------|
| **Silence** | Baseline performance |
| **Pink Noise** | Slight distraction (non-specific) |
| **74 Hz Tone** | Reduced accuracy, increased variance (γ×2 interference) |
| **70-90 Hz Sweep** | Reduced accuracy, increased variance (adaptive interference) |
| **40 Hz Binaural** | Maintained or improved performance (entrainment) |

---

## Theoretical Background

### Gamma Binding

Gamma oscillations (30-100 Hz, centered ~40 Hz) are associated with:
- **Feature binding** — integrating color, shape, motion into unified objects
- **Conscious perception** — gamma power correlates with awareness
- **Working memory** — maintaining information across time

**Key insight:** Gamma operates in a narrow frequency band. Stimulation at *exactly* 40 Hz may entrain (enhance), while *near* 40 Hz (e.g., 37 Hz, 74 Hz) may interfere.

### Why Harmonics?

We use 74 Hz and 70-90 Hz (the 2nd harmonic of gamma) instead of 37 Hz and 35-45 Hz because:
1. **Sub-50 Hz is hard for headphones** — causes distortion/clipping, especially with Bluetooth + ANC
2. **Harmonics carry the same information** — if 40 Hz is the fundamental, 80 Hz (×2) is its harmonic
3. **Same interference principle** — 74 Hz is "off" from 80 Hz the same way 37 Hz is "off" from 40 Hz

### Why Binaural for Entrainment?

The 40 Hz entrainment phase uses **binaural beats** (200 Hz left ear, 240 Hz right ear):
- The 40 Hz beat is generated *inside the brain* at the superior olivary complex
- This may be more effective at entraining cortical gamma than direct acoustic stimulation
- Uses comfortable mid-range frequencies instead of low rumble

---

## Experimental Design

### 5 Phases (Randomized Order)

| Phase | Audio | Frequency | Method | Purpose |
|-------|-------|-----------|--------|---------|
| 1 | Silence | — | — | Baseline |
| 2 | Pink Noise | Broadband | Monaural | Non-specific distraction control |
| 3 | 74 Hz Tone | 74 Hz | Monaural | Fixed γ×2 interference |
| 4 | 70-90 Hz Sweep | 70-90 Hz | Monaural | Adaptive γ×2 interference |
| 5 | 40 Hz Binaural | 200/240 Hz | Binaural | Gamma entrainment |

- **10 questions per phase** (50 total)
- **Stratified difficulty:** 4 easy + 3 moderate + 3 hard per phase
- **Phase order randomized** each session to control for fatigue/learning
- **Question options shuffled** so correct answer position varies (A/B/C/D)

### Question Types

- **Sequence patterns:** 2, 4, 8, 16, ... → ?
- **Letter patterns:** A, C, E, G, ... → ?
- **Analogies:** Doctor : Patient :: Teacher : ?
- **Logic puzzles:** If all X are Y, and Z is X, then...

These require **cognitive binding** — integrating pattern elements into a unified understanding.

---

## Metrics Collected

| Metric | What It Measures |
|--------|------------------|
| **Accuracy** | Correct answers / total |
| **Mean Response Time** | Average time per question |
| **Response Time Variance** | Consistency of processing speed |
| **Coefficient of Variation** | Normalized variance (σ/μ) |

### Key Comparisons

1. **Disruption Effect:** Control (Silence + Noise) vs. Interference (74 Hz + Sweep)
2. **Entrainment Effect:** Control vs. 40 Hz Binaural
3. **Variance Analysis:** Does interference increase response time variability?

---

## Running the Experiment

### Prerequisites

- Node.js 18+
- Modern browser (Chrome/Firefox/Edge)
- **Headphones required** (binaural beats won't work with speakers)

### Installation

```bash
cd consciousness-resonance-tester
npm install
npm run dev
```

Open http://localhost:5173

### Taking the Test

1. **Wear headphones** — required for binaural beats and low frequencies
2. **Disable ANC if possible** — active noise cancellation can interfere with tones
3. **Find a quiet environment** — minimize external distractions
4. **Complete all 5 phases** — takes 12-18 minutes
5. **Run multiple sessions** — single sessions have high noise

---

## Interpreting Results

### Dashboard Metrics

| Metric | Good Signal | Meaning |
|--------|-------------|---------|
| **Disruption Effect > 5%** | ✓ | Interference reduced accuracy |
| **Entrainment Boost > 3%** | ✓ | 40 Hz improved performance |
| **Variance Ratio > 1.3×** | ✓ | Interference destabilized processing |

### What Supports the Hypothesis?

**Strong support:**
- Accuracy: Control > Interference > Entrainment (or Control ≈ Entrainment)
- Variance: Interference >> Control ≈ Entrainment
- Effect specific to gamma-band, not just "any sound"

**Weak/no support:**
- All conditions perform similarly
- Pink noise as disruptive as gamma interference
- High individual variability across sessions

---

## Data Storage

Results are saved to `localStorage` and can be exported as JSON:

```json
{
  "sessionId": 1766210554728,
  "timestamp": "2025-12-20T06:13:10.508Z",
  "phaseOrder": [1, 3, 5, 2, 4],
  "results": {
    "phases": {
      "1": { "correct": 9, "times": [...], "questions": [...] },
      ...
    }
  }
}
```

Click **"Export All Data"** on the results screen to download.

---

## Technical Implementation

### Audio Engine

```
┌─────────────────────────────────────────────────────────┐
│ Web Audio API                                           │
├─────────────────────────────────────────────────────────┤
│ Pink Noise:   Buffer → LowPass Filter → Gain → Output   │
│ 74 Hz Tone:   Oscillator → Gain → Compressor → Output   │
│ Sweep:        Oscillator + LFO → Gain → Compressor      │
│ Binaural:     OscL → GainL ─┐                           │
│               OscR → GainR ─┼→ Merger → Compressor      │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack

- **React 18** — UI framework
- **Vite** — Build tool
- **Web Audio API** — Precise audio generation
- **localStorage** — Result persistence

---

## Limitations

1. **N=1 problem:** Individual sessions have high variance. Need multiple sessions or participants.
2. **No EEG verification:** We assume gamma is affected but don't measure it directly.
3. **Headphone dependency:** Effect may vary with headphone quality/type.
4. **Learning effects:** Participants may improve at the question types over time.
5. **Placebo possible:** Knowing which condition is "supposed" to hurt may influence performance.

---

## Related Research

| Study | Finding |
|-------|---------|
| Tsai Lab (MIT) | 40 Hz light/sound reduces amyloid in Alzheimer's models |
| Tallon-Baudry et al. | Gamma correlates with feature binding in perception |
| Garcia-Argibay (2019) | Meta-analysis: small but significant binaural beat effects |
| Reedijk et al. (2015) | Individual differences in binaural beat response |

---

## Future Improvements

- [ ] Add EEG integration to measure actual gamma changes
- [ ] Test original 37 Hz / 35-45 Hz with wired headphones
- [ ] Add more question types (spatial reasoning, Stroop task)
- [ ] Implement double-blind mode (randomized condition labels)
- [ ] Add statistical analysis (t-tests, effect sizes) to results dashboard

---

## License

Research and educational use. Part of the [Consciousness Investigation](../README.md) project.

---

*Testing the gamma binding hypothesis through behavioral measurement.*

