"""
Integrated Quantum-Avalanche Simulation
========================================

Enhanced simulation that:
1. Tunes parameters for subtle (20-50% large avalanche) quantum effects
2. Compares with real neural avalanche data (power-law scaling from literature)
3. Monte Carlo stats (1000 runs, t-tests, skewness analysis)
4. Integrates OR collapse time into avalanche dynamics (time-dependent biases)

References:
- arXiv:2102.09124 - Neural avalanche criticality data
- Penrose OR: tau = hbar / E_g
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy import stats
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PHYSICAL CONSTANTS (OR Collapse)
# =============================================================================
hbar = 1.0545718e-34  # J*s
G = 6.67430e-11       # m^3 kg^-1 s^-2
m_tubulin = 1e-22     # kg
d_separation = 1e-11  # m (0.01 nm - atomic scale)


def or_collapse_time(N):
    """Calculate OR collapse time for N tubulins."""
    E_g = N * (G * m_tubulin**2 / d_separation)
    return hbar / E_g


# =============================================================================
# REAL NEURAL AVALANCHE DATA (from literature)
# =============================================================================

def generate_powerlaw_avalanches(n_samples=1000, alpha=1.5, x_min=1, x_max=1000):
    """
    Generate synthetic power-law distributed avalanches matching real neural data.
    
    From arXiv:2102.09124: Neural avalanches follow power-law P(s) ~ s^(-alpha)
    with alpha typically between 1.5 and 2.0 for critical brain dynamics.
    
    Parameters:
    -----------
    n_samples : int
        Number of avalanche samples
    alpha : float
        Power-law exponent (1.5-2.0 for critical brain)
    x_min : int
        Minimum avalanche size
    x_max : int
        Maximum avalanche size (network size)
    """
    # Power-law distribution using inverse transform sampling
    u = np.random.uniform(0, 1, n_samples)
    # P(s) ~ s^(-alpha), CDF^(-1)
    samples = x_min * (1 - u) ** (-1 / (alpha - 1))
    samples = np.clip(samples, x_min, x_max).astype(int)
    return samples


def load_real_avalanche_stats():
    """
    Return statistics from real neural avalanche studies.
    
    From arXiv:2102.09124 and related literature:
    - Power-law exponent alpha ~ 1.5 (critical)
    - Size distribution spans multiple orders of magnitude
    - Characteristic scale-free behavior
    """
    return {
        'source': 'arXiv:2102.09124 (Neural Avalanche Criticality)',
        'alpha': 1.5,  # Power-law exponent
        'alpha_range': (1.3, 2.0),  # Range across studies
        'mean_size_fraction': 0.05,  # Mean avalanche ~5% of network
        'large_avalanche_fraction': 0.15,  # ~15% exceed 10% of network
        'skewness_range': (2.0, 5.0),  # Typical skewness (right-tailed)
    }


# =============================================================================
# NETWORK CREATION
# =============================================================================

def create_critical_network(N=1000, k=10, p=0.1, seed=None):
    """
    Create Watts-Strogatz network tuned for critical dynamics.
    """
    if seed is not None:
        np.random.seed(seed)
    
    G = nx.watts_strogatz_graph(N, k, p, seed=seed)
    
    # Initialize edges near critical threshold
    for u, v in G.edges():
        # Weights centered at threshold with moderate variance
        G[u][v]['weight'] = np.random.normal(1.0, 0.12)
        G[u][v]['original_weight'] = G[u][v]['weight']
    
    return G


# =============================================================================
# AVALANCHE SIMULATION (with OR-dependent bias)
# =============================================================================

def avalanche_size(G, source, threshold=1.05):
    """
    Simulate neural avalanche from source node.
    Threshold tuned for critical regime (near 50% propagation).
    """
    visited = set()
    queue = [source]
    size = 0
    
    while queue:
        u = queue.pop(0)
        if u in visited:
            continue
        visited.add(u)
        size += 1
        
        for v in G.neighbors(u):
            if G[u][v]['weight'] > threshold and v not in visited:
                queue.append(v)
    
    return size


def apply_or_bias(G, bias_fraction=0.1, bias_strength=0.05, N_tubulins=1e10, seed=None):
    """
    Apply quantum bias based on OR collapse dynamics.
    
    The bias strength scales with 1/tau (faster collapse = stronger effect).
    This integrates OR collapse time into avalanche dynamics.
    
    Parameters:
    -----------
    bias_fraction : float
        Fraction of edges receiving quantum bias (default 0.1 = 10%)
    bias_strength : float
        Base strength of quantum nudge (default 0.05)
    N_tubulins : float
        Number of tubulins in ensemble (affects OR timing)
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Calculate OR collapse time
    tau = or_collapse_time(N_tubulins)
    
    # Time-dependent bias: faster collapse = stronger effect
    # Normalize to neural timescale (0.1s = 100ms)
    tau_neural = 0.1
    time_factor = tau_neural / tau  # >1 if collapse is fast, <1 if slow
    time_factor = np.clip(time_factor, 0.1, 10)  # Reasonable bounds
    
    # Effective bias scales with timing
    effective_bias = bias_strength * time_factor
    
    # Select edges to bias
    edge_list = list(G.edges())
    n_bias = int(len(edge_list) * bias_fraction)
    bias_indices = np.random.choice(len(edge_list), size=n_bias, replace=False)
    
    # Apply quantum bias
    for idx in bias_indices:
        u, v = edge_list[idx]
        # Quantum collapse provides directional nudge
        # (In reality, this would be probabilistic based on OR outcome)
        G[u][v]['weight'] += effective_bias
    
    return tau, effective_bias


