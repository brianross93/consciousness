# Consciousness Investigation

**Computational exploration of the Penrose-Hameroff Orch-OR hypothesis and thermodynamic models of neural decision-making.**

**Important** Please read free_will_investigation_synthesis! , or drop it into an LLM, to understand more why this specific model is being tested.

also, messing around with the resonance tester. It's not core to the theory, just messing around with it.

This project investigates whether quantum effects in microtubules could provide a mechanism for consciousness and free will, using thermodynamic simulations (THRML), Monte Carlo analysis, and examination of existing experimental data.

---

## Neuroanatomical Reference

The following brain map illustrates the neural pathways, neurotransmitter systems, and anatomical structures discussed throughout this investigation:

![Brain Map - Neural Pathways and Structures](brainmap.png)

*Source: [The Highest of the Mountains - Brain Maps](https://thehighestofthemountains.com/brainmaps.html) - Comprehensive neuroanatomy reference showing cortical regions, subcortical structures, neurotransmitter systems, and sensory/motor pathways.*

---

## Overview

The central question: **Can quantum effects in the brain be amplified through thermodynamic criticality to influence macroscopic behavior?**

We test this through:
1. **OR Collapse Scaling** - Do Penrose's objective reduction timescales match neural processing?
2. **Thermodynamic Simulation (THRML)** - Does quantum-like bias at hub nodes produce statistically significant shifts in network dynamics?
3. **Monte Carlo Avalanche Analysis** - Can quantum bias be distinguished from classical stochastic noise?
4. **Xenon Isotope Analysis** - Does existing experimental data support quantum effects on consciousness?
5. **Biological Verification** - Do simulation parameters match real brain biology?

---

## Key Findings

| Finding | Status | Source | Significance |
|---------|--------|--------|--------------|
| OR timescales match neural (tau ~ 0.1s for 10^10 tubulins) | Confirmed | Calculation | Mechanism is biologically plausible |
| 10% hub bias -> 60% global shift at criticality | **Confirmed (p < 0.0001)** | THRML (Gibbs) | Thermodynamic amplification works |
| Bidirectional control (amplify/veto both work) | Confirmed | THRML + Monte Carlo | Supports "free will" AND "free won't" |
| Quantum bias != classical mimic (skewness differs) | Confirmed (p < 0.05) | Monte Carlo | Selective bias produces distinct dynamics |
| Model matches real neural data (hc-3, α ≈ 1.6) | **Validated** | Monte Carlo | Simulation dynamics match hippocampal recordings |
| Pulsed bias preserves criticality (constant doesn't) | Demonstrated | Epoch-based MC | Matches actual OR timing |
| Entropy distinguishes conditions under pulsed bias | Demonstrated | Epoch-based MC | Q(+) higher, Q(-) lower than baseline |
| L5p neurons as primary site | **Strong** | Literature | Anesthesia decouples L5p (Suzuki & Larkum 2020) |
| Xenon isotope spin effect (~20% potency difference) | Experimental | Literature | Direct evidence quantum properties affect consciousness |
| Brain criticality is empirically established | Literature | Literature | Neural avalanches follow power laws (Beggs & Plenz 2003+) |

---

## Simulations

### 0. UNIFIED TEST (`unified_quantum_test.py`) - DEFINITIVE

**The end-to-end rigorous test.** Combines everything:

| Component | Method |
|-----------|--------|
| Sampling | True Gibbs (THRML) — not Monte Carlo approximation |
| Bias dynamics | Epoch-based pulsed — matching actual OR collapse timing |
| Calibration | hc-3 hippocampal data (α ≈ 1.6) |
| Conditions | Classical, Q(+), Q(-), Mimic |
| Statistics | t-tests, entropy analysis, bidirectionality check |

**What it tests:**
1. Coherent phase (no bias) → Collapse → Effect phase (bias pulse)
2. Does Q(+) > Classical > Q(-) in magnetization?
3. Does Q(+) differ from Mimic (structured vs uniform bias)?
4. Does the system preserve criticality (α ≈ 1.6)?

**Pass criteria:**
- [x] Bidirectional control (Q+ and Q- both work)
- [x] Statistically significant (p < 0.05)
- [x] Differs from uniform noise (Mimic condition)
- [x] Preserves criticality (matches real neural data)

```powershell
pip install thrml jax jaxlib
python unified_quantum_test.py
```

**Output:** `data/unified_test/unified_test_*.csv`, `data/unified_test/verdict_*.txt`

---

### 1. Thermodynamic Brain Simulation (`thrml_brain_sim.py`)

**Constant-bias Gibbs sampling.** Uses Extropic's [THRML library](https://github.com/extropic-ai/thrml) for true thermodynamic (Gibbs) sampling.

**What it does:**
- Creates small-world network (100 nodes, Watts-Strogatz topology)
- Automatically finds critical temperature (maximum susceptibility)
- Compares Classical vs Quantum(+) vs Quantum(-) conditions
- Applies bias only to 10 hub nodes (10% of network)

**Key results:**
- Classical: mean magnetization ~ 0 (fluctuating)
- Quantum(+): mean magnetization +0.61 (network pushed positive)
- Quantum(-): mean magnetization -0.60 (network pushed negative)
- **p < 0.0001** for both comparisons

```powershell
pip install thrml jax jaxlib
python thrml_brain_sim.py
```

**Output:** `data/thrml_experiment/thrml_results_*.png`

---

### 2. OR Collapse Time Scaling (`or_collapse_scaling.py`)

Tests whether Penrose's Objective Reduction (OR) collapse times can reach neural processing timescales.

**What it does:**
- Calculates collapse time: tau = hbar / E_g where E_g scales with tubulin ensemble size
- Plots tau vs N to show how ensemble size affects collapse time
- Highlights neural timescales (gamma rhythms ~100ms, decision windows ~500ms)

**Key result:** tau ~ 0.1-0.5s for brain-scale ensembles (10^10 tubulins) - matching neural timescales.

```powershell
python or_collapse_scaling.py
```

**Output:** `data/or_collapse_scaling/or_collapse_scaling.png`

---

### 3. Monte Carlo Avalanche Simulation (`quantum_avalanche_v3.py`)

Comprehensive Monte Carlo simulation with **constant bias** and four conditions.

**What it does:**
- 5000-node networks, 100 Monte Carlo runs
- Four conditions: Classical, Quantum(+), Quantum(-/veto), Classical Mimic
- OR-linked bias fraction (collapse time -> bias scaling)
- Statistical tests (t-tests on means and skewness)
- **Calibrated against hc-3 hippocampal recordings** (α ≈ 1.6)

**Key results:**
- Mimic vs Quantum(+) skew: p = 0.014 - Quantum produces different distribution shape
- Quantum(+) vs Quantum(-) mean: p < 0.001 - Bidirectional control confirmed
- Classical/Q(-) α ≈ 1.6 matches real neural avalanches

**Note:** Uses constant bias (applied every timestep). See epoch-based simulation for pulsed bias matching OR timing.

```powershell
python quantum_avalanche_v3.py
```

**Output:** `data/quantum_avalanche_v3/quantum_avalanche_v3_results.png`, CSV files

---

### 4. Epoch-Based Simulation (`quantum_avalanche_epochs.py`)

Models OR collapse as **discrete pulsed events** with accumulation phases — more realistic than constant bias.

**What it does:**
- Coherent phase (~160ms): No bias, superposition "building"
- Collapse event: OR threshold reached, bias "selected"
- Effect phase (~40ms): Bias pulse propagates through network
- Tracks entropy changes across epochs

**Key insight:** Constant bias (in tests 1 and 3) pushes Q(+) away from criticality. Pulsed bias (matching actual OR timing) preserves criticality while producing distinct entropy signatures.

**Key results:**
- Q(+) shows higher entropy than Classical
- Q(-) shows lower entropy than Classical
- Alpha values converge (all conditions remain near criticality)
- **Entropy, not alpha, distinguishes conditions under realistic OR timing**

```powershell
python quantum_avalanche_epochs.py
```

---

### 5. Xenon Isotope Analysis (`fetch_real_data.py`)

Analyzes existing experimental data on quantum effects in consciousness.

**What it does:**
- Analyzes xenon isotope anesthesia data (Li et al. Anesthesiology 2018)
- Shows nuclear spin (quantum property) affects anesthetic potency by ~20%

**Key finding:** Isotopes with nuclear spin require ~20% more xenon for anesthesia than spin-0 isotopes. Same chemistry, different quantum property -> different consciousness effect.

```powershell
python fetch_real_data.py
```

**Output:** `data/xenon_isotope_analysis/xenon_isotope_analysis.png`

---

### 5. Biological Verification (`tubulin_verification.py`)

Verifies that simulation parameters match real brain biology.

**What it does:**
- Calculates tubulin counts per neuron (~1.3 billion)
- Shows 10^10 tubulins = ~8-800 neurons (plausible local ensemble)
- Identifies Layer 5 Pyramidal (L5p) neurons as primary anatomical site

```powershell
python tubulin_verification.py
```

**Output:** `data/tubulin_verification.png`

---

### 6. Visualizations (`enhanced_brain_viz.py`, `brain_cascade_animation.py`)

Creates publication-quality figures and animations.

**Outputs:**
- `data/master_summary.png` - Single-image overview of entire argument
- `data/brain_cascade.gif` - Side-by-side cascade comparison animation
- `data/brain_2d_pulse.gif` - 2D brain with pulse effect
- `data/brain_3d_rotate.gif` - 3D rotating brain animation
- `data/brain_comparison_hq.png` - High-quality static comparison

```powershell
python enhanced_brain_viz.py
python brain_cascade_animation.py
```

---

### 7. Diagnostic Tools (`diagnostic_check.py`)

Parameter sensitivity analysis for the OR collapse formula.

```powershell
python diagnostic_check.py
```

---

## Installation

```powershell
# Clone the repository
git clone <repo-url>
cd consciousness

# Install dependencies
pip install numpy matplotlib networkx scipy pandas pillow

# For THRML simulation (recommended)
pip install thrml jax jaxlib
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `numpy` | Numerical computations |
| `matplotlib` | Plotting and visualization |
| `networkx` | Graph-based neural network models |
| `scipy` | Statistical tests |
| `pandas` | Data export (CSV) |
| `pillow` | GIF creation |
| `thrml` | Thermodynamic sampling (Extropic) |
| `jax` | Backend for THRML |

---

## Project Structure

```
consciousness/
|-- README.md                           # This file
|-- free_will_investigation_synthesis.md   # Detailed investigation (~2800 lines)
|-- script.md                           # Video script
|-- available_data_sources.md           # Data source documentation
|
|-- # Core Simulations
|-- thrml_brain_sim.py                  # THRML thermodynamic simulation (BEST)
|-- quantum_avalanche_v3.py             # Monte Carlo avalanche simulation
|-- or_collapse_scaling.py              # OR collapse time calculator
|-- fetch_real_data.py                  # Xenon isotope analysis
|-- tubulin_verification.py             # Biological parameter verification
|-- diagnostic_check.py                 # Parameter sensitivity analysis
|
|-- # Visualization
|-- enhanced_brain_viz.py               # Master summary, brain visualizations
|-- brain_cascade_animation.py          # Cascade comparison GIF
|
|-- # Output Data
|-- data/
    |-- thrml_experiment/               # THRML results (newest, strongest)
    |   |-- thrml_results_*.png
    |
    |-- quantum_avalanche_v3/           # Monte Carlo results
    |   |-- quantum_avalanche_v3_results.png
    |   |-- avalanche_sizes_*.csv
    |   |-- avalanche_stats_*.csv
    |
    |-- or_collapse_scaling/            # OR timescale graphs
    |   |-- or_collapse_scaling.png
    |
    |-- xenon_isotope_analysis/         # Real experimental data
    |   |-- xenon_isotope_analysis.png
    |   |-- synthetic_avalanche_*.csv
    |
    |-- # Visualizations
    |-- master_summary.png              # Single-image overview
    |-- brain_cascade.gif               # Cascade comparison animation
    |-- brain_2d_pulse.gif              # 2D animated cascade
    |-- brain_3d_rotate.gif             # 3D rotating brain
    |-- brain_comparison_hq.png         # Static comparison
    |-- tubulin_verification.png        # Biology verification
```

---

## Theoretical Framework

### The Thermodynamic Amplification Model

The brain operates as a **thermodynamic computer at criticality**:

```
ELECTRON SUPERPOSITION IN TUBULIN (d ~ 0.01 nm)
    | ~8-800 L5p neurons across cortex, ~160ms
GRAVITATIONAL SELF-ENERGY TRIGGERS OR COLLAPSE
    | selection occurs (non-deterministic)
ELECTRON POSITION DETERMINES LOCAL ELECTRIC FIELD
    | affects tubulin-MAP binding
MICROTUBULE STATE BIASES SYNAPTIC WEIGHTS
    | selective edges strengthened
NEURAL AVALANCHE TRIGGERED (thermodynamic amplification)
    | 10% hub bias -> 60% global effect at criticality
BEHAVIOR / CONSCIOUS DECISION
```

**Key insight:** You don't need brain-wide quantum coherence. Local quantum effects at hub nodes + thermodynamic amplification at criticality = biologically realistic mechanism.

### Why Criticality Matters

The brain operates at the **critical point** (edge of chaos):
- Maximum sensitivity to small perturbations
- Long-range correlations between neurons
- Power-law avalanche distributions (Beggs & Plenz 2003)

At criticality, small quantum biases have **maximum leverage**. This is why "quantum effects are too small" fails as an objection.

---

## Evidence Summary

### What We Demonstrated

**THRML (True Gibbs Sampling):**
1. **Thermodynamic amplification works** (p < 0.0001) — 10% hub bias → 60% network shift
2. **Bidirectional control** supports both free will AND "free won't"

**Monte Carlo (Constant Bias):**
3. **Model matches real neural data** (hc-3 hippocampal recordings, α ≈ 1.6)
4. **Quantum bias ≠ classical noise** (skewness differs, p < 0.05)

**Monte Carlo (Epoch-Based / Pulsed Bias):**
5. **Pulsed bias preserves criticality** — constant bias doesn't match OR dynamics
6. **Entropy distinguishes conditions** — Q(+) higher, Q(-) lower than baseline

**Calculations:**
7. **OR timescales match neural processing** (tau ~ 100-500ms for 10^10 tubulins)
8. **Parameters match biology** (10^10 tubulins = ~8-800 L5p neurons)

### What Remains Uncertain

1. Does quantum coherence actually persist in tubulins at 37C?
2. Does OR collapse actually occur? (2025 arXiv preprint reports OR-consistent results)
3. Are L5p neurons the actual site? (Strong evidence from anesthesia studies)
4. Is quantum indeterminacy "freedom" or just "randomness"?

### Current Confidence: higher than 50%

The **mechanism** is demonstrated. The **quantum source** remains to be proven experimentally.

---

## Key References

| Topic | Citation |
|-------|----------|
| Xenon isotope spin effect | Li et al. Anesthesiology 2018 |
| Neural avalanche criticality | Beggs & Plenz, J. Neuroscience (2003) |
| Brain criticality review | Cocchi et al. Prog Neurobiol (2017) |
| OR collapse mechanism | Penrose, "The Emperor's New Mind" (1989) |
| Orch-OR theory | Hameroff & Penrose, Physics of Life Reviews (2014) |
| L5p anesthesia mechanism | Suzuki & Larkum, Cell (2020) |
| Dendritic integration theory | Larkum, Trends Neurosci (2013) |
| Tryptophan superradiance | J. Phys. Chem. 2024 (PMID 38641327) |
| OR experiment | Tagg & Reid, arXiv:2504.02914 (2025) |
| THRML library | Extropic AI, github.com/extropic-ai/thrml |

---

## Proposed Experiments

### Tier 1 (Doable Now)
- Xenon isotope effects on decision-making (not just anesthesia)
- Temperature scaling of decision variability
- Magnetic field effects on decisions

### Tier 2 (Harder But Definitive)
- Leggett-Garg inequality violations in neural systems
- Gravitational manipulation of consciousness (microgravity)
- Direct tubulin coherence measurement

### Tier 3 (Foundational)
- Non-computability tests in human cognition
- Intervention + prediction studies

---

## License

Research and educational use. See individual papers for citation requirements.

---

*For the complete investigation with all details, see `free_will_investigation_synthesis.md` (~2800 lines)*
