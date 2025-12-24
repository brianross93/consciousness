"""
Epoch-Based Quantum Avalanche Simulation

Models the actual OR dynamics:
1. COHERENT PHASE: Superposition accumulates (no bias applied yet)
2. COLLAPSE EVENT: When threshold reached, bias pulse occurs
3. EFFECT PHASE: Network responds to collapse
4. Repeat

This should show entropy building toward state transitions rather than
constant bias effects.
"""

import numpy as np
import networkx as nx
from scipy import stats
from collections import defaultdict

# =============================================================================
# ENTROPY MEASURES
# =============================================================================

def shannon_entropy(activity_vector):
    """Shannon entropy of activity distribution across neurons."""
    if activity_vector.sum() == 0:
        return 0.0
    p = activity_vector / activity_vector.sum()
    p = p[p > 0]  # avoid log(0)
    return -np.sum(p * np.log2(p))


def sample_entropy(time_series, m=2, r=0.2):
    """
    Sample entropy of time series.
    Lower = more predictable/ordered.
    m = embedding dimension, r = tolerance (fraction of std)
    """
    N = len(time_series)
    if N < m + 2:
        return np.nan
    
    r_threshold = r * np.std(time_series)
    if r_threshold == 0:
        return np.nan
    
    def count_matches(template_len):
        count = 0
        for i in range(N - template_len):
            for j in range(i + 1, N - template_len):
                if np.max(np.abs(time_series[i:i+template_len] - 
                                  time_series[j:j+template_len])) <= r_threshold:
                    count += 1
        return count
    
    A = count_matches(m + 1)
    B = count_matches(m)
    
    if A == 0 or B == 0:
        return np.nan
    
    return -np.log(A / B)


def avalanche_size_entropy(avalanche_sizes, n_bins=20):
    """Entropy of avalanche size distribution."""
    if len(avalanche_sizes) == 0:
        return 0.0
    hist, _ = np.histogram(avalanche_sizes, bins=n_bins, density=True)
    hist = hist[hist > 0]
    if len(hist) == 0:
        return 0.0
    return -np.sum(hist * np.log2(hist + 1e-10))


# =============================================================================
# EPOCH-BASED SIMULATION
# =============================================================================