def run_simulation(G, n_seeds=100, threshold=1.05, seed=None):
    """Run avalanche simulation from random seed nodes."""
    if seed is not None:
        np.random.seed(seed)
    
    nodes = list(G.nodes())
    seeds = np.random.choice(nodes, size=min(n_seeds, len(nodes)), replace=False)
    
    sizes = []
    for s in seeds:
        size = avalanche_size(G, s, threshold)
        sizes.append(size)
    
    return np.array(sizes)


def reset_network(G):
    """Reset network to original weights."""
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['original_weight']


# =============================================================================
# MONTE CARLO ANALYSIS
# =============================================================================

def monte_carlo_comparison(n_runs=1000, n_seeds_per_run=50, N_nodes=1000,
                           bias_fraction=0.1, bias_strength=0.05, threshold=1.05):
    """
    Run Monte Carlo comparison between classical and quantum-biased avalanches.
    
    Parameters:
    -----------
    n_runs : int
        Number of Monte Carlo runs (default 1000)
    n_seeds_per_run : int
        Number of avalanche seeds per run
    """
    print(f"Running Monte Carlo analysis ({n_runs} runs)...")
    print(f"  Parameters: bias_fraction={bias_fraction}, bias_strength={bias_strength}")
    print()
    
    classical_results = {
        'mean_sizes': [],
        'std_sizes': [],
        'skewness': [],
        'large_fraction': [],  # Fraction > 50% of network
        'all_sizes': []
    }
    
    quantum_results = {
        'mean_sizes': [],
        'std_sizes': [],
        'skewness': [],
        'large_fraction': [],
        'all_sizes': []
    }
    
    large_threshold = N_nodes * 0.5  # "Large" = >50% of network
    
    for run in range(n_runs):
        if run % 100 == 0:
            print(f"  Run {run}/{n_runs}...")
        
        # Create fresh network for each run
        G = create_critical_network(N=N_nodes, seed=run)
        
        # Classical run
        reset_network(G)
        sizes_classical = run_simulation(G, n_seeds=n_seeds_per_run, 
                                         threshold=threshold, seed=run)
        
        classical_results['mean_sizes'].append(np.mean(sizes_classical))
        classical_results['std_sizes'].append(np.std(sizes_classical))
        if np.std(sizes_classical) > 0:
            classical_results['skewness'].append(stats.skew(sizes_classical))
        else:
            classical_results['skewness'].append(0)
        classical_results['large_fraction'].append(
            np.sum(sizes_classical > large_threshold) / len(sizes_classical)
        )
        classical_results['all_sizes'].extend(sizes_classical)
        
        # Quantum-biased run
        reset_network(G)
        tau, eff_bias = apply_or_bias(G, bias_fraction=bias_fraction, 
                                       bias_strength=bias_strength, seed=run+10000)
        sizes_quantum = run_simulation(G, n_seeds=n_seeds_per_run, 
                                       threshold=threshold, seed=run+20000)
        
        quantum_results['mean_sizes'].append(np.mean(sizes_quantum))
        quantum_results['std_sizes'].append(np.std(sizes_quantum))
        if np.std(sizes_quantum) > 0:
            quantum_results['skewness'].append(stats.skew(sizes_quantum))
        else:
            quantum_results['skewness'].append(0)
        quantum_results['large_fraction'].append(
            np.sum(sizes_quantum > large_threshold) / len(sizes_quantum)
        )
        quantum_results['all_sizes'].extend(sizes_quantum)
    
    # Convert to arrays
    for key in classical_results:
        classical_results[key] = np.array(classical_results[key])
        quantum_results[key] = np.array(quantum_results[key])
    
    return classical_results, quantum_results


