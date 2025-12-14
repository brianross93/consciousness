"""
Quantum-Avalanche Simulation v2
===============================

Enhanced with:
1. Scale N to 10k nodes (better power-laws)
2. Classical mimic control (match quantum mean, test skew)
3. OR param linking (tau -> bias_fraction)
4. CSV export for external analysis

Optimized for faster execution.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy import stats
import csv
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================
hbar = 1.0545718e-34
G = 6.67430e-11
m_tubulin = 1e-22
d_separation = 1e-11  # 0.01 nm


def or_collapse_time(N):
    """Calculate OR collapse time for N tubulins."""
    E_g = N * (G * m_tubulin**2 / d_separation)
    return hbar / E_g


def or_bias_fraction(N_tubulins, base_fraction=0.1, scale_factor=1.0):
    """
    Link OR parameters to bias fraction.
    Larger tubulin ensembles = faster collapse = more edges biased.
    
    tau ~ 1/N, so bias_fraction scales with N (up to a limit)
    """
    tau = or_collapse_time(N_tubulins)
    tau_ref = or_collapse_time(1e10)  # Reference: 10^10 tubulins
    
    # Faster collapse (smaller tau) = stronger effect = more edges
    ratio = tau_ref / tau  # >1 if N > 10^10
    ratio = np.clip(ratio, 0.5, 2.0)  # Reasonable bounds
    
    return base_fraction * ratio * scale_factor


# =============================================================================
# NETWORK & AVALANCHE
# =============================================================================

def create_network(N=10000, k=8, p=0.1, seed=None):
    """Create Watts-Strogatz network (scaled to 10k nodes)."""
    if seed is not None:
        np.random.seed(seed)
    
    G = nx.watts_strogatz_graph(N, k, p, seed=seed)
    
    for u, v in G.edges():
        G[u][v]['weight'] = np.random.normal(1.0, 0.12)
        G[u][v]['original_weight'] = G[u][v]['weight']
    
    return G


def avalanche_size(G, source, threshold=1.05):
    """BFS avalanche propagation."""
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


def reset_network(G):
    """Reset to original weights."""
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['original_weight']


def apply_bias(G, bias_fraction, bias_strength, seed=None):
    """Apply bias to fraction of edges."""
    if seed is not None:
        np.random.seed(seed)
    
    edge_list = list(G.edges())
    n_bias = int(len(edge_list) * bias_fraction)
    if n_bias == 0:
        return
    
    bias_indices = np.random.choice(len(edge_list), size=n_bias, replace=False)
    
    for idx in bias_indices:
        u, v = edge_list[idx]
        G[u][v]['weight'] += bias_strength


def run_avalanches(G, n_seeds=50, threshold=1.05, seed=None):
    """Run avalanches from random seeds."""
    if seed is not None:
        np.random.seed(seed)
    
    nodes = list(G.nodes())
    seeds = np.random.choice(nodes, size=min(n_seeds, len(nodes)), replace=False)
    
    return np.array([avalanche_size(G, s, threshold) for s in seeds])


# =============================================================================
# SIMULATION CONDITIONS
# =============================================================================

def run_classical(G, n_seeds, threshold, seed):
    """Pure classical (thermal only)."""
    reset_network(G)
    return run_avalanches(G, n_seeds, threshold, seed)


def run_quantum(G, n_seeds, threshold, seed, N_tubulins=1e10, 
                base_bias_fraction=0.1, bias_strength=0.05):
    """Quantum-biased with OR-linked parameters."""
    reset_network(G)
    
    # OR-linked bias fraction
    bias_frac = or_bias_fraction(N_tubulins, base_bias_fraction)
    apply_bias(G, bias_frac, bias_strength, seed + 5000)
    
    return run_avalanches(G, n_seeds, threshold, seed)


def run_classical_mimic(G, n_seeds, threshold, seed, target_mean, max_boost=0.15):
    """
    Classical mimic: Add extra thermal noise to match quantum mean.
    Tests whether skew differs even when means are matched.
    """
    reset_network(G)
    
    # First, measure baseline
    baseline_sizes = run_avalanches(G, n_seeds, threshold, seed)
    baseline_mean = np.mean(baseline_sizes)
    
    # If already above target, return as-is
    if baseline_mean >= target_mean:
        return baseline_sizes
    
    # Binary search for boost strength
    reset_network(G)
    
    # Add uniform thermal boost (not quantum-selected edges)
    # This is DIFFERENT from quantum - affects ALL edges equally
    boost = 0.0
    for _ in range(5):  # Few iterations
        reset_network(G)
        # Add small boost to ALL edges
        for u, v in G.edges():
            G[u][v]['weight'] = G[u][v]['original_weight'] + boost
        
        sizes = run_avalanches(G, n_seeds, threshold, seed + 1000)
        current_mean = np.mean(sizes)
        
        if current_mean < target_mean:
            boost += 0.02
        else:
            break
        
        if boost > max_boost:
            break
    
    return sizes


# =============================================================================
# MONTE CARLO
# =============================================================================

def monte_carlo(n_runs=200, N_nodes=10000, n_seeds_per_run=50, threshold=1.05,
                N_tubulins=1e10, base_bias_fraction=0.1, bias_strength=0.05):
    """
    Run Monte Carlo comparison with all three conditions.
    """
    print(f"Monte Carlo: {n_runs} runs, {N_nodes} nodes, {n_seeds_per_run} seeds/run")
    print(f"OR params: N_tubulins={N_tubulins:.0e}, base_bias={base_bias_fraction}, strength={bias_strength}")
    
    results = {
        'classical': {'sizes': [], 'means': [], 'skews': [], 'large_frac': []},
        'quantum': {'sizes': [], 'means': [], 'skews': [], 'large_frac': []},
        'mimic': {'sizes': [], 'means': [], 'skews': [], 'large_frac': []}
    }
    
    large_thresh = N_nodes * 0.5
    
    for run in range(n_runs):
        if run % 50 == 0:
            print(f"  Run {run}/{n_runs}...")
        
        # Fresh network per run
        G = create_network(N=N_nodes, seed=run)
        
        # Classical
        sizes_c = run_classical(G, n_seeds_per_run, threshold, run)
        results['classical']['sizes'].extend(sizes_c)
        results['classical']['means'].append(np.mean(sizes_c))
        results['classical']['skews'].append(stats.skew(sizes_c) if np.std(sizes_c) > 0 else 0)
        results['classical']['large_frac'].append(np.mean(sizes_c > large_thresh))
        
        # Quantum
        sizes_q = run_quantum(G, n_seeds_per_run, threshold, run + 10000,
                              N_tubulins, base_bias_fraction, bias_strength)
        results['quantum']['sizes'].extend(sizes_q)
        results['quantum']['means'].append(np.mean(sizes_q))
        results['quantum']['skews'].append(stats.skew(sizes_q) if np.std(sizes_q) > 0 else 0)
        results['quantum']['large_frac'].append(np.mean(sizes_q > large_thresh))
        
        # Classical mimic (match quantum mean)
        target_mean = np.mean(sizes_q)
        sizes_m = run_classical_mimic(G, n_seeds_per_run, threshold, run + 20000, target_mean)
        results['mimic']['sizes'].extend(sizes_m)
        results['mimic']['means'].append(np.mean(sizes_m))
        results['mimic']['skews'].append(stats.skew(sizes_m) if np.std(sizes_m) > 0 else 0)
        results['mimic']['large_frac'].append(np.mean(sizes_m > large_thresh))
    
    # Convert to arrays
    for cond in results:
        for key in results[cond]:
            results[cond][key] = np.array(results[cond][key])
    
    return results


# =============================================================================
# OR PARAMETER SWEEP
# =============================================================================

def or_param_sweep(n_runs=50, N_nodes=5000, n_seeds_per_run=30, threshold=1.05):
    """
    Sweep OR parameters: vary N_tubulins, see effect on avalanches.
    """
    print("\nOR Parameter Sweep...")
    
    N_tubulin_range = [1e8, 1e9, 1e10, 1e11, 1e12]
    sweep_results = []
    
    for N_tub in N_tubulin_range:
        tau = or_collapse_time(N_tub)
        bias_frac = or_bias_fraction(N_tub, base_fraction=0.1)
        
        print(f"  N_tubulins={N_tub:.0e}: tau={tau:.3f}s, bias_frac={bias_frac:.3f}")
        
        means = []
        large_fracs = []
        
        for run in range(n_runs):
            G = create_network(N=N_nodes, seed=run)
            sizes = run_quantum(G, n_seeds_per_run, threshold, run,
                               N_tub, base_bias_fraction=0.1, bias_strength=0.05)
            means.append(np.mean(sizes))
            large_fracs.append(np.mean(sizes > N_nodes * 0.5))
        
        sweep_results.append({
            'N_tubulins': N_tub,
            'tau': tau,
            'bias_fraction': bias_frac,
            'mean_size': np.mean(means),
            'mean_std': np.std(means),
            'large_frac': np.mean(large_fracs),
            'large_std': np.std(large_fracs)
        })
    
    return sweep_results


# =============================================================================
# EXPORT
# =============================================================================

def export_csv(results, sweep_results, filename_prefix='avalanche_data'):
    """Export all data to CSV files."""
    
    os.makedirs('data/quantum_avalanche_v2', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. All avalanche sizes
    sizes_file = f'data/quantum_avalanche_v2/{filename_prefix}_sizes_{timestamp}.csv'
    with open(sizes_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['condition', 'avalanche_size'])
        for cond in ['classical', 'quantum', 'mimic']:
            for size in results[cond]['sizes']:
                writer.writerow([cond, size])
    print(f"  Exported: {sizes_file}")
    
    # 2. Run-level statistics
    stats_file = f'data/quantum_avalanche_v2/{filename_prefix}_stats_{timestamp}.csv'
    with open(stats_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['condition', 'run', 'mean', 'skewness', 'large_fraction'])
        for cond in ['classical', 'quantum', 'mimic']:
            for i, (m, s, l) in enumerate(zip(
                results[cond]['means'],
                results[cond]['skews'],
                results[cond]['large_frac']
            )):
                writer.writerow([cond, i, m, s, l])
    print(f"  Exported: {stats_file}")
    
    # 3. OR sweep results
    sweep_file = f'data/quantum_avalanche_v2/{filename_prefix}_or_sweep_{timestamp}.csv'
    with open(sweep_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['N_tubulins', 'tau_seconds', 'bias_fraction', 
                        'mean_avalanche_size', 'mean_std', 'large_fraction', 'large_std'])
        for r in sweep_results:
            writer.writerow([r['N_tubulins'], r['tau'], r['bias_fraction'],
                           r['mean_size'], r['mean_std'], r['large_frac'], r['large_std']])
    print(f"  Exported: {sweep_file}")
    
    return sizes_file, stats_file, sweep_file


# =============================================================================
# ANALYSIS & PLOTTING
# =============================================================================

def analyze(results):
    """Statistical analysis with mimic comparison."""
    
    analysis = {}
    
    # Classical vs Quantum
    t_cq, p_cq = stats.ttest_ind(results['classical']['means'], results['quantum']['means'])
    t_skew_cq, p_skew_cq = stats.ttest_ind(results['classical']['skews'], results['quantum']['skews'])
    
    # Mimic vs Quantum (KEY TEST: same mean, different skew?)
    t_mq, p_mq = stats.ttest_ind(results['mimic']['means'], results['quantum']['means'])
    t_skew_mq, p_skew_mq = stats.ttest_ind(results['mimic']['skews'], results['quantum']['skews'])
    
    analysis['classical_vs_quantum'] = {
        'mean_p': p_cq,
        'skew_p': p_skew_cq
    }
    
    analysis['mimic_vs_quantum'] = {
        'mean_p': p_mq,  # Should be ~1 if mimic worked
        'skew_p': p_skew_mq  # KEY: Is this significant?
    }
    
    # Summary stats
    for cond in results:
        analysis[cond] = {
            'mean': np.mean(results[cond]['means']),
            'mean_std': np.std(results[cond]['means']),
            'skew': np.mean(results[cond]['skews']),
            'skew_std': np.std(results[cond]['skews']),
            'large_frac': np.mean(results[cond]['large_frac']),
            'large_std': np.std(results[cond]['large_frac'])
        }
    
    return analysis


def plot_all(results, analysis, sweep_results):
    """Comprehensive visualization."""
    
    fig = plt.figure(figsize=(18, 12))
    
    # 1. Size distributions (log-log for power-law)
    ax1 = fig.add_subplot(2, 3, 1)
    for cond, color, label in [('classical', 'blue', 'Classical'),
                                ('quantum', 'red', 'Quantum'),
                                ('mimic', 'green', 'Mimic')]:
        sizes = results[cond]['sizes']
        bins = np.logspace(0, np.log10(max(sizes)+1), 50)
        ax1.hist(sizes, bins=bins, alpha=0.5, label=label, color=color, density=True)
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Avalanche Size')
    ax1.set_ylabel('Probability Density')
    ax1.set_title('Avalanche Size Distribution (Power-Law Check)')
    ax1.legend()
    
    # 2. Mean comparison
    ax2 = fig.add_subplot(2, 3, 2)
    conditions = ['Classical', 'Quantum', 'Mimic']
    means = [analysis[c.lower()]['mean'] for c in conditions]
    stds = [analysis[c.lower()]['mean_std'] for c in conditions]
    colors = ['blue', 'red', 'green']
    ax2.bar(conditions, means, yerr=stds, color=colors, alpha=0.7, capsize=5)
    ax2.set_ylabel('Mean Avalanche Size')
    ax2.set_title('Mean Size Comparison')
    
    # 3. Skewness comparison (KEY PLOT)
    ax3 = fig.add_subplot(2, 3, 3)
    skews = [analysis[c.lower()]['skew'] for c in conditions]
    skew_stds = [analysis[c.lower()]['skew_std'] for c in conditions]
    ax3.bar(conditions, skews, yerr=skew_stds, color=colors, alpha=0.7, capsize=5)
    ax3.set_ylabel('Skewness')
    ax3.set_title(f'Skewness (Mimic vs Quantum p={analysis["mimic_vs_quantum"]["skew_p"]:.3f})')
    
    # 4. Skewness distributions
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.hist(results['classical']['skews'], bins=30, alpha=0.5, label='Classical', color='blue')
    ax4.hist(results['quantum']['skews'], bins=30, alpha=0.5, label='Quantum', color='red')
    ax4.hist(results['mimic']['skews'], bins=30, alpha=0.5, label='Mimic', color='green')
    ax4.set_xlabel('Skewness')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Skewness Distributions')
    ax4.legend()
    
    # 5. OR Parameter Sweep
    ax5 = fig.add_subplot(2, 3, 5)
    N_tubs = [r['N_tubulins'] for r in sweep_results]
    large_fracs = [r['large_frac'] for r in sweep_results]
    large_stds = [r['large_std'] for r in sweep_results]
    ax5.errorbar(N_tubs, large_fracs, yerr=large_stds, marker='o', capsize=5, color='purple')
    ax5.set_xscale('log')
    ax5.set_xlabel('N Tubulins (ensemble size)')
    ax5.set_ylabel('Large Avalanche Fraction')
    ax5.set_title('OR Parameter Effect: tau -> bias -> avalanches')
    ax5.axhline(y=0.2, color='g', linestyle='--', alpha=0.5, label='Target 20%')
    ax5.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='Target 50%')
    ax5.legend()
    
    # 6. Summary
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.axis('off')
    
    summary = f"""
