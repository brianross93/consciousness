"""
Brain Cascade Animation
=======================

Animated visualization of neural avalanche cascading through a brain-like network.
Shows side-by-side comparison of Classical vs Quantum-biased avalanche propagation.

Exports to MP4 for use in videos.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.patches import Circle
import matplotlib.patches as mpatches
import os
import warnings
warnings.filterwarnings('ignore')


def create_brain_network(N=200, k=6, p=0.1, seed=42):
    """Create a brain-like small-world network."""
    G = nx.watts_strogatz_graph(N, k, p, seed=seed)
    
    # Add edge weights
    np.random.seed(seed)
    for u, v in G.edges():
        G[u][v]['weight'] = np.random.normal(1.0, 0.12)
        G[u][v]['original_weight'] = G[u][v]['weight']
    
    return G


def get_brain_layout(G, seed=42):
    """
    Create a brain-shaped layout for the network.
    Uses an elliptical arrangement with some clustering.
    """
    np.random.seed(seed)
    N = len(G.nodes())
    
    # Create elliptical brain shape
    pos = {}
    for i, node in enumerate(G.nodes()):
        # Angle around ellipse
        theta = 2 * np.pi * i / N + np.random.normal(0, 0.1)
        
        # Ellipse with some noise for organic look
        # Left hemisphere (negative x) and right hemisphere (positive x)
        r = 0.8 + np.random.normal(0, 0.15)
        x = r * np.cos(theta) * 1.3  # Wider horizontally
        y = r * np.sin(theta) * 0.9  # Narrower vertically
        
        # Add some internal nodes (not just on the edge)
        if np.random.random() < 0.4:
            x *= np.random.uniform(0.3, 0.9)
            y *= np.random.uniform(0.3, 0.9)
        
        pos[node] = (x, y)
    
    return pos


def simulate_cascade_steps(G, source, threshold=1.05, max_steps=50):
    """
    Simulate avalanche and return activation at each time step.
    
    Returns:
    --------
    steps : list of sets
        Each element is the set of nodes activated at that step
    """
    activated = set()
    frontier = {source}
    steps = [frontier.copy()]
    activated.add(source)
    
    for _ in range(max_steps):
        new_frontier = set()
        for u in frontier:
            for v in G.neighbors(u):
                if v not in activated and G[u][v]['weight'] > threshold:
                    new_frontier.add(v)
                    activated.add(v)
        
        if not new_frontier:
            break
        
        steps.append(new_frontier.copy())
        frontier = new_frontier
    
    return steps


def apply_quantum_bias(G, bias_fraction=0.15, bias_strength=0.08, seed=None):
    """Apply selective quantum bias to edges."""
    if seed is not None:
        np.random.seed(seed)
    
    # Reset first
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['original_weight']
    
    # Apply selective bias
    edge_list = list(G.edges())
    n_bias = max(1, int(len(edge_list) * bias_fraction))
    bias_indices = np.random.choice(len(edge_list), size=n_bias, replace=False)
    
    for idx in bias_indices:
        u, v = edge_list[idx]
        G[u][v]['weight'] += bias_strength


def reset_network(G):
    """Reset network to original weights."""
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['original_weight']


def create_cascade_animation(save_path='data/brain_cascade.mp4', fps=10, dpi=120):
    """
    Create side-by-side animation of Classical vs Quantum cascade.
    """
    print("Creating brain cascade animation...")
    print("=" * 60)
    
    # Create network
    N_NODES = 200
    G_classical = create_brain_network(N=N_NODES, k=6, p=0.1, seed=42)
    G_quantum = create_brain_network(N=N_NODES, k=6, p=0.1, seed=42)
    
    # Get brain-shaped layout (same for both)
    pos = get_brain_layout(G_classical, seed=42)
    
    # Apply quantum bias
    apply_quantum_bias(G_quantum, bias_fraction=0.15, bias_strength=0.08, seed=123)
    
    # Choose seed node (center-ish)
    nodes = list(G_classical.nodes())
    # Find node closest to center
    center_node = min(nodes, key=lambda n: pos[n][0]**2 + pos[n][1]**2)
    
    # Simulate cascades
    print(f"Simulating from seed node {center_node}...")
    steps_classical = simulate_cascade_steps(G_classical, center_node, threshold=1.05)
    steps_quantum = simulate_cascade_steps(G_quantum, center_node, threshold=1.05)
    
    # Pad to same length
    max_steps = max(len(steps_classical), len(steps_quantum))
    while len(steps_classical) < max_steps:
        steps_classical.append(set())
    while len(steps_quantum) < max_steps:
        steps_quantum.append(set())
    
    print(f"Classical cascade: {sum(len(s) for s in steps_classical)} nodes in {len(steps_classical)} steps")
    print(f"Quantum cascade: {sum(len(s) for s in steps_quantum)} nodes in {len(steps_quantum)} steps")
    
    # Build cumulative activation for coloring
    def build_cumulative(steps):
        cumulative = []
        activated = set()
        for step in steps:
            activated = activated | step
            cumulative.append(activated.copy())
        return cumulative
    
    cum_classical = build_cumulative(steps_classical)
    cum_quantum = build_cumulative(steps_quantum)
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    fig.patch.set_facecolor('#1a1a2e')
    
    for ax in [ax1, ax2]:
        ax.set_facecolor('#1a1a2e')
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect('equal')
        ax.axis('off')
    
    ax1.set_title('CLASSICAL\n(Thermal Noise Only)', fontsize=14, fontweight='bold', 
                  color='#4fc3f7', pad=10)
    ax2.set_title('QUANTUM-BIASED\n(OR Collapse Nudge)', fontsize=14, fontweight='bold', 
                  color='#ff7043', pad=10)
    
    # Draw edges (faint)
    edge_alpha = 0.08
    for u, v in G_classical.edges():
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        ax1.plot(x, y, color='#555555', alpha=edge_alpha, linewidth=0.3)
        ax2.plot(x, y, color='#555555', alpha=edge_alpha, linewidth=0.3)
    
    # Initialize node scatter plots
    node_positions = np.array([pos[n] for n in nodes])
    
    # Colors: inactive=dark, active=bright
    inactive_color = '#333344'
    active_colors = plt.cm.plasma(np.linspace(0.2, 0.9, max_steps))
    seed_color = '#00ff00'
    
    scatter1 = ax1.scatter(node_positions[:, 0], node_positions[:, 1], 
                           c=[inactive_color]*N_NODES, s=30, zorder=5, edgecolors='none')
    scatter2 = ax2.scatter(node_positions[:, 0], node_positions[:, 1], 
                           c=[inactive_color]*N_NODES, s=30, zorder=5, edgecolors='none')
    
    # Time indicator
    time_text = fig.text(0.5, 0.02, '', ha='center', fontsize=12, color='white')
    
    # Count indicators
    count1_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes, fontsize=11, 
                           color='#4fc3f7', verticalalignment='top', fontweight='bold')
    count2_text = ax2.text(0.02, 0.98, '', transform=ax2.transAxes, fontsize=11, 
                           color='#ff7043', verticalalignment='top', fontweight='bold')
    
    def get_colors(cumulative_at_step, steps_list, step_idx, n_nodes, nodes_list):
        """Get color array for current state."""
        colors = []
        for node in nodes_list:
            if step_idx > 0 and node == center_node:
                colors.append(seed_color)
            elif node in cumulative_at_step:
                # Find which step this node was activated
                for s_idx, step_set in enumerate(steps_list[:step_idx+1]):
                    if node in step_set:
                        colors.append(active_colors[min(s_idx, max_steps-1)])
                        break
                else:
                    colors.append(active_colors[0])
            else:
                colors.append(inactive_color)
        return colors
    
    def animate(frame):
        # Add pause at beginning and end
        pause_frames = 15
        if frame < pause_frames:
            step_idx = 0
        elif frame >= pause_frames + max_steps:
            step_idx = max_steps - 1
        else:
            step_idx = frame - pause_frames
        
        step_idx = min(step_idx, max_steps - 1)
        
        # Get current cumulative activations
        cum_c = cum_classical[step_idx] if step_idx < len(cum_classical) else cum_classical[-1]
        cum_q = cum_quantum[step_idx] if step_idx < len(cum_quantum) else cum_quantum[-1]
        
        # Update colors
        colors1 = get_colors(cum_c, steps_classical, step_idx, N_NODES, nodes)
        colors2 = get_colors(cum_q, steps_quantum, step_idx, N_NODES, nodes)
        
        scatter1.set_color(colors1)
        scatter2.set_color(colors2)
        
        # Update sizes (active nodes slightly larger)
        sizes1 = [50 if n in cum_c else 25 for n in nodes]
        sizes2 = [50 if n in cum_q else 25 for n in nodes]
        scatter1.set_sizes(sizes1)
        scatter2.set_sizes(sizes2)
        
        # Update text
        if frame < pause_frames:
            time_text.set_text('Starting cascade from center node...')
        else:
            time_text.set_text(f'Time Step: {step_idx + 1} / {max_steps}')
        
        count1_text.set_text(f'Active: {len(cum_c)} nodes')
        count2_text.set_text(f'Active: {len(cum_q)} nodes')
        
        return scatter1, scatter2, time_text, count1_text, count2_text
    
    # Create animation
    pause_frames = 15
    total_frames = pause_frames + max_steps + 30
    
    print(f"Creating {total_frames} frames...")
    anim = FuncAnimation(fig, animate, frames=total_frames, interval=1000//fps, blit=False)
    
    # Save
    os.makedirs('data', exist_ok=True)
    
    # Try MP4 first, fall back to GIF
    try:
        print(f"Saving to {save_path}...")
        writer = FFMpegWriter(fps=fps, metadata={'title': 'Brain Cascade'})
        anim.save(save_path, writer=writer, dpi=dpi)
        print(f"[OK] Saved: {save_path}")
    except Exception as e:
        print(f"MP4 failed ({e}), trying GIF...")
        gif_path = save_path.replace('.mp4', '.gif')
        writer = PillowWriter(fps=fps)
        anim.save(gif_path, writer=writer, dpi=dpi)
        print(f"[OK] Saved: {gif_path}")
    
    plt.close()
    return anim


def create_single_brain_cascade(save_path='data/brain_cascade_single.png', dpi=150):
    """
    Create a static multi-panel showing cascade progression.
    Good for thumbnail or static visualization.
    """
    print("\nCreating static cascade progression...")
    
    N_NODES = 200
    G = create_brain_network(N=N_NODES, seed=42)
    apply_quantum_bias(G, bias_fraction=0.15, bias_strength=0.08, seed=123)
    
    pos = get_brain_layout(G, seed=42)
    nodes = list(G.nodes())
    center_node = min(nodes, key=lambda n: pos[n][0]**2 + pos[n][1]**2)
    
    steps = simulate_cascade_steps(G, center_node, threshold=1.05)
    
    # Build cumulative
    cumulative = []
    activated = set()
    for step in steps:
        activated = activated | step
        cumulative.append(activated.copy())
    
    # Show 6 time points
    n_panels = 6
    indices = np.linspace(0, len(cumulative)-1, n_panels).astype(int)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.patch.set_facecolor('#1a1a2e')
    axes = axes.flatten()
    
    node_positions = np.array([pos[n] for n in nodes])
    
    for i, (ax, idx) in enumerate(zip(axes, indices)):
        ax.set_facecolor('#1a1a2e')
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Draw edges
        for u, v in G.edges():
            x = [pos[u][0], pos[v][0]]
            y = [pos[u][1], pos[v][1]]
            ax.plot(x, y, color='#444444', alpha=0.1, linewidth=0.3)
        
        # Color nodes
        cum_at_step = cumulative[idx]
        colors = []
        sizes = []
        for node in nodes:
            if node == center_node:
                colors.append('#00ff00')
                sizes.append(80)
            elif node in cum_at_step:
                colors.append('#ff6b35')
                sizes.append(50)
            else:
                colors.append('#333344')
                sizes.append(20)
        
        ax.scatter(node_positions[:, 0], node_positions[:, 1], c=colors, s=sizes, zorder=5)
        
        ax.set_title(f't = {idx+1}\n{len(cum_at_step)} nodes active', 
                    fontsize=11, color='white', fontweight='bold')
    
    fig.suptitle('NEURAL AVALANCHE CASCADE\nQuantum-Biased Network', 
                 fontsize=16, fontweight='bold', color='#ff7043', y=0.98)
    
    plt.tight_layout()
    os.makedirs('data', exist_ok=True)
    plt.savefig(save_path, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches='tight')
    print(f"[OK] Saved: {save_path}")
    plt.close()


def create_comparison_final_state(save_path='data/cascade_comparison_final.png', dpi=150):
    """
    Show final state of Classical vs Quantum side by side.
    """
    print("\nCreating final state comparison...")
    
    N_NODES = 300
    G_classical = create_brain_network(N=N_NODES, k=6, p=0.1, seed=42)
    G_quantum = create_brain_network(N=N_NODES, k=6, p=0.1, seed=42)
    
    pos = get_brain_layout(G_classical, seed=42)
    apply_quantum_bias(G_quantum, bias_fraction=0.15, bias_strength=0.08, seed=123)
    
    nodes = list(G_classical.nodes())
    center_node = min(nodes, key=lambda n: pos[n][0]**2 + pos[n][1]**2)
    
    # Run cascades
    steps_c = simulate_cascade_steps(G_classical, center_node)
    steps_q = simulate_cascade_steps(G_quantum, center_node)
    
    final_c = set().union(*steps_c)
    final_q = set().union(*steps_q)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    fig.patch.set_facecolor('#1a1a2e')
    
    node_positions = np.array([pos[n] for n in nodes])
    
    for ax, final_set, title, color in [
        (ax1, final_c, f'CLASSICAL\n{len(final_c)} nodes activated', '#4fc3f7'),
        (ax2, final_q, f'QUANTUM-BIASED\n{len(final_q)} nodes activated', '#ff7043')
    ]:
        ax.set_facecolor('#1a1a2e')
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Edges
        for u, v in G_classical.edges():
            x = [pos[u][0], pos[v][0]]
            y = [pos[u][1], pos[v][1]]
            ax.plot(x, y, color='#444444', alpha=0.08, linewidth=0.3)
        
        # Nodes
        colors = []
        sizes = []
        for node in nodes:
            if node == center_node:
                colors.append('#00ff00')
                sizes.append(100)
            elif node in final_set:
                colors.append(color)
                sizes.append(50)
            else:
                colors.append('#333344')
                sizes.append(20)
        
        ax.scatter(node_positions[:, 0], node_positions[:, 1], c=colors, s=sizes, zorder=5)
        ax.set_title(title, fontsize=14, fontweight='bold', color=color, pad=15)
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor='#00ff00', label='Seed Node'),
        mpatches.Patch(facecolor='#4fc3f7', label='Classical Active'),
        mpatches.Patch(facecolor='#ff7043', label='Quantum Active'),
        mpatches.Patch(facecolor='#333344', label='Inactive'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, 
               fontsize=10, facecolor='#1a1a2e', edgecolor='white',
               labelcolor='white')
    
    fig.suptitle('AVALANCHE FINAL STATE: Same Seed, Different Outcomes', 
                 fontsize=16, fontweight='bold', color='white', y=0.95)
    
    plt.tight_layout(rect=[0, 0.08, 1, 0.92])
    os.makedirs('data', exist_ok=True)
    plt.savefig(save_path, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches='tight')
    print(f"[OK] Saved: {save_path}")
    plt.close()


if __name__ == "__main__":
    print("=" * 60)
    print("BRAIN CASCADE VISUALIZATION")
    print("=" * 60)
    print()
    
    # Create static comparisons first (fast)
    create_comparison_final_state('data/cascade_comparison_final.png')
    create_single_brain_cascade('data/brain_cascade_progression.png')
    
    # Create animation (slower, requires ffmpeg for mp4)
    print("\nAttempting animation (requires ffmpeg for MP4, falls back to GIF)...")
    create_cascade_animation('data/brain_cascade.mp4', fps=12, dpi=100)
    
    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