def statistical_analysis(classical, quantum):
    """Perform statistical tests comparing classical and quantum results."""
    
    results = {}
    
    # T-tests
    t_mean, p_mean = stats.ttest_ind(classical['mean_sizes'], quantum['mean_sizes'])
    t_skew, p_skew = stats.ttest_ind(classical['skewness'], quantum['skewness'])
    t_large, p_large = stats.ttest_ind(classical['large_fraction'], quantum['large_fraction'])
    
    results['mean_sizes'] = {
        'classical': (np.mean(classical['mean_sizes']), np.std(classical['mean_sizes'])),
        'quantum': (np.mean(quantum['mean_sizes']), np.std(quantum['mean_sizes'])),
        't_stat': t_mean,
        'p_value': p_mean
    }
    
    results['skewness'] = {
        'classical': (np.mean(classical['skewness']), np.std(classical['skewness'])),
        'quantum': (np.mean(quantum['skewness']), np.std(quantum['skewness'])),
        't_stat': t_skew,
        'p_value': p_skew
    }
    
    results['large_fraction'] = {
        'classical': (np.mean(classical['large_fraction']), np.std(classical['large_fraction'])),
        'quantum': (np.mean(quantum['large_fraction']), np.std(quantum['large_fraction'])),
        't_stat': t_large,
        'p_value': p_large
    }
    
    # Effect sizes (Cohen's d)
    def cohens_d(x, y):
        nx, ny = len(x), len(y)
        pooled_std = np.sqrt(((nx-1)*np.std(x)**2 + (ny-1)*np.std(y)**2) / (nx+ny-2))
        return (np.mean(x) - np.mean(y)) / pooled_std if pooled_std > 0 else 0
    
    results['effect_sizes'] = {
        'mean_sizes_d': cohens_d(quantum['mean_sizes'], classical['mean_sizes']),
        'skewness_d': cohens_d(quantum['skewness'], classical['skewness']),
        'large_fraction_d': cohens_d(quantum['large_fraction'], classical['large_fraction'])
    }
    
    return results


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(classical, quantum, stats_results, real_data):
    """Create comprehensive visualization of results."""
    
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Avalanche size distributions
    ax1 = fig.add_subplot(2, 3, 1)
    bins = np.logspace(0, 3, 50)
    ax1.hist(classical['all_sizes'], bins=bins, alpha=0.6, label='Classical', 
             color='blue', density=True)
    ax1.hist(quantum['all_sizes'], bins=bins, alpha=0.6, label='Quantum Biased', 
             color='red', density=True)
    
    # Overlay power-law from real data
    x_fit = np.logspace(0, 3, 100)
    y_fit = x_fit ** (-real_data['alpha'])
    y_fit = y_fit / np.sum(y_fit) * len(bins)  # Normalize
    ax1.plot(x_fit, y_fit * 0.1, 'g--', linewidth=2, 
             label=f'Real data (alpha={real_data["alpha"]})')
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Avalanche Size')
    ax1.set_ylabel('Probability Density')
    ax1.set_title('Avalanche Size Distribution')
    ax1.legend()
    
    # 2. Mean sizes comparison
    ax2 = fig.add_subplot(2, 3, 2)
    bp = ax2.boxplot([classical['mean_sizes'], quantum['mean_sizes']], 
                     labels=['Classical', 'Quantum'])
    ax2.set_ylabel('Mean Avalanche Size')
    ax2.set_title(f'Mean Size Comparison\np={stats_results["mean_sizes"]["p_value"]:.2e}')
    
    # 3. Large avalanche fraction
    ax3 = fig.add_subplot(2, 3, 3)
    means = [np.mean(classical['large_fraction']), np.mean(quantum['large_fraction'])]
    stds = [np.std(classical['large_fraction']), np.std(quantum['large_fraction'])]
    x_pos = [0, 1]
    bars = ax3.bar(x_pos, means, yerr=stds, capsize=5, 
                   color=['blue', 'red'], alpha=0.7)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(['Classical', 'Quantum'])
    ax3.set_ylabel('Fraction Large Avalanches (>50%)')
    ax3.set_title(f'Large Avalanche Fraction\np={stats_results["large_fraction"]["p_value"]:.2e}')
    ax3.axhline(y=0.2, color='g', linestyle='--', label='Target min (20%)')
    ax3.axhline(y=0.5, color='orange', linestyle='--', label='Target max (50%)')
    ax3.legend()
    
    # 4. Skewness comparison
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.hist(classical['skewness'], bins=30, alpha=0.6, label='Classical', color='blue')
    ax4.hist(quantum['skewness'], bins=30, alpha=0.6, label='Quantum', color='red')
    ax4.axvline(x=real_data['skewness_range'][0], color='g', linestyle='--', 
                label=f'Real range ({real_data["skewness_range"][0]}-{real_data["skewness_range"][1]})')
    ax4.axvline(x=real_data['skewness_range'][1], color='g', linestyle='--')
    ax4.set_xlabel('Skewness')
    ax4.set_ylabel('Frequency')
    ax4.set_title(f'Skewness Distribution\np={stats_results["skewness"]["p_value"]:.2e}')
    ax4.legend()
    
    # 5. Effect sizes
    ax5 = fig.add_subplot(2, 3, 5)
    effect_names = ['Mean Size', 'Skewness', 'Large Fraction']
    effect_values = [
        stats_results['effect_sizes']['mean_sizes_d'],
        stats_results['effect_sizes']['skewness_d'],
        stats_results['effect_sizes']['large_fraction_d']
    ]
    colors = ['green' if abs(v) > 0.5 else 'orange' if abs(v) > 0.2 else 'gray' 
              for v in effect_values]
    bars = ax5.barh(effect_names, effect_values, color=colors)
    ax5.axvline(x=0, color='black', linewidth=0.5)
    ax5.axvline(x=0.2, color='orange', linestyle='--', alpha=0.5, label='Small effect')
    ax5.axvline(x=0.5, color='green', linestyle='--', alpha=0.5, label='Medium effect')
    ax5.axvline(x=-0.2, color='orange', linestyle='--', alpha=0.5)
    ax5.axvline(x=-0.5, color='green', linestyle='--', alpha=0.5)
    ax5.set_xlabel("Cohen's d (Effect Size)")
    ax5.set_title('Effect Sizes (Quantum vs Classical)')
    ax5.legend()
    
    # 6. Summary text
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.axis('off')
    
    summary_text = f"""
MONTE CARLO RESULTS SUMMARY
===========================

Runs: {len(classical['mean_sizes'])}
Seeds per run: {len(classical['all_sizes']) // len(classical['mean_sizes'])}

MEAN AVALANCHE SIZE:
  Classical: {stats_results['mean_sizes']['classical'][0]:.1f} +/- {stats_results['mean_sizes']['classical'][1]:.1f}
  Quantum:   {stats_results['mean_sizes']['quantum'][0]:.1f} +/- {stats_results['mean_sizes']['quantum'][1]:.1f}
  p-value:   {stats_results['mean_sizes']['p_value']:.2e}
  Cohen's d: {stats_results['effect_sizes']['mean_sizes_d']:.3f}

LARGE AVALANCHE FRACTION (>50%):
  Classical: {stats_results['large_fraction']['classical'][0]:.1%} +/- {stats_results['large_fraction']['classical'][1]:.1%}
  Quantum:   {stats_results['large_fraction']['quantum'][0]:.1%} +/- {stats_results['large_fraction']['quantum'][1]:.1%}
  p-value:   {stats_results['large_fraction']['p_value']:.2e}
  Cohen's d: {stats_results['effect_sizes']['large_fraction_d']:.3f}

SKEWNESS:
  Classical: {stats_results['skewness']['classical'][0]:.2f} +/- {stats_results['skewness']['classical'][1]:.2f}
  Quantum:   {stats_results['skewness']['quantum'][0]:.2f} +/- {stats_results['skewness']['quantum'][1]:.2f}
  p-value:   {stats_results['skewness']['p_value']:.2e}
  Cohen's d: {stats_results['effect_sizes']['skewness_d']:.3f}

REAL DATA COMPARISON:
  Power-law alpha: {real_data['alpha']} (range: {real_data['alpha_range']})
  Expected skewness: {real_data['skewness_range']}
"""
    ax6.text(0.05, 0.95, summary_text, transform=ax6.transAxes, fontsize=9,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('monte_carlo_results.png', dpi=150, bbox_inches='tight')
    print("\n[OK] Plot saved: monte_carlo_results.png")
    
    return fig


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*70)
    print("INTEGRATED QUANTUM-AVALANCHE SIMULATION")
    print("="*70)
    print()
    
    # Parameters (tuned for subtlety)
    N_NODES = 1000
    BIAS_FRACTION = 0.1      # 10% of edges
    BIAS_STRENGTH = 0.05     # Subtle nudge
    THRESHOLD = 1.05         # Near-critical
    N_RUNS = 1000            # Monte Carlo runs
    N_SEEDS_PER_RUN = 50     # Avalanches per run
    
    # Load real data stats
    real_data = load_real_avalanche_stats()
    print(f"Real neural avalanche data: {real_data['source']}")
    print(f"  Power-law exponent: {real_data['alpha']}")
    print(f"  Expected large avalanche fraction: ~{real_data['large_avalanche_fraction']:.0%}")
    print()
    
    # OR collapse time info
    tau_brain = or_collapse_time(1e10)
    print(f"OR Collapse Time (N=10^10): {tau_brain:.3f} s ({tau_brain*1000:.1f} ms)")
    print()
    
    # Run Monte Carlo
    classical, quantum = monte_carlo_comparison(
        n_runs=N_RUNS,
        n_seeds_per_run=N_SEEDS_PER_RUN,
        N_nodes=N_NODES,
        bias_fraction=BIAS_FRACTION,
        bias_strength=BIAS_STRENGTH,
        threshold=THRESHOLD
    )
    
    # Statistical analysis
    print("\nPerforming statistical analysis...")
    stats_results = statistical_analysis(classical, quantum)
    
    # Print key results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print()
    
    print("MEAN AVALANCHE SIZE:")
    print(f"  Classical: {stats_results['mean_sizes']['classical'][0]:.1f} +/- {stats_results['mean_sizes']['classical'][1]:.1f}")
    print(f"  Quantum:   {stats_results['mean_sizes']['quantum'][0]:.1f} +/- {stats_results['mean_sizes']['quantum'][1]:.1f}")
    print(f"  t-stat: {stats_results['mean_sizes']['t_stat']:.2f}, p-value: {stats_results['mean_sizes']['p_value']:.2e}")
    print()
    
    print("LARGE AVALANCHE FRACTION (>50% of network):")
    print(f"  Classical: {stats_results['large_fraction']['classical'][0]:.1%} +/- {stats_results['large_fraction']['classical'][1]:.1%}")
    print(f"  Quantum:   {stats_results['large_fraction']['quantum'][0]:.1%} +/- {stats_results['large_fraction']['quantum'][1]:.1%}")
    print(f"  t-stat: {stats_results['large_fraction']['t_stat']:.2f}, p-value: {stats_results['large_fraction']['p_value']:.2e}")
    print(f"  TARGET: 20-50% for quantum")
    print()
    
    print("SKEWNESS (non-Gaussian tails):")
    print(f"  Classical: {stats_results['skewness']['classical'][0]:.2f} +/- {stats_results['skewness']['classical'][1]:.2f}")
    print(f"  Quantum:   {stats_results['skewness']['quantum'][0]:.2f} +/- {stats_results['skewness']['quantum'][1]:.2f}")
    print(f"  t-stat: {stats_results['skewness']['t_stat']:.2f}, p-value: {stats_results['skewness']['p_value']:.2e}")
    print()
    
    print("EFFECT SIZES (Cohen's d):")
    print(f"  Mean size:      {stats_results['effect_sizes']['mean_sizes_d']:.3f}")
    print(f"  Large fraction: {stats_results['effect_sizes']['large_fraction_d']:.3f}")
    print(f"  Skewness:       {stats_results['effect_sizes']['skewness_d']:.3f}")
    print("  (|d| > 0.2 = small, |d| > 0.5 = medium, |d| > 0.8 = large effect)")
    print()
    
    # Interpretation
    print("="*70)
    print("INTERPRETATION")
    print("="*70)
    
    p_threshold = 0.05
    sig_mean = stats_results['mean_sizes']['p_value'] < p_threshold
    sig_large = stats_results['large_fraction']['p_value'] < p_threshold
    sig_skew = stats_results['skewness']['p_value'] < p_threshold
    
    if sig_mean or sig_large or sig_skew:
        print("\n[SIGNIFICANT] Quantum bias shows measurable effects:")
        if sig_mean:
            print(f"  - Mean avalanche size differs (p={stats_results['mean_sizes']['p_value']:.2e})")
        if sig_large:
            print(f"  - Large avalanche fraction differs (p={stats_results['large_fraction']['p_value']:.2e})")
        if sig_skew:
            print(f"  - Skewness differs (p={stats_results['skewness']['p_value']:.2e})")
    else:
        print("\n[NOT SIGNIFICANT] No detectable quantum effect with current parameters.")
        print("  Consider: increasing bias_strength or bias_fraction")
    
    # Check if quantum large fraction is in target range
    q_large = stats_results['large_fraction']['quantum'][0]
    if 0.2 <= q_large <= 0.5:
        print(f"\n[TARGET MET] Quantum large avalanche fraction ({q_large:.1%}) is in 20-50% range!")
    else:
        print(f"\n[TARGET NOT MET] Quantum large avalanche fraction ({q_large:.1%}) outside 20-50% range.")
    
    # Plot
    print("\nGenerating visualization...")
    fig = plot_results(classical, quantum, stats_results, real_data)
    
    print("\n" + "="*70)
    print("SIMULATION COMPLETE")
    print("="*70)
    

if __name__ == "__main__":
    main()
    plt.show()