def simulate_epochs(
    N=3000,                    # Number of neurons
    k=10,                      # Connectivity degree
    p=0.1,                     # Rewiring probability
    n_epochs=50,               # Number of OR collapse cycles
    coherence_bins=40,         # Bins for coherence to accumulate (~160ms at 4ms/bin)
    effect_bins=10,            # Bins for effect to propagate after collapse
    prob_fire=0.0002,          # Baseline firing probability
    base_threshold=1.3,        # Propagation threshold
    bias_nodes_fraction=0.1,   # Fraction of nodes that receive bias
    bias_strength=0.0015,      # Magnitude of bias pulse
    bias_mode='positive',      # 'positive', 'negative', or 'none'
    refractory=True,           # Refractory period
    seed=None,
    track_entropy=True
):
    """
    Simulate network with epoch-based bias application.
    
    Each epoch:
    1. COHERENT PHASE (coherence_bins): No bias, normal dynamics
       - Superposition is "building" during this phase
    2. COLLAPSE EVENT: At end of coherent phase, OR collapse occurs
    3. EFFECT PHASE (effect_bins): Bias applied as pulse
       - This is when the quantum selection affects the network
    
    Returns:
        dict with activity counts, entropy trajectories, and epoch markers
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Create network
    G = nx.watts_strogatz_graph(N, k, p, seed=seed)
    for u, v in G.edges():
        G[u][v]['weight'] = np.random.normal(1.0, 0.12)
    
    # Select bias nodes (hubs - highest degree)
    degrees = dict(G.degree())
    n_bias = max(1, int(bias_nodes_fraction * N))
    bias_nodes = np.array(sorted(degrees, key=degrees.get, reverse=True)[:n_bias])
    
    # Storage
    total_bins = n_epochs * (coherence_bins + effect_bins)
    active_counts = []
    entropy_trajectory = {
        'shannon': [],
        'sample_window': [],  # Sample entropy over sliding window
        'phase': [],          # 'coherent' or 'effect'
        'epoch': [],
        'time_in_epoch': []
    }
    
    last_active_mask = np.zeros(N, dtype=bool)
    activity_window = []  # For sample entropy
    window_size = 20
    
    for epoch in range(n_epochs):
        # =====================================================================
        # COHERENT PHASE: Superposition accumulating, no bias yet
        # =====================================================================
        for t in range(coherence_bins):
            # No bias during coherent phase
            prob = np.full(N, prob_fire)
            spontaneous = np.random.rand(N) < prob
            
            # Propagation
            neighbor_hit = np.zeros(N, dtype=bool)
            for u, v in G.edges():
                if last_active_mask[u] and G[u][v]['weight'] > base_threshold:
                    neighbor_hit[v] = True
                if last_active_mask[v] and G[u][v]['weight'] > base_threshold:
                    neighbor_hit[u] = True
            
            active_mask = spontaneous | neighbor_hit
            if refractory:
                active_mask = active_mask & (~last_active_mask)
            
            count = active_mask.sum()
            active_counts.append(count)
            
            # Track entropy
            if track_entropy:
                entropy_trajectory['shannon'].append(
                    shannon_entropy(active_mask.astype(float))
                )
                activity_window.append(count)
                if len(activity_window) > window_size:
                    activity_window.pop(0)
                if len(activity_window) >= window_size:
                    entropy_trajectory['sample_window'].append(
                        sample_entropy(np.array(activity_window))
                    )
                else:
                    entropy_trajectory['sample_window'].append(np.nan)
                entropy_trajectory['phase'].append('coherent')
                entropy_trajectory['epoch'].append(epoch)
                entropy_trajectory['time_in_epoch'].append(t)
            
            last_active_mask = active_mask
        
        # =====================================================================
        # COLLAPSE EVENT: OR happens here
        # =====================================================================
        # (This is the discrete moment - the bias is now "selected")
        
        # =====================================================================
        # EFFECT PHASE: Bias pulse applied
        # =====================================================================
        for t in range(effect_bins):
            # Apply bias during effect phase
            prob = np.full(N, prob_fire)
            
            if bias_mode == 'positive':
                prob[bias_nodes] = np.clip(prob[bias_nodes] + bias_strength, 0, 1)
            elif bias_mode == 'negative':
                prob[bias_nodes] = np.clip(prob[bias_nodes] - bias_strength, 0, 1)
            # 'none' = classical, no bias
            
            spontaneous = np.random.rand(N) < prob
            
            # Propagation
            neighbor_hit = np.zeros(N, dtype=bool)
            for u, v in G.edges():
                if last_active_mask[u] and G[u][v]['weight'] > base_threshold:
                    neighbor_hit[v] = True
                if last_active_mask[v] and G[u][v]['weight'] > base_threshold:
                    neighbor_hit[u] = True
            
            active_mask = spontaneous | neighbor_hit
            if refractory:
                active_mask = active_mask & (~last_active_mask)
            
            count = active_mask.sum()
            active_counts.append(count)
            
            # Track entropy
            if track_entropy:
                entropy_trajectory['shannon'].append(
                    shannon_entropy(active_mask.astype(float))
                )
                activity_window.append(count)
                if len(activity_window) > window_size:
                    activity_window.pop(0)
                if len(activity_window) >= window_size:
                    entropy_trajectory['sample_window'].append(
                        sample_entropy(np.array(activity_window))
                    )
                else:
                    entropy_trajectory['sample_window'].append(np.nan)
                entropy_trajectory['phase'].append('effect')
                entropy_trajectory['epoch'].append(epoch)
                entropy_trajectory['time_in_epoch'].append(coherence_bins + t)
            
            last_active_mask = active_mask
    
    return {
        'counts': np.array(active_counts),
        'entropy': entropy_trajectory,
        'params': {
            'N': N, 'k': k, 'p': p,
            'n_epochs': n_epochs,
            'coherence_bins': coherence_bins,
            'effect_bins': effect_bins,
            'bias_mode': bias_mode,
            'bias_strength': bias_strength
        }
    }


def collapse_to_avalanches(counts, threshold=0):
    """Convert activity counts to avalanche sizes."""
    avalanches = []
    current = 0
    in_avalanche = False
    
    for c in counts:
        if c > threshold:
            in_avalanche = True
            current += c
        else:
            if in_avalanche:
                avalanches.append(current)
                current = 0
                in_avalanche = False
    
    if in_avalanche:
        avalanches.append(current)
    
    return np.array(avalanches)


def fit_power_law(sizes, xmin=1):
    """Fit power law exponent using MLE."""
    sizes = sizes[sizes >= xmin]
    if len(sizes) < 10:
        return np.nan, np.nan
    alpha = 1 + len(sizes) / np.sum(np.log(sizes / xmin))
    stderr = (alpha - 1) / np.sqrt(len(sizes))
    return alpha, stderr


# =============================================================================
# EPOCH ANALYSIS
# =============================================================================

def analyze_epochs(result):
    """
    Analyze entropy dynamics across epochs.
    
    Key questions:
    1. Does entropy decrease during coherent phase (order building)?
    2. Does entropy spike at collapse (state transition)?
    3. Does the pattern differ between Q(+), Q(-), and Classical?
    """
    entropy = result['entropy']
    
    # Separate coherent vs effect phases
    coherent_mask = np.array(entropy['phase']) == 'coherent'
    effect_mask = np.array(entropy['phase']) == 'effect'
    
    # Get sample entropy (more informative than Shannon for time series)
    sample_ent = np.array(entropy['sample_window'])
    valid = ~np.isnan(sample_ent)
    
    # Average entropy by phase
    coherent_entropy = sample_ent[coherent_mask & valid].mean() if (coherent_mask & valid).any() else np.nan
    effect_entropy = sample_ent[effect_mask & valid].mean() if (effect_mask & valid).any() else np.nan
    
    # Entropy change at collapse (end of coherent → start of effect)
    epochs = np.array(entropy['epoch'])
    time_in_epoch = np.array(entropy['time_in_epoch'])
    coherence_bins = result['params']['coherence_bins']
    
    collapse_changes = []
    for e in range(result['params']['n_epochs']):
        # Last bin of coherent phase
        pre_collapse = sample_ent[(epochs == e) & (time_in_epoch == coherence_bins - 1)]
        # First bin of effect phase
        post_collapse = sample_ent[(epochs == e) & (time_in_epoch == coherence_bins)]
        
        if len(pre_collapse) > 0 and len(post_collapse) > 0:
            if not np.isnan(pre_collapse[0]) and not np.isnan(post_collapse[0]):
                collapse_changes.append(post_collapse[0] - pre_collapse[0])
    
    return {
        'coherent_entropy_mean': coherent_entropy,
        'effect_entropy_mean': effect_entropy,
        'entropy_change_at_collapse': np.mean(collapse_changes) if collapse_changes else np.nan,
        'collapse_changes': collapse_changes
    }


def compare_conditions(n_runs=20, **kwargs):
    """
    Run epoch-based simulation for all conditions and compare.
    """
    conditions = ['positive', 'negative', 'none']
    results = {c: [] for c in conditions}
    
    for run in range(n_runs):
        print(f"Run {run+1}/{n_runs}", end='\r')
        
        for cond in conditions:
            result = simulate_epochs(
                bias_mode=cond,
                seed=run * 1000 + hash(cond) % 1000,
                **kwargs
            )
            
            avalanches = collapse_to_avalanches(result['counts'])
            alpha, stderr = fit_power_law(avalanches)
            epoch_analysis = analyze_epochs(result)
            
            results[cond].append({
                'avalanches': avalanches,
                'alpha': alpha,
                'mean': avalanches.mean() if len(avalanches) > 0 else 0,
                'entropy_analysis': epoch_analysis,
                'counts': result['counts']
            })
    
    return results


def print_comparison(results):
    """Print comparison statistics."""
    print("\n" + "="*70)
    print("EPOCH-BASED SIMULATION RESULTS")
    print("="*70)
    
    for cond in ['none', 'positive', 'negative']:
        alphas = [r['alpha'] for r in results[cond] if not np.isnan(r['alpha'])]
        means = [r['mean'] for r in results[cond]]
        coherent_ent = [r['entropy_analysis']['coherent_entropy_mean'] 
                       for r in results[cond] if not np.isnan(r['entropy_analysis']['coherent_entropy_mean'])]
        effect_ent = [r['entropy_analysis']['effect_entropy_mean'] 
                     for r in results[cond] if not np.isnan(r['entropy_analysis']['effect_entropy_mean'])]
        collapse_changes = []
        for r in results[cond]:
            collapse_changes.extend(r['entropy_analysis']['collapse_changes'])
        
        label = {'none': 'Classical', 'positive': 'Q(+)', 'negative': 'Q(-)'}[cond]
        
        print(f"\n{label}:")
        print(f"  Alpha: {np.mean(alphas):.2f} ± {np.std(alphas):.2f}")
        print(f"  Mean avalanche: {np.mean(means):.1f}")
        if coherent_ent:
            print(f"  Coherent phase entropy: {np.mean(coherent_ent):.3f}")
        if effect_ent:
            print(f"  Effect phase entropy: {np.mean(effect_ent):.3f}")
        if collapse_changes:
            print(f"  Entropy change at collapse: {np.mean(collapse_changes):.3f} ± {np.std(collapse_changes):.3f}")
    
    # Statistical tests
    print("\n" + "-"*70)
    print("STATISTICAL TESTS")
    print("-"*70)
    
    # Alpha comparison
    alpha_pos = [r['alpha'] for r in results['positive'] if not np.isnan(r['alpha'])]
    alpha_neg = [r['alpha'] for r in results['negative'] if not np.isnan(r['alpha'])]
    alpha_classical = [r['alpha'] for r in results['none'] if not np.isnan(r['alpha'])]
    
    if alpha_pos and alpha_neg:
        t, p = stats.ttest_ind(alpha_pos, alpha_neg)
        print(f"Q(+) vs Q(-) alpha: t={t:.2f}, p={p:.4f}")
    
    if alpha_pos and alpha_classical:
        t, p = stats.ttest_ind(alpha_pos, alpha_classical)
        print(f"Q(+) vs Classical alpha: t={t:.2f}, p={p:.4f}")
    
    # Entropy change comparison
    collapse_pos = []
    collapse_neg = []
    for r in results['positive']:
        collapse_pos.extend(r['entropy_analysis']['collapse_changes'])
    for r in results['negative']:
        collapse_neg.extend(r['entropy_analysis']['collapse_changes'])
    
    if collapse_pos and collapse_neg:
        t, p = stats.ttest_ind(collapse_pos, collapse_neg)
        print(f"Entropy change at collapse Q(+) vs Q(-): t={t:.2f}, p={p:.4f}")


# =============================================================================
# REAL DATA COMPARISON
# =============================================================================

def segment_real_data_into_epochs(activity_counts, epoch_bins=50, overlap=0.5):
    """
    Segment real neural data into overlapping epochs for entropy analysis.
    
    Args:
        activity_counts: Array of activity counts per time bin
        epoch_bins: Number of bins per epoch
        overlap: Fraction of overlap between epochs
    
    Returns:
        List of epoch entropy values
    """
    step = int(epoch_bins * (1 - overlap))
    epochs = []
    
    for start in range(0, len(activity_counts) - epoch_bins, step):
        epoch_data = activity_counts[start:start + epoch_bins]
        
        # Compute sample entropy for this epoch
        if len(epoch_data) >= 10:
            ent = sample_entropy(epoch_data.astype(float))
            if not np.isnan(ent):
                epochs.append({
                    'start': start,
                    'entropy': ent,
                    'mean_activity': epoch_data.mean(),
                    'std_activity': epoch_data.std()
                })
    
    return epochs


def classify_epochs(epochs, threshold_low=None, threshold_high=None):
    """
    Classify epochs as Q(-)-like (low entropy, ordered), 
    Q(+)-like (high entropy, disordered), or neutral.
    
    If thresholds not provided, uses 25th and 75th percentiles.
    """
    entropies = [e['entropy'] for e in epochs]
    
    if threshold_low is None:
        threshold_low = np.percentile(entropies, 25)
    if threshold_high is None:
        threshold_high = np.percentile(entropies, 75)
    
    for e in epochs:
        if e['entropy'] < threshold_low:
            e['classification'] = 'Q(-)-like'  # Ordered, veto-dominated
        elif e['entropy'] > threshold_high:
            e['classification'] = 'Q(+)-like'  # Disordered, promote-dominated
        else:
            e['classification'] = 'neutral'
    
    return epochs, threshold_low, threshold_high


def analyze_entropy_distribution(epochs):
    """Analyze the distribution of epoch entropies."""
    entropies = [e['entropy'] for e in epochs]
    
    # Test for normality vs bimodality
    # Bimodality would suggest two distinct states (Q+ vs Q-)
    from scipy.stats import skew, kurtosis
    
    return {
        'mean': np.mean(entropies),
        'std': np.std(entropies),
        'skew': skew(entropies),
        'kurtosis': kurtosis(entropies),
        'n_epochs': len(epochs),
        'q_minus_fraction': len([e for e in epochs if e.get('classification') == 'Q(-)-like']) / len(epochs) if epochs else 0,
        'q_plus_fraction': len([e for e in epochs if e.get('classification') == 'Q(+)-like']) / len(epochs) if epochs else 0
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Running epoch-based quantum avalanche simulation...")
    print("This models OR collapse as discrete events with accumulation phases.\n")
    
    # Parameters matched to user's successful calibration
    results = compare_conditions(
        n_runs=20,
        N=3000,
        k=8,
        p=0.1,
        n_epochs=50,
        coherence_bins=40,      # ~160ms at 4ms/bin
        effect_bins=10,         # ~40ms effect window
        prob_fire=0.0002,
        base_threshold=1.3,
        bias_nodes_fraction=0.1,
        bias_strength=0.0015,
        refractory=True
    )
    
    print_comparison(results)
    
    print("\n" + "="*70)
    print("INTERPRETATION")
    print("="*70)
    print("""
Key predictions for epoch-based model:

1. ENTROPY TRAJECTORY:
   - Coherent phase should show gradually decreasing entropy (order building)
   - Collapse moment should show entropy spike or transition
   - Effect phase should show new (lower?) entropy state
   
2. Q(+) vs Q(-) ASYMMETRY:
   - Q(+) should show larger entropy drops at collapse (stronger state transition)
   - Q(-) should maintain more stable entropy (veto prevents transition)
   
3. POWER LAW PRESERVATION:
   - Classical and Q(-) should maintain alpha ~ 1.5-1.6 (criticality preserved)
   - Q(+) might still show lower alpha, but ONLY during effect phases
   
4. WHAT TO COMPARE WITH REAL DATA:
   - Segment real hc-3 data into epochs
   - Look for entropy signatures that match coherent -> collapse -> effect pattern
   - If found, this is evidence for pulsed quantum effects, not continuous bias
""")

