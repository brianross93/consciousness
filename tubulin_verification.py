"""
Tubulin Count Verification
==========================

Verify that our simulation parameters match biological reality.
Based on literature values for tubulin counts in neurons.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# =============================================================================
# BIOLOGICAL CONSTANTS (from literature)
# =============================================================================

# Tubulin dimers per microtubule per micron
DIMERS_PER_MICRON = 1625  # BioNumbers database

# Microtubules in a typical neuron
# Pyramidal neurons have extensive dendritic arbors
# Estimated total MT length varies by cell type

# From NeuroQuantology paper:
TUBULINS_PER_NEURON = 1.3e9  # Adult pyramidal neuron

# Human brain neuron count (Azevedo et al.)
NEURONS_IN_BRAIN = 86e9

# Total tubulins in brain
TOTAL_BRAIN_TUBULINS = TUBULINS_PER_NEURON * NEURONS_IN_BRAIN  # ~10^20

# Our simulation parameter
SIMULATION_N = 1e10

# =============================================================================
# ANALYSIS
# =============================================================================

def main():
    print("=" * 70)
    print("TUBULIN COUNT VERIFICATION")
    print("=" * 70)
    print()
    
    print("BIOLOGICAL REFERENCE VALUES:")
    print("-" * 50)
    print(f"  Tubulin dimers per neuron:     {TUBULINS_PER_NEURON:.2e}")
    print(f"  Neurons in human brain:        {NEURONS_IN_BRAIN:.2e}")
    print(f"  Total brain tubulins:          {TOTAL_BRAIN_TUBULINS:.2e}")
    print()
    
    print("OUR SIMULATION PARAMETER:")
    print("-" * 50)
    print(f"  N_tubulins for OR collapse:    {SIMULATION_N:.2e}")
    print()
    
    # What fraction of brain?
    fraction_of_brain = SIMULATION_N / TOTAL_BRAIN_TUBULINS
    print(f"  Fraction of total brain:       {fraction_of_brain:.2e} ({fraction_of_brain*100:.8f}%)")
    print()
    
    # Equivalent neuron counts at different coherence fractions
    print("EQUIVALENT NEURON INVOLVEMENT:")
    print("-" * 50)
    print("(How many neurons needed if X% of their tubulins are coherent)")
    print()
    
    coherence_fractions = [1.0, 0.1, 0.01, 0.001, 0.0001]
    
    results = []
    for frac in coherence_fractions:
        coherent_per_neuron = TUBULINS_PER_NEURON * frac
        neurons_needed = SIMULATION_N / coherent_per_neuron
        results.append((frac, neurons_needed))
        print(f"  {frac*100:6.2f}% coherent per neuron -> {neurons_needed:,.0f} neurons involved")
    
    print()
    
    # OR collapse time check
    print("OR COLLAPSE TIME CHECK:")
    print("-" * 50)
    
    hbar = 1.0545718e-34  # J*s
    G = 6.67430e-11       # gravitational constant
    m = 1e-22             # kg per tubulin (approximate)
    d = 1e-11             # m (0.01 nm separation)
    
    N_values = [1e8, 1e9, 1e10, 1e11, 1e12]
    
    print(f"  (Using d = {d*1e9:.3f} nm, m = {m*1e22:.1f}x10^-22 kg)")
    print()
    
    for N in N_values:
        E_g = N * (G * m**2 / d)
        tau = hbar / E_g
        neurons_equiv = N / TUBULINS_PER_NEURON
        print(f"  N = {N:.0e} tubulins ({neurons_equiv:6.1f} neurons) -> tau = {tau:.3f} s ({tau*1000:.0f} ms)")
    
    print()
    
    # Biological plausibility assessment
    print("BIOLOGICAL PLAUSIBILITY ASSESSMENT:")
    print("-" * 50)
    print()
    
    print("  FOR 10^10 tubulins coherent:")
    print()
    print("  Scenario A: Dense local ensemble")
    print("    - ~8 neighboring neurons, 100% MT coherence")
    print("    - Connected via gap junctions")
    print("    - Plausibility: MODERATE (gap junctions exist)")
    print()
    print("  Scenario B: Sparse distributed ensemble")  
    print("    - ~8,000 neurons, 0.1% MT coherence each")
    print("    - Partial coherence in many cells")
    print("    - Plausibility: LOWER (coordination harder)")
    print()
    print("  Scenario C: Cortical column scale")
    print("    - ~80-800 neurons in a minicolumn")
    print("    - 1-10% MT coherence per neuron")
    print("    - Plausibility: MODERATE (columns are functional units)")
    print()
    
    # What does literature say about coherence?
    print("LITERATURE SUPPORT:")
    print("-" * 50)
    print("""
    1. Tryptophan superradiance (2024, PMID 38641327):
       - Evidence of collective quantum behavior in MT tryptophans
       - Suggests SOME quantum coherence possible at warm temps
       
    2. Anesthesia-MT link (2024, PMID 39147581):
       - MT stabilizers affect anesthetic response
       - MTs involved in consciousness mechanism
       
    3. Gap junctions and coherence:
       - Gap junctions electrically couple neurons
       - Could potentially allow coherence to span cells
       - Hameroff has argued for this mechanism
       
    4. Decoherence estimates:
       - Naive thermal estimates: femtoseconds (too fast)
       - Tegmark (2000): argued against quantum brain
       - Counter: protected environments, quantum error correction
       - Debate ongoing
    """)
    
    # Create visualization
    print("\nGenerating visualization...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#1a1a2e')
    
    # Left: Tubulin count scales
    ax1 = axes[0]
    ax1.set_facecolor('#1a1a2e')
    
    scales = ['Single\nTubulin', 'Single\nMT', 'Single\nNeuron', 'Our\nSimulation', 'Cortical\nColumn', 'Whole\nBrain']
    values = [1, 1625*10, TUBULINS_PER_NEURON, SIMULATION_N, TUBULINS_PER_NEURON*1000, TOTAL_BRAIN_TUBULINS]
    colors = ['#666666', '#888888', '#4fc3f7', '#ff7043', '#81c784', '#e1bee7']
    
    bars = ax1.bar(scales, values, color=colors, edgecolor='white', linewidth=1)
    ax1.set_yscale('log')
    ax1.set_ylabel('Number of Tubulin Dimers', fontsize=11, color='white')
    ax1.set_title('TUBULIN COUNT SCALES', fontsize=13, fontweight='bold', color='white')
    ax1.tick_params(colors='white')
    for spine in ax1.spines.values():
        spine.set_color('#3a3a5e')
    
    # Add value labels
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, val*2, f'{val:.0e}', 
                ha='center', va='bottom', fontsize=9, color='white')
    
    # Highlight our simulation
    ax1.axhline(y=SIMULATION_N, color='#ff7043', linestyle='--', alpha=0.7, linewidth=2)
    ax1.text(5.5, SIMULATION_N*1.5, 'Our N = 10^10', fontsize=10, color='#ff7043', ha='right')
    
    # Right: Neurons involved vs coherence fraction
    ax2 = axes[1]
    ax2.set_facecolor('#1a1a2e')
    
    fracs = np.logspace(-5, 0, 50)
    neurons = SIMULATION_N / (TUBULINS_PER_NEURON * fracs)
    
    ax2.loglog(fracs * 100, neurons, color='#4fc3f7', linewidth=2.5)
    ax2.axhline(y=100, color='#81c784', linestyle='--', alpha=0.7, label='~100 neurons (minicolumn)')
    ax2.axhline(y=10000, color='#ffd54f', linestyle='--', alpha=0.7, label='~10,000 neurons (column)')
    ax2.axvline(x=1, color='#ff7043', linestyle='--', alpha=0.7, label='1% coherence')
    
    ax2.set_xlabel('Coherence Fraction per Neuron (%)', fontsize=11, color='white')
    ax2.set_ylabel('Neurons Required for N=10^10', fontsize=11, color='white')
    ax2.set_title('NEURONS NEEDED vs COHERENCE LEVEL', fontsize=13, fontweight='bold', color='white')
    ax2.legend(fontsize=9, facecolor='#1a1a2e', edgecolor='#3a3a5e', labelcolor='white', loc='upper right')
    ax2.tick_params(colors='white')
    ax2.grid(True, alpha=0.2)
    for spine in ax2.spines.values():
        spine.set_color('#3a3a5e')
    
    # Fill plausible region
    ax2.fill_between([0.1, 10], [1, 1], [1e8, 1e8], alpha=0.15, color='#81c784')
    ax2.text(1, 500, 'Plausible\nRange', fontsize=10, color='#81c784', ha='center', fontweight='bold')
    
    plt.tight_layout()
    os.makedirs('data', exist_ok=True)
    plt.savefig('data/tubulin_verification.png', dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
    print("[OK] Saved: data/tubulin_verification.png")
    plt.close()
    
    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Our simulation uses N = 10^10 tubulins.
    
    This represents:
    - ~8 neurons if 100% of their MTs are coherent
    - ~800 neurons if 1% of their MTs are coherent  
    - A tiny fraction (10^-10) of total brain tubulins
    
    Biological plausibility: MODERATE
    - Requires either very local dense coherence, OR
    - Sparse partial coherence across many neurons
    - Gap junctions could enable inter-neuron coherence
    - Some experimental support from recent MT studies
    
    The parameter is NOT arbitrary - it's chosen to hit neural timescales
    AND represents a plausible local neural ensemble.
    """)


if __name__ == "__main__":
    main()
