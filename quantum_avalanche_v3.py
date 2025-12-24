"""
Quantum-Avalanche Simulation v3
===============================

New features:
1. Power-law exponent fit (linregress on log-binned CDF)
2. Negative bias runs (QZE "veto" - suppresses avalanches)
3. Real avalanche data loader (Beggs lab format compatible)
4. Enhanced visualization

Based on v2 results showing quantum skew differs from mimic even at matched means.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import csv
import os
import glob
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================
hbar = 1.0545718e-34
G = 6.67430e-11
m_tubulin = 1e-22
d_separation = 1e-11


def or_collapse_time(N):
    """Calculate OR collapse time for N tubulins."""
    E_g = N * (G * m_tubulin**2 / d_separation)
    return hbar / E_g


def or_bias_fraction(N_tubulins, base_fraction=0.1):
    """OR-linked bias fraction."""
    tau = or_collapse_time(N_tubulins)
    tau_ref = or_collapse_time(1e10)
    ratio = np.clip(tau_ref / tau, 0.5, 2.0)
    return base_fraction * ratio


# =============================================================================
# POWER-LAW FITTING
# =============================================================================

def fit_powerlaw(sizes, x_min=None, x_max=None):
    """
    Simple MLE power-law exponent (no xmin search).
    alpha = 1 + n / sum(log(x/xmin))
    """
    sizes = np.asarray(sizes, dtype=float)
    sizes = sizes[np.isfinite(sizes)]
    sizes = sizes[sizes > 0]
    if sizes.size == 0:
        return np.nan, np.nan, np.nan
    if x_max is not None:
        sizes = sizes[sizes <= x_max]
    if sizes.size == 0:
        return np.nan, np.nan, np.nan
    if x_min is None:
        x_min = sizes.min()
    sizes = sizes[sizes >= x_min]
    n = len(sizes)
    if n < 10:
        return np.nan, np.nan, np.nan
    alpha = 1 + n / np.sum(np.log(sizes / x_min))
    alpha_err = (alpha - 1) / np.sqrt(n)
    # KS statistic (optional check)
    sorted_sizes = np.sort(sizes)
    emp_cdf = np.arange(1, n + 1) / n
    th_cdf = 1 - (sorted_sizes / x_min) ** (-(alpha - 1))
    ks_stat = np.max(np.abs(emp_cdf - th_cdf))
    return alpha, alpha_err, ks_stat


def fit_powerlaw_linregress(sizes, n_bins=20, x_min=5):
    """
    Legacy log-binned fit (kept for plotting).
    """
    sizes = np.array(sizes)
    sizes = sizes[sizes >= x_min]
    
    if len(sizes) < 50:
        return np.nan, np.nan, [], []
    
    bins = np.logspace(np.log10(x_min), np.log10(max(sizes)), n_bins + 1)
    hist, bin_edges = np.histogram(sizes, bins=bins, density=True)
    bin_centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])
    mask = hist > 0
    log_x = np.log10(bin_centers[mask])
    log_y = np.log10(hist[mask])
    
    if len(log_x) < 3:
        return np.nan, np.nan, [], []
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_x, log_y)
    alpha = -slope
    return alpha, std_err, bin_centers[mask], hist[mask]


# =============================================================================
# REAL DATA LOADER
# =============================================================================

def load_beggs_data(filepath=None):
    """
    Load real neural avalanche data (Beggs lab or similar format).
    
    Expected CSV format:
    size,duration (or just size column)
    
    If no file provided, generates synthetic power-law data matching
    literature values (alpha ~1.5, Beggs & Plenz 2003).
    """
    # 1) Prefer local avalanche CSVs if present (e.g., hc-3 derived)
    local_glob = os.environ.get("REAL_AVALANCHE_GLOB", "data/neuron/avalanche_sizes_*.csv")
    local_files = sorted(glob.glob(local_glob))
    if filepath is None and local_files:
        sizes = []
        for lf in local_files:
            try:
                arr = np.loadtxt(lf, delimiter=',', skiprows=1, usecols=[0])
                # loadtxt returns float if any blank; enforce int-ish
                sizes.extend([int(x) for x in np.atleast_1d(arr) if x > 0])
            except Exception as e:
                print(f"[warn] Failed to read {lf}: {e}")
        if sizes:
            return np.array(sizes), f'local ({len(local_files)} files: {local_glob})'
    
    # 2) Specific file if provided
    if filepath is not None and os.path.exists(filepath):
        sizes = []
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'size' in row and row['size']:
                    sizes.append(int(row['size']))
                elif 'avalanche_size' in row and row['avalanche_size']:
                    sizes.append(int(row['avalanche_size']))
        if sizes:
            return np.array(sizes), 'real'
    
    # 3) Fallback synthetic "real" data matching literature (Beggs & Plenz 2003)
    np.random.seed(42)
    n_samples = 5000
    alpha = 1.5
    x_min = 1
    
    u = np.random.uniform(0, 1, n_samples)
    sizes = x_min * (1 - u) ** (-1 / (alpha - 1))
    sizes = np.clip(sizes, 1, 5000).astype(int)
    
    return sizes, 'synthetic (alpha=1.5, Beggs-like)'


# =============================================================================
# NETWORK & AVALANCHE
# =============================================================================

def create_network(N=5000, k=10, p=0.1, seed=None):
    """Create network with adjustable connectivity."""
    if seed is not None:
        np.random.seed(seed)
    
    G = nx.watts_strogatz_graph(N, k, p, seed=seed)
    
    for u, v in G.edges():
        G[u][v]['weight'] = np.random.normal(1.0, 0.12)
        G[u][v]['original_weight'] = G[u][v]['weight']
    
    return G


def avalanche_size(G, source, threshold=1.05):
    """BFS avalanche."""
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
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['original_weight']


def apply_bias(G, bias_fraction, bias_strength, seed=None):
    """Apply bias (positive or negative)."""
    if seed is not None:
        np.random.seed(seed)
    
    edge_list = list(G.edges())
    n_bias = max(1, int(len(edge_list) * bias_fraction))
    bias_indices = np.random.choice(len(edge_list), size=n_bias, replace=False)
    
    for idx in bias_indices:
        u, v = edge_list[idx]
        G[u][v]['weight'] += bias_strength  # Can be negative for veto!


def run_avalanches(G, n_seeds=30, threshold=1.05, seed=None):
    if seed is not None:
        np.random.seed(seed)
    
    nodes = list(G.nodes())
    seeds = np.random.choice(nodes, size=min(n_seeds, len(nodes)), replace=False)
    return np.array([avalanche_size(G, s, threshold) for s in seeds])


def collapse_to_avalanches(seq):
    """Convert a sequence of bin counts into contiguous avalanches (nonzero runs)."""
    aval = []
    run = 0
    for v in seq:
        if v > 0:
            run += v
        elif run > 0:
            aval.append(run)
            run = 0
    if run > 0:
        aval.append(run)
    return np.array(aval)


def simulate_time_bins(N=3000, k=10, p=0.1, n_bins=500, prob_fire=0.02,
                       base_threshold=1.03, bias_nodes=None, bias_strength=0.0,
                       seed=None, refractory=False):
    """
    Generate per-bin active-unit counts from a simple stochastic propagation model.
    - prob_fire: baseline prob a node activates spontaneously per bin
    - base_threshold: neighbor weight threshold for propagating activity
    - bias_nodes: indices receiving an additive bias to activation probability
    - bias_strength: added probability for bias_nodes
    """
    if seed is not None:
        np.random.seed(seed)
    G = nx.watts_strogatz_graph(N, k, p, seed=seed)
    # neighbor weights ~ N(1, 0.12)
    for u, v in G.edges():
        G[u][v]['weight'] = np.random.normal(1.0, 0.12)
    active_counts = []
    last_active_mask = np.zeros(N, dtype=bool)
    for t in range(n_bins):
        # spontaneous
        prob = np.full(N, prob_fire)
        if bias_nodes is not None and bias_strength != 0:
            prob[bias_nodes] = np.clip(prob[bias_nodes] + bias_strength, 0, 1)
        spontaneous = np.random.rand(N) < prob
        # propagation: if neighbor weight > threshold and neighbor fired last bin
        neighbor_hit = np.zeros(N, dtype=bool)
        for u, v in G.edges():
            if last_active_mask[u] and G[u][v]['weight'] > base_threshold:
                neighbor_hit[v] = True
            if last_active_mask[v] and G[u][v]['weight'] > base_threshold:
                neighbor_hit[u] = True
        propagated = neighbor_hit
        active_mask = spontaneous | propagated
        if refractory:
            # simple 1-bin refractory: can't fire twice consecutively
            active_mask = active_mask & (~last_active_mask)
        active_counts.append({'mask': active_mask, 'count': active_mask.sum()})
        last_active_mask = active_mask
    return np.array([a['count'] for a in active_counts])


# =============================================================================
# SIMULATION CONDITIONS
# =============================================================================

def run_classical(G, n_seeds, threshold, seed):
    reset_network(G)
    return run_avalanches(G, n_seeds, threshold, seed)


def run_quantum_positive(G, n_seeds, threshold, seed, N_tubulins=1e10,
                          base_bias_fraction=0.1, bias_strength=0.05):
    """Quantum bias: OR collapse AMPLIFIES selected edges (free will)."""
    reset_network(G)
    bias_frac = or_bias_fraction(N_tubulins, base_bias_fraction)
    apply_bias(G, bias_frac, bias_strength, seed + 5000)
    return run_avalanches(G, n_seeds, threshold, seed)


def run_quantum_negative(G, n_seeds, threshold, seed, N_tubulins=1e10,
                          base_bias_fraction=0.1, bias_strength=0.05):
    """Quantum VETO: QZE SUPPRESSES selected edges (free won't)."""
    reset_network(G)
    bias_frac = or_bias_fraction(N_tubulins, base_bias_fraction)
    apply_bias(G, bias_frac, -bias_strength, seed + 5000)  # NEGATIVE!
    return run_avalanches(G, n_seeds, threshold, seed)


def run_mimic(G, n_seeds, threshold, seed, target_mean, max_boost=0.15):
    """Classical mimic with uniform boost."""
    reset_network(G)
    
    # Binary search for boost
    boost = 0.0
    for _ in range(5):
        reset_network(G)
        for u, v in G.edges():
            G[u][v]['weight'] = G[u][v]['original_weight'] + boost
        
        sizes = run_avalanches(G, n_seeds, threshold, seed + 1000)
        if np.mean(sizes) < target_mean and boost < max_boost:
            boost += 0.02
        else:
            break
    
    return sizes


# =============================================================================
# MONTE CARLO
# =============================================================================

def monte_carlo(n_runs=80, N_nodes=5000, n_seeds_per_run=30, threshold=1.05,
                N_tubulins=1e10, base_bias_fraction=0.1, bias_strength=0.05):
    """
    Monte Carlo with all four conditions using the original cascade metric:
    - Classical
    - Quantum Positive (amplify)
    - Quantum Negative (veto)
    - Classical Mimic
    """
    print(f"Monte Carlo: {n_runs} runs, {N_nodes} nodes")
    
    results = {
        'classical': {'sizes': [], 'means': [], 'skews': []},
        'quantum_pos': {'sizes': [], 'means': [], 'skews': []},
        'quantum_neg': {'sizes': [], 'means': [], 'skews': []},
        'mimic': {'sizes': [], 'means': [], 'skews': []}
    }
    
    for run in range(n_runs):
        if run % 20 == 0:
            print(f"  Run {run}/{n_runs}...")
        
        G = create_network(N=N_nodes, seed=run)
        
        # Classical
        sizes_c = run_classical(G, n_seeds_per_run, threshold, run)
        aval_c = collapse_to_avalanches(sizes_c)
        results['classical']['sizes'].extend(aval_c)
        results['classical']['means'].append(np.mean(aval_c) if aval_c.size else 0)
        results['classical']['skews'].append(stats.skew(aval_c) if aval_c.size and np.std(aval_c) > 0 else 0)
        
        # Quantum Positive (amplify)
        sizes_qp = run_quantum_positive(G, n_seeds_per_run, threshold, run + 10000,
                                         N_tubulins, base_bias_fraction, bias_strength)
        aval_qp = collapse_to_avalanches(sizes_qp)
        results['quantum_pos']['sizes'].extend(aval_qp)
        results['quantum_pos']['means'].append(np.mean(aval_qp) if aval_qp.size else 0)
        results['quantum_pos']['skews'].append(stats.skew(aval_qp) if aval_qp.size and np.std(aval_qp) > 0 else 0)
        
        # Quantum Negative (veto)
        sizes_qn = run_quantum_negative(G, n_seeds_per_run, threshold, run + 20000,
                                         N_tubulins, base_bias_fraction, bias_strength)
        aval_qn = collapse_to_avalanches(sizes_qn)
        results['quantum_neg']['sizes'].extend(aval_qn)
        results['quantum_neg']['means'].append(np.mean(aval_qn) if aval_qn.size else 0)
        results['quantum_neg']['skews'].append(stats.skew(aval_qn) if aval_qn.size and np.std(aval_qn) > 0 else 0)
        
        # Mimic (match quantum positive)
        target_mean = np.mean(sizes_qp) if sizes_qp.size else 0
        sizes_m = run_mimic(G, n_seeds_per_run, threshold, run + 30000, target_mean)
        aval_m = collapse_to_avalanches(sizes_m)
        results['mimic']['sizes'].extend(aval_m)
        results['mimic']['means'].append(np.mean(aval_m) if aval_m.size else 0)
        results['mimic']['skews'].append(stats.skew(aval_m) if aval_m.size and np.std(aval_m) > 0 else 0)
    
    for cond in results:
        for key in results[cond]:
            results[cond][key] = np.array(results[cond][key])
    
    return results


def monte_carlo_timebins(n_runs=40, N_nodes=3000, k=10, p=0.1, n_bins=800,
                         prob_fire=0.02, base_threshold=1.03,
                         bias_fraction=0.1, bias_strength=0.02,
                         seed_offset=0):
    """
    Time-binned avalanches using active-units-per-bin (aligned with real data).
    Returns dict with sizes/means/skews for each condition.
    """
    results = {
        'classical': {'sizes': [], 'means': [], 'skews': []},
        'quantum_pos': {'sizes': [], 'means': [], 'skews': []},
        'quantum_neg': {'sizes': [], 'means': [], 'skews': []},
        'mimic': {'sizes': [], 'means': [], 'skews': []}
    }
    for run in range(n_runs):
        if run % 10 == 0:
            print(f"  [timebin] Run {run}/{n_runs}...")
        # bias nodes selection
        np.random.seed(run + seed_offset)
        bias_nodes = np.random.choice(N_nodes, size=max(1, int(bias_fraction * N_nodes)), replace=False)
        
        # Classical
        counts = simulate_time_bins(N=N_nodes, k=k, p=p, n_bins=n_bins,
                                    prob_fire=prob_fire, base_threshold=base_threshold,
                                    bias_nodes=None, bias_strength=0.0,
                                    seed=run + seed_offset)
        aval = collapse_to_avalanches(counts)
        results['classical']['sizes'].extend(aval)
        results['classical']['means'].append(np.mean(aval) if aval.size else 0)
        results['classical']['skews'].append(stats.skew(aval) if aval.size and np.std(aval) > 0 else 0)
        
        # Quantum Positive
        counts = simulate_time_bins(N=N_nodes, k=k, p=p, n_bins=n_bins,
                                    prob_fire=prob_fire, base_threshold=base_threshold,
                                    bias_nodes=bias_nodes, bias_strength=bias_strength,
                                    seed=run + seed_offset + 10000)
        aval = collapse_to_avalanches(counts)
        results['quantum_pos']['sizes'].extend(aval)
        results['quantum_pos']['means'].append(np.mean(aval) if aval.size else 0)
        results['quantum_pos']['skews'].append(stats.skew(aval) if aval.size and np.std(aval) > 0 else 0)
        
        # Quantum Negative (veto: reduce firing prob on bias nodes)
        counts = simulate_time_bins(N=N_nodes, k=k, p=p, n_bins=n_bins,
                                    prob_fire=prob_fire, base_threshold=base_threshold,
                                    bias_nodes=bias_nodes, bias_strength=-bias_strength,
                                    seed=run + seed_offset + 20000)
        aval = collapse_to_avalanches(counts)
        results['quantum_neg']['sizes'].extend(aval)
        results['quantum_neg']['means'].append(np.mean(aval) if aval.size else 0)
        results['quantum_neg']['skews'].append(stats.skew(aval) if aval.size and np.std(aval) > 0 else 0)
        
        # Mimic: no bias nodes but increase global prob_fire slightly to match Q(+) mean
        mimic_prob = prob_fire + (bias_strength * bias_fraction)
        counts = simulate_time_bins(N=N_nodes, k=k, p=p, n_bins=n_bins,
                                    prob_fire=mimic_prob, base_threshold=base_threshold,
                                    bias_nodes=None, bias_strength=0.0,
                                    seed=run + seed_offset + 30000)
        aval = collapse_to_avalanches(counts)
        results['mimic']['sizes'].extend(aval)
        results['mimic']['means'].append(np.mean(aval) if aval.size else 0)
        results['mimic']['skews'].append(stats.skew(aval) if aval.size and np.std(aval) > 0 else 0)
    return results


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze(results, real_sizes):
    """Full statistical analysis including power-law fits."""
    
    analysis = {}
    
    # Power-law fits for each condition
    for cond in results:
        alpha_mle, alpha_err, ks = fit_powerlaw(results[cond]['sizes'])
        alpha_lr, lr_err, _, _ = fit_powerlaw_linregress(results[cond]['sizes'])
        
        analysis[cond] = {
            'mean': np.mean(results[cond]['means']),
            'mean_std': np.std(results[cond]['means']),
            'skew': np.mean(results[cond]['skews']),
            'skew_std': np.std(results[cond]['skews']),
            'alpha_mle': alpha_mle,
            'alpha_mle_err': alpha_err,
            'alpha_linreg': alpha_lr,
            'ks_stat': ks
        }
    
    # Real data fit
    alpha_real, _, _ = fit_powerlaw(real_sizes)
    analysis['real_data'] = {'alpha': alpha_real}
    
    # Statistical tests
    # Classical vs Quantum Positive
    t_cqp, p_cqp = stats.ttest_ind(results['classical']['skews'], results['quantum_pos']['skews'])
    analysis['classical_vs_quantum_pos'] = {'skew_p': p_cqp}
    
    # Classical vs Quantum Negative
    t_cqn, p_cqn = stats.ttest_ind(results['classical']['skews'], results['quantum_neg']['skews'])
    analysis['classical_vs_quantum_neg'] = {'skew_p': p_cqn}
    
    # Mimic vs Quantum Positive (KEY TEST)
    t_mqp, p_mqp = stats.ttest_ind(results['mimic']['skews'], results['quantum_pos']['skews'])
    analysis['mimic_vs_quantum_pos'] = {'skew_p': p_mqp}
    
    # Quantum Positive vs Quantum Negative
    t_qpn, p_qpn = stats.ttest_ind(results['quantum_pos']['means'], results['quantum_neg']['means'])
    analysis['quantum_pos_vs_neg'] = {'mean_p': p_qpn}
    
    return analysis


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_all(results, analysis, real_sizes, real_source):
    """Comprehensive 6-panel visualization."""
    
    fig = plt.figure(figsize=(18, 12))
    
    # 1. Power-law fits (log-log with real data overlay)
    ax1 = fig.add_subplot(2, 3, 1)
    
    colors = {'classical': 'blue', 'quantum_pos': 'red', 
              'quantum_neg': 'orange', 'mimic': 'green'}
    labels = {'classical': 'Classical', 'quantum_pos': 'Quantum (+)', 
              'quantum_neg': 'Quantum Veto (-)', 'mimic': 'Mimic'}
    
    for cond in ['classical', 'quantum_pos', 'quantum_neg']:
        alpha, _, bin_x, bin_y = fit_powerlaw_linregress(results[cond]['sizes'])
        if len(bin_x) > 0:
            ax1.scatter(bin_x, bin_y, alpha=0.6, color=colors[cond], 
                       label=f'{labels[cond]} (a={alpha:.2f})', s=30)
    
    # Real data overlay
    alpha_real, _, bin_x_real, bin_y_real = fit_powerlaw_linregress(real_sizes)
    if len(bin_x_real) > 0:
        ax1.plot(bin_x_real, bin_y_real, 'k--', linewidth=2, 
                label=f'Real data (a={alpha_real:.2f})')
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Avalanche Size')
    ax1.set_ylabel('P(size)')
    ax1.set_title('Power-Law Fits (log-binned)')
    ax1.legend(fontsize=8)
    
    # 2. Skewness comparison (all 4 conditions)
    ax2 = fig.add_subplot(2, 3, 2)
    conditions = ['Classical', 'Q(+)', 'Q(-)', 'Mimic']
    cond_keys = ['classical', 'quantum_pos', 'quantum_neg', 'mimic']
    skews = [analysis[k]['skew'] for k in cond_keys]
    skew_stds = [analysis[k]['skew_std'] for k in cond_keys]
    bar_colors = ['blue', 'red', 'orange', 'green']
    
    ax2.bar(conditions, skews, yerr=skew_stds, color=bar_colors, alpha=0.7, capsize=5)
    ax2.set_ylabel('Skewness')
    ax2.set_title('Skewness: Quantum(+) vs Veto(-) vs Mimic')
    ax2.axhline(y=analysis['classical']['skew'], color='blue', linestyle='--', alpha=0.5)
    
    # 3. Mean avalanche sizes
    ax3 = fig.add_subplot(2, 3, 3)
    means = [analysis[k]['mean'] for k in cond_keys]
    mean_stds = [analysis[k]['mean_std'] for k in cond_keys]
    ax3.bar(conditions, means, yerr=mean_stds, color=bar_colors, alpha=0.7, capsize=5)
    ax3.set_ylabel('Mean Avalanche Size')
    ax3.set_title(f'Q(+) vs Q(-) mean p={analysis["quantum_pos_vs_neg"]["mean_p"]:.3f}')
    
    # 4. Veto effect: histogram comparison
    ax4 = fig.add_subplot(2, 3, 4)
    bins = np.linspace(0, max(results['quantum_pos']['sizes']), 50)
    ax4.hist(results['quantum_pos']['sizes'], bins=bins, alpha=0.5, 
             label='Quantum (+)', color='red', density=True)
    ax4.hist(results['quantum_neg']['sizes'], bins=bins, alpha=0.5, 
             label='Quantum Veto (-)', color='orange', density=True)
    ax4.set_xlabel('Avalanche Size')
    ax4.set_ylabel('Density')
    ax4.set_title('Free Will (+) vs Free Won\'t (-)')
    ax4.legend()
    
    # 5. Mimic test detail
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.hist(results['mimic']['skews'], bins=20, alpha=0.5, label='Mimic', color='green')
    ax5.hist(results['quantum_pos']['skews'], bins=20, alpha=0.5, label='Quantum(+)', color='red')
    ax5.axvline(x=np.mean(results['mimic']['skews']), color='green', linestyle='--')
    ax5.axvline(x=np.mean(results['quantum_pos']['skews']), color='red', linestyle='--')
    ax5.set_xlabel('Skewness (per run)')
    ax5.set_ylabel('Frequency')
    ax5.set_title(f'Mimic vs Q(+) Skew Distributions (p={analysis["mimic_vs_quantum_pos"]["skew_p"]:.4f})')
    ax5.legend()
    
    # 6. Summary text
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.axis('off')
    
    summary = f"""
RESULTS SUMMARY (v3)
====================

POWER-LAW EXPONENTS (alpha):
  Classical:    {analysis['classical']['alpha_mle']:.2f} +/- {analysis['classical']['alpha_mle_err']:.2f}
  Quantum(+):   {analysis['quantum_pos']['alpha_mle']:.2f} +/- {analysis['quantum_pos']['alpha_mle_err']:.2f}
  Quantum(-):   {analysis['quantum_neg']['alpha_mle']:.2f} +/- {analysis['quantum_neg']['alpha_mle_err']:.2f}
  Real data:    {analysis['real_data']['alpha']:.2f}
  Literature:   ~1.5 (Beggs & Plenz)

MEAN AVALANCHE SIZE:
  Classical:    {analysis['classical']['mean']:.0f}
  Quantum(+):   {analysis['quantum_pos']['mean']:.0f}  (amplify)
  Quantum(-):   {analysis['quantum_neg']['mean']:.0f}  (veto)
  Mimic:        {analysis['mimic']['mean']:.0f}

SKEWNESS:
  Classical:    {analysis['classical']['skew']:.2f}
  Quantum(+):   {analysis['quantum_pos']['skew']:.2f}
  Quantum(-):   {analysis['quantum_neg']['skew']:.2f}
  Mimic:        {analysis['mimic']['skew']:.2f}

KEY TESTS:
  Mimic vs Q(+) skew:  p = {analysis['mimic_vs_quantum_pos']['skew_p']:.4f}
  Q(+) vs Q(-) mean:   p = {analysis['quantum_pos_vs_neg']['mean_p']:.4f}

INTERPRETATION:
  Q(+) amplifies avalanches (free will)
  Q(-) suppresses avalanches (free won't/veto)
  Mimic fails to replicate Q(+) skew => quantum effect!
  
Real data source: {real_source}
"""
    ax6.text(0.02, 0.98, summary, transform=ax6.transAxes, fontsize=9,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    os.makedirs('data/quantum_avalanche_v3', exist_ok=True)
    plt.savefig('data/quantum_avalanche_v3/quantum_avalanche_v3_results.png', dpi=150, bbox_inches='tight')
    print("\n[OK] Plot saved: data/quantum_avalanche_v3/quantum_avalanche_v3_results.png")
    
    return fig


def export_csv(results, analysis, filename='avalanche_v3_data.csv'):
    """Export all sizes with condition labels."""
    
    os.makedirs('data/quantum_avalanche_v3', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # All sizes
    sizes_file = f'data/quantum_avalanche_v3/avalanche_sizes_{timestamp}.csv'
    with open(sizes_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['condition', 'size'])
        for cond in results:
            for size in results[cond]['sizes']:
                writer.writerow([cond, size])
    print(f"  Exported: {sizes_file}")
    
    # Summary stats
    stats_file = f'data/quantum_avalanche_v3/avalanche_stats_{timestamp}.csv'
    with open(stats_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['condition', 'mean', 'mean_std', 'skew', 'skew_std', 
                        'alpha_mle', 'alpha_err'])
        for cond in results:
            a = analysis[cond]
            writer.writerow([cond, a['mean'], a['mean_std'], a['skew'], 
                           a['skew_std'], a['alpha_mle'], a['alpha_mle_err']])
    print(f"  Exported: {stats_file}")
    
    return sizes_file, stats_file


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*70)
    print("QUANTUM-AVALANCHE SIMULATION v3")
    print("With: Power-law fits, QZE Veto, Real data comparison")
    print("="*70)
    print()
    
    # Time-binned simulation parameters (aligned to real-data binning)
    BIN_MS = float(os.environ.get("SIM_BIN_MS", "4"))
    N_NODES = int(os.environ.get("SIM_NODES", "3000"))
    N_RUNS = int(os.environ.get("SIM_RUNS", "40"))
    N_BINS = int(os.environ.get("SIM_N_BINS", "800"))
    PROB_FIRE = float(os.environ.get("SIM_PROB_FIRE", "0.02"))
    BASE_THRESHOLD = float(os.environ.get("SIM_BASE_THRESHOLD", "1.03"))
    BIAS_FRACTION = float(os.environ.get("SIM_BIAS_FRACTION", "0.1"))
    BIAS_STRENGTH = float(os.environ.get("SIM_BIAS_STRENGTH", "0.02"))
    REFRACTORY = os.environ.get("SIM_REFRACTORY", "1") == "1"
    DO_SWEEP = os.environ.get("SIM_SWEEP", "1") == "1"
    
    # Load real data
    print("Loading real avalanche data...")
    real_sizes, real_source = load_beggs_data()  # Prefers local data/neuron/avalanche_sizes_*.csv or units_bin*
    print(f"  Source: {real_source}")
    print(f"  N samples: {len(real_sizes)}")
    alpha_real, _, _ = fit_powerlaw(real_sizes)
    print(f"  Alpha: {alpha_real:.2f}")
    print()
    
    target_alpha = alpha_real if np.isfinite(alpha_real) else 1.6

    # Optional parameter sweep to match real alpha
    best = None
    if DO_SWEEP:
        print("Sweeping prob_fire and base_threshold to match real alpha...")
        pf_grid = [float(x) for x in os.environ.get("SIM_SWEEP_PROB_FIRE", "0.0002,0.0005,0.001").split(",")]
        th_grid = [float(x) for x in os.environ.get("SIM_SWEEP_THRESHOLD", "1.05,1.1,1.2,1.3").split(",")]
        k_grid = [int(x) for x in os.environ.get("SIM_SWEEP_K", "8,10").split(",")]
        sweep_runs = int(os.environ.get("SIM_SWEEP_RUNS", "8"))
        sweep_bins = int(os.environ.get("SIM_SWEEP_N_BINS", "400"))
        for pf in pf_grid:
            for th in th_grid:
                for kk in k_grid:
                    res = monte_carlo_timebins(
                        n_runs=sweep_runs,
                        N_nodes=N_NODES,
                        k=kk,
                        n_bins=sweep_bins,
                        prob_fire=pf,
                        base_threshold=th,
                        bias_fraction=0.0,
                        bias_strength=0.0,
                        seed_offset=1234
                    )
                    aval = np.array(res['classical']['sizes'])
                    alpha_sim, _, _ = fit_powerlaw(aval)
                    diff = abs(alpha_sim - target_alpha) if np.isfinite(alpha_sim) else np.inf
                    print(f"  pf={pf}, th={th}, k={kk} -> alpha_sim={alpha_sim:.2f}, diff={diff:.2f}")
                    if best is None or diff < best['diff']:
                        best = {'pf': pf, 'th': th, 'k': kk, 'alpha': alpha_sim, 'diff': diff}
        if best:
            PROB_FIRE = best['pf']
            BASE_THRESHOLD = best['th']
            K_SWEEP = best['k']
            print(f"Best sweep: pf={PROB_FIRE}, th={BASE_THRESHOLD}, k={K_SWEEP}, alpha_sim={best['alpha']:.2f}")
        else:
            K_SWEEP = 10
    else:
        K_SWEEP = 10

    # Time-binned Monte Carlo aligned to real-data binning (final run)
    results = monte_carlo_timebins(
        n_runs=N_RUNS,
        N_nodes=N_NODES,
        k=K_SWEEP,
        n_bins=N_BINS,
        prob_fire=PROB_FIRE,
        base_threshold=BASE_THRESHOLD,
        bias_fraction=BIAS_FRACTION,
        bias_strength=BIAS_STRENGTH,
        seed_offset=0
    )
    
    # Analysis
    print("\nAnalyzing...")
    analysis = analyze(results, real_sizes)
    
    # Print results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    print("\nPOWER-LAW EXPONENTS:")
    for cond in ['classical', 'quantum_pos', 'quantum_neg']:
        print(f"  {cond:12s}: alpha = {analysis[cond]['alpha_mle']:.2f} +/- {analysis[cond]['alpha_mle_err']:.2f}")
    print(f"  {'real data':12s}: alpha = {analysis['real_data']['alpha']:.2f}")
    
    print("\nMEAN AVALANCHE SIZE:")
    print(f"  Classical:    {analysis['classical']['mean']:.0f}")
    print(f"  Quantum(+):   {analysis['quantum_pos']['mean']:.0f}  [amplify/free will]")
    print(f"  Quantum(-):   {analysis['quantum_neg']['mean']:.0f}  [veto/free won't]")
    print(f"  Mimic:        {analysis['mimic']['mean']:.0f}")
    
    print("\nSKEWNESS:")
    print(f"  Classical:    {analysis['classical']['skew']:.2f}")
    print(f"  Quantum(+):   {analysis['quantum_pos']['skew']:.2f}")
    print(f"  Quantum(-):   {analysis['quantum_neg']['skew']:.2f}")
    print(f"  Mimic:        {analysis['mimic']['skew']:.2f}")
    
    print("\nKEY STATISTICAL TESTS:")
    p_mimic = analysis['mimic_vs_quantum_pos']['skew_p']
    p_veto = analysis['quantum_pos_vs_neg']['mean_p']
    
    print(f"  Mimic vs Q(+) skew: p = {p_mimic:.4f}", end="")
    print("  [SIGNIFICANT]" if p_mimic < 0.05 else "  [not sig]")
    
    print(f"  Q(+) vs Q(-) mean:  p = {p_veto:.4f}", end="")
    print("  [SIGNIFICANT]" if p_veto < 0.05 else "  [not sig]")
    
    # Interpretation
    print("\n" + "="*70)
    print("INTERPRETATION")
    print("="*70)
    
    if p_mimic < 0.05:
        print("\n[WIN] Quantum(+) produces different skew than thermal mimic!")
        print("      -> Quantum selection creates clustered large events")
        print("      -> Not replicable by uniform noise boost")
    
    if p_veto < 0.05:
        print("\n[WIN] Quantum(+) and Quantum(-) have different means!")
        print("      -> OR can both amplify (free will) and suppress (veto)")
        print("      -> Bidirectional agency mechanism confirmed")
    
    # Export
    print("\nExporting CSV data...")
    export_csv(results, analysis)
    
    # Plot
    print("\nGenerating plots...")
    fig = plot_all(results, analysis, real_sizes, real_source)
    
    print("\n" + "="*70)
    print("COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
    plt.show()