RESULTS SUMMARY
===============

CLASSICAL vs QUANTUM:
  Mean size:  {analysis['classical']['mean']:.1f} vs {analysis['quantum']['mean']:.1f}
  Skewness:   {analysis['classical']['skew']:.2f} vs {analysis['quantum']['skew']:.2f}
  p(mean):    {analysis['classical_vs_quantum']['mean_p']:.2e}
  p(skew):    {analysis['classical_vs_quantum']['skew_p']:.2e}

MIMIC vs QUANTUM (KEY TEST):
  Mean size:  {analysis['mimic']['mean']:.1f} vs {analysis['quantum']['mean']:.1f}
  Skewness:   {analysis['mimic']['skew']:.2f} vs {analysis['quantum']['skew']:.2f}
  p(mean):    {analysis['mimic_vs_quantum']['mean_p']:.2e}  (should be ~1)
  p(skew):    {analysis['mimic_vs_quantum']['skew_p']:.2e}  (KEY!)

INTERPRETATION:
  If mimic matches quantum mean but NOT skew,
  quantum bias has qualitatively different effect
  than simple thermal boost.

LARGE AVALANCHE FRACTIONS:
  Classical: {analysis['classical']['large_frac']:.1%}
  Quantum:   {analysis['quantum']['large_frac']:.1%}
  Mimic:     {analysis['mimic']['large_frac']:.1%}
