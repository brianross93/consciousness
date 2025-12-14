"""
Avalanche Bias Simulation - Quantum Steering in Neural Networks
================================================================

Tests Crux 2: Can quantum bias (via OR collapse) steer neural avalanches
differently than classical thermal noise alone?

Uses NetworkX Watts-Strogatz brain-like network with:
- Classical control: Pure thermal noise
- Quantum-biased: OR collapse provides probabilistic edge weight nudge

Key test: Do quantum-biased runs show sharper decision forks (non-Gaussian tails)?
This would indicate quantum-specific steering beyond classical stochasticity.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import warnings
import os
warnings.filterwarnings('ignore')


def create_brain_network(N=1000, k=10, p=0.1):
    """
    Create a Watts-Strogatz small-world network (brain proxy).
    
    Parameters:
    -----------
    N : int
        Number of nodes (neurons/regions)
    k : int
        Mean degree (connectivity)
    p : float
        Rewiring probability (0 = regular, 1 = random)
        
    Returns:
    --------
    G : networkx.Graph
        The network with random edge weights (thermal noise)
    """
    G = nx.watts_strogatz_graph(N, k, p, seed=42)
    
    # Initialize edges with thermal noise (classical baseline)
    # Lower threshold (0.9) so more edges can participate in avalanches
    np.random.seed(42)
    for u, v in G.edges():
        # Normal distribution around 1.0 with thermal fluctuations
        G[u][v]['weight'] = np.random.normal(1.0, 0.15)  # Moderate std
        G[u][v]['original_weight'] = G[u][v]['weight']
    
    return G


def avalanche_size(G, source, threshold=1.1):  # Balanced threshold
    """
    Simulate neural avalanche from seed node using BFS.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network with edge weights
    source : int
        Starting node for avalanche
    threshold : float
        Minimum weight to propagate
        
    Returns:
    --------
    size : int
        Number of nodes activated in avalanche
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
        
        # Propagate to neighbors above threshold
        for v in G.neighbors(u):
            if G[u][v]['weight'] > threshold and v not in visited:
                queue.append(v)
    
    return size


def run_classical_simulation(G, n_seeds=100):
    """
    Run classical (pure thermal) avalanche simulation.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network (edges reset to thermal baseline)
    n_seeds : int
        Number of random seeds to test
        
    Returns:
    --------
    sizes : list
        Avalanche sizes for each seed
    """
    # Reset all edges to thermal baseline
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['original_weight']
    
    sizes = []
    np.random.seed(42)  # Reproducibility
    seeds = np.random.choice(list(G.nodes()), size=n_seeds, replace=False)
    
    for seed in seeds:
        size = avalanche_size(G, seed)
        sizes.append(size)
    
    return sizes


def run_quantum_biased_simulation(G, n_seeds=100, bias_fraction=0.2, bias_strength=0.15):
    """
    Run quantum-biased simulation with OR collapse nudge.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network
    n_seeds : int
        Number of random seeds
    bias_fraction : float
        Fraction of edges that receive quantum bias (0.1 = 10%)
    bias_strength : float
        Strength of quantum nudge (+bias_strength to weight)
        
    Returns:
    --------
    sizes : list
        Avalanche sizes for each seed
    """
    # Reset to thermal baseline
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['original_weight']
    
    # Apply quantum bias: OR collapse nudges subset of edges
    edge_list = list(G.edges())
    n_bias = int(len(edge_list) * bias_fraction)
    bias_indices = np.random.choice(len(edge_list), size=n_bias, replace=False)
    bias_edges = [edge_list[i] for i in bias_indices]
    
    # Quantum selection: probabilistic nudge (like OR collapse outcome)
    for u, v in bias_edges:
        # OR collapse provides probabilistic selection
        # In reality, this would be quantum-mechanically determined
        # Here we model it as a small positive bias
        G[u][v]['weight'] += bias_strength
    
    # Run avalanches
    sizes = []
    # Use different seed for quantum - quantum collapse is probabilistic!
    np.random.seed(43)  # Different seed to show quantum variability
    seeds = np.random.choice(list(G.nodes()), size=n_seeds, replace=False)
    
    for seed in seeds:
        size = avalanche_size(G, seed)
        sizes.append(size)
    
    return sizes


def analyze_will_variance(sizes_classical, sizes_quantum):
    """
    Analyze "will variance" - non-Gaussian tails in quantum runs.
    
    Parameters:
    -----------
    sizes_classical : list
        Classical avalanche sizes
    sizes_quantum : list
        Quantum-biased avalanche sizes
        
    Returns:
    --------
    stats : dict
        Statistical comparison
    """
    sizes_classical = np.array(sizes_classical)
    sizes_quantum = np.array(sizes_quantum)
    
    stats = {
        'classical_mean': np.mean(sizes_classical),
        'quantum_mean': np.mean(sizes_quantum),
        'classical_std': np.std(sizes_classical),
        'quantum_std': np.std(sizes_quantum),
        'classical_skew': np.mean(((sizes_classical - np.mean(sizes_classical)) / np.std(sizes_classical))**3),
        'quantum_skew': np.mean(((sizes_quantum - np.mean(sizes_quantum)) / np.std(sizes_quantum))**3),
    }
    
    # Check for non-Gaussian tails (large avalanches)
    threshold = np.percentile(sizes_classical, 95)
    large_classical = np.sum(sizes_classical > threshold)
    large_quantum = np.sum(sizes_quantum > threshold)
    
    stats['large_avalanche_fraction_classical'] = large_classical / len(sizes_classical)
    stats['large_avalanche_fraction_quantum'] = large_quantum / len(sizes_quantum)
    
    return stats


