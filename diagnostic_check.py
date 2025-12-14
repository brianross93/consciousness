"""
Diagnostic check for simulation parameters and logic
"""

import numpy as np

print("="*60)
print("DIAGNOSTIC CHECK")
print("="*60)
print()

# Check OR Collapse parameters
print("1. OR COLLAPSE SCALING PARAMETERS:")
print("-" * 40)
hbar = 1.0545718e-34
G = 6.67430e-11
m = 1e-22
d = 1e-9

# What parameters give ~0.1s for N=10^10?
target_tau = 0.1  # 100 ms
N_target = 1e10
E_g_needed = hbar / target_tau
print(f"Target: tau = {target_tau} s for N = {N_target}")
print(f"E_g needed: {E_g_needed:.2e} J")
print(f"Current E_g per tubulin: {G * m**2 / d:.2e} J")
print(f"Current E_g for N={N_target}: {(G * m**2 / d) * N_target:.2e} J")
print()

# Calculate what d would give us target
d_needed = (G * m**2 * N_target) / E_g_needed
print(f"To get tau={target_tau}s, we need d = {d_needed*1e9:.3f} nm (vs current {d*1e9:.1f} nm)")
print()

# Or what mass
m_needed = np.sqrt((E_g_needed / N_target) * d / G)
print(f"To get tau={target_tau}s, we need m = {m_needed*1e22:.3f}x10^-22 kg (vs current {m*1e22:.1f}x10^-22 kg)")
print()

print("2. AVALANCHE SIMULATION PARAMETERS:")
print("-" * 40)
print("Edge weight distribution:")
thermal_mean = 1.0
thermal_std = 0.1
threshold = 1.2
bias_strength = 0.05
bias_fraction = 0.1

print(f"  Thermal baseline: mean={thermal_mean}, std={thermal_std}")
print(f"  Threshold: {threshold}")
print(f"  Quantum bias: +{bias_strength} on {bias_fraction*100}% of edges")
print()

# Probability edge exceeds threshold
from scipy import stats
prob_above_threshold = 1 - stats.norm.cdf(threshold, thermal_mean, thermal_std)
print(f"  Probability edge exceeds threshold (baseline): {prob_above_threshold:.3f}")
prob_above_threshold_biased = 1 - stats.norm.cdf(threshold - bias_strength, thermal_mean, thermal_std)
print(f"  Probability edge exceeds threshold (after bias): {prob_above_threshold_biased:.3f}")
print(f"  Improvement: {prob_above_threshold_biased / prob_above_threshold:.2f}x")
print()

# Network connectivity
N_nodes = 1000
k = 10
p = 0.1
n_edges_approx = int(N_nodes * k / 2)  # Undirected graph
print(f"Network: {N_nodes} nodes, ~{n_edges_approx} edges")
print(f"  Mean degree: {k}")
print(f"  Expected edges with bias: {int(n_edges_approx * bias_fraction)}")
print()

print("3. POTENTIAL ISSUES:")
print("-" * 40)
print("OR Collapse:")
print("  [*] Current parameters give tau ~10s for N=10^10, not ~0.1s")
print("  [*] Need smaller d (~0.01 nm) or smaller m to hit neural timescales")
print("  [*] OR need larger N (~10^12) to compensate")
print()
print("Avalanche Bias:")
print("  [*] Only ~15.9% of edges exceed threshold even after bias")
print("  [*] Network might be too sparse for avalanches to propagate")
print("  [*] Bias might need to be stronger or on more edges")
print("  [*] Same random seed used - quantum bias is deterministic per run")