"""
    ax6.text(0.05, 0.95, summary, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('data/quantum_avalanche_v2/quantum_avalanche_v2_results.png', dpi=150, bbox_inches='tight')
    print("\n[OK] Plot saved: data/quantum_avalanche_v2/quantum_avalanche_v2_results.png")
    
    return fig


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*70)
    print("QUANTUM-AVALANCHE SIMULATION v2")
    print("="*70)
    print()
    
    # Parameters
    N_NODES = 5000           # Scaled up for better power-laws (10k was slow)
    N_RUNS = 100             # Monte Carlo runs (reduced for speed)
    N_SEEDS_PER_RUN = 30     # Avalanches per run
    THRESHOLD = 1.05
    N_TUBULINS = 1e10
    BASE_BIAS_FRACTION = 0.1
    BIAS_STRENGTH = 0.05
    
    # OR info
    tau = or_collapse_time(N_TUBULINS)
    bias_frac = or_bias_fraction(N_TUBULINS, BASE_BIAS_FRACTION)
    print(f"OR Collapse: N={N_TUBULINS:.0e}, tau={tau:.3f}s, bias_frac={bias_frac:.3f}")
    print()
    
    # Monte Carlo
    results = monte_carlo(
        n_runs=N_RUNS,
        N_nodes=N_NODES,
        n_seeds_per_run=N_SEEDS_PER_RUN,
        threshold=THRESHOLD,
        N_tubulins=N_TUBULINS,
        base_bias_fraction=BASE_BIAS_FRACTION,
        bias_strength=BIAS_STRENGTH
    )
    
    # OR parameter sweep
    sweep_results = or_param_sweep(
        n_runs=20,
        N_nodes=3000,
        n_seeds_per_run=20,
        threshold=THRESHOLD
    )
    
    # Analysis
    print("\nAnalyzing results...")
    analysis = analyze(results)
    
    # Print key results
    print("\n" + "="*70)
    print("KEY RESULTS")
    print("="*70)
    
    print("\nCLASSICAL vs QUANTUM:")
    print(f"  Mean: {analysis['classical']['mean']:.1f} vs {analysis['quantum']['mean']:.1f}")
    print(f"  Skew: {analysis['classical']['skew']:.2f} vs {analysis['quantum']['skew']:.2f}")
    print(f"  p(skew): {analysis['classical_vs_quantum']['skew_p']:.4f}")
    
    print("\nMIMIC vs QUANTUM (matched means, test skew):")
    print(f"  Mean: {analysis['mimic']['mean']:.1f} vs {analysis['quantum']['mean']:.1f}")
    print(f"  Skew: {analysis['mimic']['skew']:.2f} vs {analysis['quantum']['skew']:.2f}")
    print(f"  p(skew): {analysis['mimic_vs_quantum']['skew_p']:.4f}")
    
    if analysis['mimic_vs_quantum']['skew_p'] < 0.05:
        print("\n  [SIGNIFICANT] Quantum produces different skew than thermal mimic!")
    else:
        print("\n  [NOT SIGNIFICANT] Cannot distinguish quantum from thermal boost.")
    
    print("\nLARGE AVALANCHE FRACTIONS (target 20-50%):")
    print(f"  Classical: {analysis['classical']['large_frac']:.1%}")
    print(f"  Quantum:   {analysis['quantum']['large_frac']:.1%}")
    print(f"  Mimic:     {analysis['mimic']['large_frac']:.1%}")
    
    # Export CSV
    print("\nExporting data to CSV...")
    export_csv(results, sweep_results)
    
    # Plot
    print("\nGenerating plots...")
    fig = plot_all(results, analysis, sweep_results)
    
    print("\n" + "="*70)
    print("COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
    plt.show()