def main():
    """Run the simulation and generate analysis."""
    
    print("="*60)
    print("AVALANCHE BIAS SIMULATION")
    print("Quantum Steering vs Classical Noise")
    print("="*60)
    print()
    
    # Create brain-like network
    print("Creating Watts-Strogatz network (brain proxy)...")
    G = create_brain_network(N=1000, k=10, p=0.1)
    print(f"[OK] Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print()
    
    # Run simulations
    print("Running simulations...")
    print("  Classical (pure thermal): ", end="", flush=True)
    sizes_classical = run_classical_simulation(G, n_seeds=100)
    print(f"[OK] ({len(sizes_classical)} avalanches)")
    
    print("  Quantum-biased (OR nudge): ", end="", flush=True)
    sizes_quantum = run_quantum_biased_simulation(G, n_seeds=100, 
                                                   bias_fraction=0.2,  # Increased from 0.1
                                                   bias_strength=0.15)  # Increased from 0.05
    print(f"[OK] ({len(sizes_quantum)} avalanches)")
    print()
    
    # Analyze
    stats = analyze_will_variance(sizes_classical, sizes_quantum)
    
    print("Results:")
    print(f"  Classical mean size:  {stats['classical_mean']:.2f} +/-  {stats['classical_std']:.2f}")
    print(f"  Quantum mean size:    {stats['quantum_mean']:.2f} +/-  {stats['quantum_std']:.2f}")
    print(f"  Classical skewness:   {stats['classical_skew']:.3f}")
    print(f"  Quantum skewness:     {stats['quantum_skew']:.3f}")
    print(f"  Large avalanches (>95th percentile):")
    print(f"    Classical: {stats['large_avalanche_fraction_classical']:.1%}")
    print(f"    Quantum:   {stats['large_avalanche_fraction_quantum']:.1%}")
    print()
    
    # Create comparison plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram comparison
    ax1 = axes[0]
    bins = np.arange(0, max(max(sizes_classical), max(sizes_quantum)) + 2)
    ax1.hist(sizes_classical, bins=bins, alpha=0.6, label='Classical (Thermal)', 
             color='blue', edgecolor='black', linewidth=0.5)
    ax1.hist(sizes_quantum, bins=bins, alpha=0.6, label='Quantum Biased', 
             color='red', edgecolor='black', linewidth=0.5)
    ax1.set_xlabel('Avalanche Size', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax1.set_title('Avalanche Size Distribution\n(Quantum Bias = OR Collapse Nudge)', 
                  fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Cumulative distribution (to see tails)
    ax2 = axes[1]
    sorted_classical = np.sort(sizes_classical)
    sorted_quantum = np.sort(sizes_quantum)
    p_classical = np.arange(1, len(sorted_classical) + 1) / len(sorted_classical)
    p_quantum = np.arange(1, len(sorted_quantum) + 1) / len(sorted_quantum)
    
    ax2.plot(sorted_classical, p_classical, 'b-', linewidth=2, 
             label='Classical (Thermal)', alpha=0.8)
    ax2.plot(sorted_quantum, p_quantum, 'r-', linewidth=2, 
             label='Quantum Biased', alpha=0.8)
    ax2.set_xlabel('Avalanche Size', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Cumulative Probability', fontsize=11, fontweight='bold')
    ax2.set_title('Cumulative Distribution\n(Check for Non-Gaussian Tails)', 
                  fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    os.makedirs('data/avalanche_bias_sim', exist_ok=True)
    plt.savefig('data/avalanche_bias_sim/avalanche_bias_comparison.png', dpi=150, bbox_inches='tight')
    print("[OK] Plot saved: avalanche_bias_comparison.png")
    print()
    
    # Vary bias strength (meditator vs fatigued)
    print("Varying quantum bias strength (will state):")
    bias_strengths = [0.05, 0.10, 0.15, 0.20, 0.25]
    mean_sizes = []
    
    for bias in bias_strengths:
        sizes = run_quantum_biased_simulation(G, n_seeds=100, 
                                              bias_fraction=0.2, 
                                              bias_strength=bias)
        mean_sizes.append(np.mean(sizes))
        print(f"  Bias = {bias:.2f} -> Mean avalanche size = {np.mean(sizes):.2f}")
    
    # Plot bias strength effect
    fig2, ax = plt.subplots(figsize=(8, 5))
    ax.plot(bias_strengths, mean_sizes, 'ro-', linewidth=2, markersize=8)
    ax.set_xlabel('Quantum Bias Strength (OR Collapse Nudge)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Mean Avalanche Size', fontsize=11, fontweight='bold')
    ax.set_title('Effect of Quantum Bias Strength\n(Meditator vs. Fatigued)', 
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=stats['classical_mean'], color='blue', linestyle='--', 
               label=f'Classical baseline ({stats["classical_mean"]:.2f})')
    ax.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('data/avalanche_bias_sim/bias_strength_effect.png', dpi=150, bbox_inches='tight')
    print()
    print("[OK] Plot saved: bias_strength_effect.png")
    print()
    
    print("="*60)
    print("Interpretation:")
    print("="*60)
    print("• If quantum runs show sharper decision forks (non-Gaussian tails),")
    print("  it indicates quantum-specific steering beyond classical noise")
    print("• Testable twist: Quantify 'will variance'—vary bias strength")
    print("  (meditator vs. fatigued) to see if quantum runs cluster non-randomly")
    print("• Scale to 10k nodes for full brain simulation")
    print()


if __name__ == "__main__":
    main()
    plt.show()

