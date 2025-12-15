"""
Enhanced Brain Visualization
============================

1. Brain-shaped network (anatomical outline)
2. Pulse effect (glow on fresh activation)
3. 3D rotating brain
4. Master summary figure

For the consciousness/free will video.
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Polygon, Circle, Ellipse
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import os
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# BRAIN SHAPE UTILITIES
# =============================================================================

def brain_outline_2d():
    """
    Generate 2D brain outline (side view / lateral).
    Returns list of (x, y) points forming the brain silhouette.
    """
    t = np.linspace(0, 2*np.pi, 200)
    
    # Main brain shape (modified ellipse with frontal and occipital bulges)
    # Frontal lobe bulge
    x = 1.2 * np.cos(t) + 0.3 * np.cos(2*t)
    y = 0.9 * np.sin(t) + 0.15 * np.sin(3*t)
    
    # Add some irregularity for organic look
    x += 0.08 * np.sin(5*t) + 0.05 * np.cos(7*t)
    y += 0.06 * np.cos(4*t) + 0.04 * np.sin(6*t)
    
    return x, y


def brain_surface_3d(n_points=500):
    """
    Generate 3D brain-like surface points.
    Two hemispheres with realistic proportions.
    """
    points = []
    
    # Generate points on brain-like ellipsoid
    for _ in range(n_points):
        # Spherical coordinates with brain proportions
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, np.pi)
        
        # Brain is wider (x), tall (z), and deep front-to-back (y)
        # Add asymmetry and lobes
        r_base = 1.0
        
        # Frontal lobe bulge (front)
        frontal = 0.15 * np.exp(-((phi - np.pi/2)**2) / 0.5) * np.exp(-((theta - np.pi)**2) / 1.0)
        
        # Occipital bulge (back)
        occipital = 0.1 * np.exp(-((phi - np.pi/2)**2) / 0.5) * np.exp(-((theta)**2) / 0.8)
        
        # Temporal lobes (sides, lower)
        temporal = 0.12 * np.exp(-((phi - 2*np.pi/3)**2) / 0.3) * (np.abs(np.sin(theta)))
        
        r = r_base + frontal + occipital + temporal
        
        # Convert to cartesian with brain proportions
        x = r * 1.3 * np.sin(phi) * np.cos(theta)  # Width (left-right)
        y = r * 1.1 * np.sin(phi) * np.sin(theta)  # Depth (front-back)  
        z = r * 0.95 * np.cos(phi)                  # Height (top-bottom)
        
        # Add slight noise for organic feel
        x += np.random.normal(0, 0.03)
        y += np.random.normal(0, 0.03)
        z += np.random.normal(0, 0.03)
        
        points.append((x, y, z))
    
    return np.array(points)


def place_nodes_in_brain_2d(n_nodes, seed=42):
    """Place network nodes inside brain outline."""
    np.random.seed(seed)
    
    brain_x, brain_y = brain_outline_2d()
    
    # Get bounding box
    x_min, x_max = brain_x.min(), brain_x.max()
    y_min, y_max = brain_y.min(), brain_y.max()
    
    positions = {}
    node_id = 0
    
    # Rejection sampling to place nodes inside brain
    while node_id < n_nodes:
        x = np.random.uniform(x_min * 0.9, x_max * 0.9)
        y = np.random.uniform(y_min * 0.9, y_max * 0.9)
        
        # Check if point is inside brain (approximate with ellipse + adjustments)
        # Simplified: use distance from center with angle-dependent radius
        angle = np.arctan2(y, x)
        idx = int((angle + np.pi) / (2 * np.pi) * len(brain_x)) % len(brain_x)
        r_boundary = np.sqrt(brain_x[idx]**2 + brain_y[idx]**2)
        r_point = np.sqrt(x**2 + y**2)
        
        if r_point < r_boundary * 0.92:  # Inside with margin
            positions[node_id] = (x, y)
            node_id += 1
    
    return positions


def place_nodes_in_brain_3d(n_nodes, seed=42):
    """Place network nodes on 3D brain surface."""
    np.random.seed(seed)
    points = brain_surface_3d(n_nodes)
    return {i: tuple(points[i]) for i in range(n_nodes)}


# =============================================================================
# NETWORK CREATION
# =============================================================================

def create_brain_network(n_nodes=250, k=6, p=0.1, seed=42):
    """Create small-world network with edge weights."""
    G = nx.watts_strogatz_graph(n_nodes, k, p, seed=seed)
    
    np.random.seed(seed)
    for u, v in G.edges():
        G[u][v]['weight'] = np.random.normal(1.0, 0.12)
        G[u][v]['original_weight'] = G[u][v]['weight']
    
    return G


def apply_quantum_bias(G, bias_fraction=0.15, bias_strength=0.08, seed=None):
    """Apply selective quantum bias."""
    if seed is not None:
        np.random.seed(seed)
    
    for u, v in G.edges():
        G[u][v]['weight'] = G[u][v]['original_weight']
    
    edge_list = list(G.edges())
    n_bias = max(1, int(len(edge_list) * bias_fraction))
    bias_indices = np.random.choice(len(edge_list), size=n_bias, replace=False)
    
    for idx in bias_indices:
        u, v = edge_list[idx]
        G[u][v]['weight'] += bias_strength


def simulate_cascade_steps(G, source, threshold=1.05, max_steps=50):
    """Simulate avalanche step by step."""
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


# =============================================================================
# 2D BRAIN WITH OUTLINE AND PULSE
# =============================================================================

def create_2d_brain_cascade_with_pulse(save_path='data/brain_2d_pulse.gif', fps=10, dpi=100):
    """
    2D brain visualization with:
    - Anatomical brain outline
    - Pulse effect on fresh activations
    """
    print("Creating 2D brain with pulse effect...")
    
    N_NODES = 300
    
    # Create networks
    G_classical = create_brain_network(N_NODES, seed=42)
    G_quantum = create_brain_network(N_NODES, seed=42)
    apply_quantum_bias(G_quantum, seed=123)
    
    # Place nodes inside brain shape
    pos = place_nodes_in_brain_2d(N_NODES, seed=42)
    nodes = list(G_classical.nodes())
    
    # Find seed node (center of brain)
    center_node = min(nodes, key=lambda n: pos[n][0]**2 + pos[n][1]**2)
    
    # Simulate cascades
    steps_c = simulate_cascade_steps(G_classical, center_node)
    steps_q = simulate_cascade_steps(G_quantum, center_node)
    
    max_steps = max(len(steps_c), len(steps_q))
    while len(steps_c) < max_steps:
        steps_c.append(set())
    while len(steps_q) < max_steps:
        steps_q.append(set())
    
    print(f"  Classical: {sum(len(s) for s in steps_c)} nodes")
    print(f"  Quantum: {sum(len(s) for s in steps_q)} nodes")
    
    # Build cumulative
    def build_cumulative(steps):
        cum = []
        activated = set()
        for step in steps:
            activated = activated | step
            cum.append(activated.copy())
        return cum
    
    cum_c = build_cumulative(steps_c)
    cum_q = build_cumulative(steps_q)
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.patch.set_facecolor('#0d1117')
    
    # Draw brain outline on both
    brain_x, brain_y = brain_outline_2d()
    
    for ax, title, color in [(ax1, 'CLASSICAL', '#4fc3f7'), (ax2, 'QUANTUM-BIASED', '#ff7043')]:
        ax.set_facecolor('#0d1117')
        ax.fill(brain_x, brain_y, facecolor='#1a1a2e', edgecolor='#3a3a5e', linewidth=2, alpha=0.8)
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.4, 1.4)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', color=color, pad=15)
    
    # Draw faint edges
    node_positions = np.array([pos[n] for n in nodes])
    for u, v in G_classical.edges():
        for ax in [ax1, ax2]:
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 
                   color='#2a2a4a', alpha=0.15, linewidth=0.3, zorder=1)
    
    # Initialize scatter plots
    scatter1 = ax1.scatter([], [], s=[], c=[], zorder=5)
    scatter2 = ax2.scatter([], [], s=[], c=[], zorder=5)
    
    # Pulse rings (for glow effect)
    pulse_artists1 = []
    pulse_artists2 = []
    
    count1 = ax1.text(0.02, 0.98, '', transform=ax1.transAxes, fontsize=12,
                      color='#4fc3f7', va='top', fontweight='bold')
    count2 = ax2.text(0.02, 0.98, '', transform=ax2.transAxes, fontsize=12,
                      color='#ff7043', va='top', fontweight='bold')
    time_text = fig.text(0.5, 0.02, '', ha='center', fontsize=12, color='white')
    
    def animate(frame):
        nonlocal pulse_artists1, pulse_artists2
        
        # Clear old pulse rings
        for artist in pulse_artists1 + pulse_artists2:
            artist.remove()
        pulse_artists1 = []
        pulse_artists2 = []
        
        pause = 10
        if frame < pause:
            step_idx = 0
        else:
            step_idx = min(frame - pause, max_steps - 1)
        
        # Get states
        cum_c_now = cum_c[step_idx] if step_idx < len(cum_c) else cum_c[-1]
        cum_q_now = cum_q[step_idx] if step_idx < len(cum_q) else cum_q[-1]
        fresh_c = steps_c[step_idx] if step_idx < len(steps_c) else set()
        fresh_q = steps_q[step_idx] if step_idx < len(steps_q) else set()
        
        # Build colors and sizes with PULSE effect
        def get_visuals(cum_set, fresh_set, base_color):
            colors = []
            sizes = []
            for node in nodes:
                if node == center_node:
                    colors.append('#00ff00')
                    sizes.append(120)
                elif node in fresh_set:
                    colors.append('#ffffff')  # Bright white for fresh
                    sizes.append(100)  # Larger
                elif node in cum_set:
                    colors.append(base_color)
                    sizes.append(50)
                else:
                    colors.append('#2a2a3a')
                    sizes.append(20)
            return colors, sizes
        
        colors1, sizes1 = get_visuals(cum_c_now, fresh_c, '#4fc3f7')
        colors2, sizes2 = get_visuals(cum_q_now, fresh_q, '#ff7043')
        
        # Update scatters
        scatter1.set_offsets(node_positions)
        scatter1.set_color(colors1)
        scatter1.set_sizes(sizes1)
        
        scatter2.set_offsets(node_positions)
        scatter2.set_color(colors2)
        scatter2.set_sizes(sizes2)
        
        # Add pulse rings around fresh nodes
        for node in fresh_c:
            x, y = pos[node]
            circle = plt.Circle((x, y), 0.08, fill=False, color='#4fc3f7', 
                               linewidth=2, alpha=0.7, zorder=4)
            ax1.add_patch(circle)
            pulse_artists1.append(circle)
        
        for node in fresh_q:
            x, y = pos[node]
            circle = plt.Circle((x, y), 0.08, fill=False, color='#ff7043',
                               linewidth=2, alpha=0.7, zorder=4)
            ax2.add_patch(circle)
            pulse_artists2.append(circle)
        
        count1.set_text(f'Active: {len(cum_c_now)}')
        count2.set_text(f'Active: {len(cum_q_now)}')
        
        if frame < pause:
            time_text.set_text('Initiating cascade from seed node...')
        else:
            time_text.set_text(f'Time Step: {step_idx + 1}')
        
        return [scatter1, scatter2, count1, count2, time_text] + pulse_artists1 + pulse_artists2
    
    total_frames = 10 + max_steps + 25
    print(f"  Creating {total_frames} frames...")
    
    anim = FuncAnimation(fig, animate, frames=total_frames, interval=1000//fps, blit=False)
    
    os.makedirs('data', exist_ok=True)
    writer = PillowWriter(fps=fps)
    anim.save(save_path, writer=writer, dpi=dpi)
    print(f"  [OK] Saved: {save_path}")
    plt.close()


# =============================================================================
# 3D ROTATING BRAIN
# =============================================================================

def create_3d_brain_cascade(save_path='data/brain_3d_rotate.gif', fps=12, dpi=80):
    """
    3D brain with rotating view during cascade.
    Uses frame-by-frame rendering to avoid matplotlib 3D scatter animation issues.
    """
    print("\nCreating 3D rotating brain...")
    
    N_NODES = 200
    
    G = create_brain_network(N_NODES, seed=42)
    apply_quantum_bias(G, seed=123)
    
    # 3D positions
    pos = place_nodes_in_brain_3d(N_NODES, seed=42)
    nodes = list(G.nodes())
    
    # Find center node
    center_node = min(nodes, key=lambda n: sum(x**2 for x in pos[n]))
    
    steps = simulate_cascade_steps(G, center_node)
    max_steps = len(steps)
    
    print(f"  {sum(len(s) for s in steps)} nodes in {max_steps} steps")
    
    # Build cumulative
    cum = []
    activated = set()
    for step in steps:
        activated = activated | step
        cum.append(activated.copy())
    
    node_coords = np.array([pos[n] for n in nodes])
    
    # Pre-compute edge data
    edge_data = []
    for u, v in G.edges():
        edge_data.append(([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], [pos[u][2], pos[v][2]]))
    
    pause = 15
    total_frames = pause + max_steps + 60
    print(f"  Creating {total_frames} frames...")
    
    # Generate frames manually
    frames = []
    
    for frame in range(total_frames):
        if frame % 10 == 0:
            print(f"    Frame {frame}/{total_frames}...")
        
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        fig.patch.set_facecolor('#0d1117')
        ax.set_facecolor('#0d1117')
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('#0d1117')
        ax.yaxis.pane.set_edgecolor('#0d1117')
        ax.zaxis.pane.set_edgecolor('#0d1117')
        
        # Rotation
        ax.view_init(elev=20, azim=frame * 3)
        
        # Draw edges
        for xs, ys, zs in edge_data:
            ax.plot(xs, ys, zs, color='#3a3a5a', alpha=0.08, linewidth=0.3)
        
        # Get state
        if frame < pause:
            step_idx = 0
        else:
            step_idx = min(frame - pause, max_steps - 1)
        
        cum_now = cum[step_idx] if step_idx < len(cum) else cum[-1]
        fresh = steps[step_idx] if step_idx < len(steps) else set()
        
        # Draw nodes by category (to handle sizes properly)
        inactive_idx = [i for i, n in enumerate(nodes) if n not in cum_now and n != center_node]
        active_idx = [i for i, n in enumerate(nodes) if n in cum_now and n not in fresh and n != center_node]
        fresh_idx = [i for i, n in enumerate(nodes) if n in fresh]
        center_idx = [i for i, n in enumerate(nodes) if n == center_node]
        
        if inactive_idx:
            ax.scatter(node_coords[inactive_idx, 0], node_coords[inactive_idx, 1], 
                      node_coords[inactive_idx, 2], c='#2a2a4a', s=20, alpha=0.5)
        if active_idx:
            ax.scatter(node_coords[active_idx, 0], node_coords[active_idx, 1],
                      node_coords[active_idx, 2], c='#ff7043', s=50, alpha=0.9)
        if fresh_idx:
            ax.scatter(node_coords[fresh_idx, 0], node_coords[fresh_idx, 1],
                      node_coords[fresh_idx, 2], c='#ffffff', s=100, alpha=1.0)
        if center_idx:
            ax.scatter(node_coords[center_idx, 0], node_coords[center_idx, 1],
                      node_coords[center_idx, 2], c='#00ff00', s=150, alpha=1.0)
        
        ax.set_title(f'QUANTUM CASCADE - {len(cum_now)} nodes active',
                    fontsize=14, fontweight='bold', color='#ff7043', pad=20)
        
        # Save frame to buffer using BytesIO
        from io import BytesIO
        from PIL import Image
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=dpi, facecolor=fig.get_facecolor(), 
                   bbox_inches='tight', pad_inches=0.1)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        frames.append(img.copy())
        buf.close()
        plt.close(fig)
    
    # Save as GIF
    from PIL import Image
    frames[0].save(save_path, save_all=True, append_images=frames[1:], 
                   duration=1000//fps, loop=0, optimize=True)
    
    print(f"  [OK] Saved: {save_path}")
    plt.close('all')


# =============================================================================
# MASTER SUMMARY FIGURE
# =============================================================================

def create_master_summary(save_path='data/master_summary.png', dpi=150):
    """
    Single figure telling the whole story:
    - OR timescale graph
    - Key statistics
    - Brain cascade comparison
    """
    print("\nCreating master summary figure...")
    
    fig = plt.figure(figsize=(20, 12))
    fig.patch.set_facecolor('#0d1117')
    
    # Grid layout
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3,
                          left=0.05, right=0.95, top=0.92, bottom=0.08)
    
    # ===================
    # Panel 1: OR Timescales (top left)
    # ===================
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#1a1a2e')
    
    # OR collapse calculation
    hbar = 1.0545718e-34
    G_const = 6.67430e-11
    m = 1e-22
    d = 1e-11
    
    N_range = np.logspace(0, 12, 100)
    tau_range = hbar / (N_range * G_const * m**2 / d)
    
    ax1.loglog(N_range, tau_range, color='#4fc3f7', linewidth=2.5, label='OR Collapse Time')
    ax1.axhline(y=0.1, color='#ff7043', linestyle='--', linewidth=2, label='~100 ms (gamma)')
    ax1.axhline(y=0.5, color='#ffd54f', linestyle='--', linewidth=2, label='~500 ms (decision)')
    ax1.axvline(x=1e10, color='#81c784', linestyle='--', linewidth=2, label='Brain-scale (~10^10)')
    
    ax1.fill_between([1e9, 1e11], [0.01, 0.01], [1, 1], alpha=0.2, color='#81c784')
    
    ax1.set_xlabel('Tubulin Ensemble Size N', fontsize=10, color='white')
    ax1.set_ylabel('Collapse Time (s)', fontsize=10, color='white')
    ax1.set_title('OR TIMESCALES HIT NEURAL WINDOW', fontsize=12, fontweight='bold', color='#4fc3f7')
    ax1.legend(fontsize=8, loc='upper right', facecolor='#1a1a2e', edgecolor='#3a3a5e', labelcolor='white')
    ax1.tick_params(colors='white')
    ax1.grid(True, alpha=0.2)
    for spine in ax1.spines.values():
        spine.set_color('#3a3a5e')
    
    # ===================
    # Panel 2: Key Stats (top middle)
    # ===================
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#1a1a2e')
    ax2.axis('off')
    
    stats_text = """
    KEY FINDINGS
    
    1. OR TIMESCALE MATCH
       10^10 tubulins -> tau = 0.16s
       Matches gamma rhythm (100ms)
    
    2. SELECTIVE BIAS != UNIFORM NOISE
       Mimic vs Quantum skewness
       p = 0.014 (SIGNIFICANT)
    
    3. BIDIRECTIONAL CONTROL
       Quantum(+) amplifies
       Quantum(-) vetoes
       p = 0.0001 (HIGHLY SIGNIFICANT)
    
    4. XENON ISOTOPE EVIDENCE
       Nuclear spin affects anesthesia
       ~20% potency difference
       Same chemistry, different quantum
    """
    
    ax2.text(0.05, 0.95, stats_text, transform=ax2.transAxes, fontsize=11,
             verticalalignment='top', fontfamily='monospace', color='white',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a4a', edgecolor='#4a4a6a'))
    ax2.set_title('SIMULATION RESULTS', fontsize=12, fontweight='bold', color='#81c784')
    
    # ===================
    # Panel 3: Mechanism Diagram (top right)
    # ===================
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor('#1a1a2e')
    ax3.axis('off')
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    
    # Draw mechanism flow
    boxes = [
        (5, 8.5, 'THERMODYNAMIC SUBSTRATE\n(Brain at criticality)', '#4fc3f7'),
        (5, 6.5, 'QUANTUM TRIGGER\n(OR in microtubules)', '#ff7043'),
        (5, 4.5, 'SELECTIVE BIAS\n(Nudge specific edges)', '#ffd54f'),
        (5, 2.5, 'AVALANCHE AMPLIFICATION\n(Microscopic -> Macroscopic)', '#81c784'),
        (5, 0.5, 'BEHAVIOR / DECISION', '#e1bee7'),
    ]
    
    for x, y, text, color in boxes:
        rect = plt.Rectangle((x-2.3, y-0.6), 4.6, 1.2, facecolor='#2a2a4a',
                             edgecolor=color, linewidth=2, zorder=2)
        ax3.add_patch(rect)
        ax3.text(x, y, text, ha='center', va='center', fontsize=9, 
                fontweight='bold', color=color, zorder=3)
    
    # Arrows
    for i in range(len(boxes)-1):
        ax3.annotate('', xy=(5, boxes[i+1][1]+0.7), xytext=(5, boxes[i][1]-0.7),
                    arrowprops=dict(arrowstyle='->', color='white', lw=2))
    
    ax3.set_title('THE MECHANISM', fontsize=12, fontweight='bold', color='#ff7043')
    
    # ===================
    # Panel 4 & 5: Brain Cascades (bottom left and middle)
    # ===================
    N_NODES = 200
    G_c = create_brain_network(N_NODES, seed=42)
    G_q = create_brain_network(N_NODES, seed=42)
    apply_quantum_bias(G_q, seed=123)
    
    pos = place_nodes_in_brain_2d(N_NODES, seed=42)
    nodes = list(G_c.nodes())
    center_node = min(nodes, key=lambda n: pos[n][0]**2 + pos[n][1]**2)
    
    steps_c = simulate_cascade_steps(G_c, center_node)
    steps_q = simulate_cascade_steps(G_q, center_node)
    
    final_c = set().union(*steps_c)
    final_q = set().union(*steps_q)
    
    brain_x, brain_y = brain_outline_2d()
    node_positions = np.array([pos[n] for n in nodes])
    
    for ax_idx, (ax_pos, final_set, title, color) in enumerate([
        (gs[1, 0], final_c, f'CLASSICAL\n{len(final_c)} nodes', '#4fc3f7'),
        (gs[1, 1], final_q, f'QUANTUM-BIASED\n{len(final_q)} nodes', '#ff7043')
    ]):
        ax = fig.add_subplot(ax_pos)
        ax.set_facecolor('#0d1117')
        ax.fill(brain_x, brain_y, facecolor='#1a1a2e', edgecolor='#3a3a5e', linewidth=1.5)
        
        # Draw edges
        for u, v in G_c.edges():
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                   color='#2a2a4a', alpha=0.1, linewidth=0.3)
        
        # Draw nodes
        colors = []
        sizes = []
        for node in nodes:
            if node == center_node:
                colors.append('#00ff00')
                sizes.append(80)
            elif node in final_set:
                colors.append(color)
                sizes.append(40)
            else:
                colors.append('#2a2a3a')
                sizes.append(15)
        
        ax.scatter(node_positions[:, 0], node_positions[:, 1], c=colors, s=sizes, zorder=5)
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=12, fontweight='bold', color=color)
    
    # ===================
    # Panel 6: Conclusion (bottom right)
    # ===================
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_facecolor('#1a1a2e')
    ax6.axis('off')
    
    conclusion = """
    THE ARGUMENT

    1. AI scales intelligence
       but NOT agency

    2. Nature shows the same:
       4 billion years, one clear
       example of goal-revision (us)

    3. Quantum mechanics provides
       the selection gap

    4. Thermodynamic amplification
       makes it biologically viable

    5. Simulations confirm:
       selective bias != thermal noise
       bidirectional control works


    Free will is not free.
    But it might be real.
    """
    
    ax6.text(0.05, 0.95, conclusion, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace', color='white',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a4a', edgecolor='#4a4a6a'))
    ax6.set_title('CONCLUSION', fontsize=12, fontweight='bold', color='#e1bee7')
    
    # Main title
    fig.suptitle('QUANTUM CONSCIOUSNESS: The Computational Evidence',
                 fontsize=20, fontweight='bold', color='white', y=0.97)
    
    os.makedirs('data', exist_ok=True)
    plt.savefig(save_path, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches='tight')
    print(f"  [OK] Saved: {save_path}")
    plt.close()


# =============================================================================
# STATIC BRAIN COMPARISON (HIGH QUALITY)
# =============================================================================

def create_brain_comparison_hq(save_path='data/brain_comparison_hq.png', dpi=200):
    """High quality brain comparison for video thumbnails."""
    print("\nCreating high-quality brain comparison...")
    
    N_NODES = 400
    G_c = create_brain_network(N_NODES, seed=42)
    G_q = create_brain_network(N_NODES, seed=42)
    apply_quantum_bias(G_q, bias_fraction=0.15, bias_strength=0.08, seed=123)
    
    pos = place_nodes_in_brain_2d(N_NODES, seed=42)
    nodes = list(G_c.nodes())
    center_node = min(nodes, key=lambda n: pos[n][0]**2 + pos[n][1]**2)
    
    steps_c = simulate_cascade_steps(G_c, center_node)
    steps_q = simulate_cascade_steps(G_q, center_node)
    
    final_c = set().union(*steps_c)
    final_q = set().union(*steps_q)
    
    print(f"  Classical: {len(final_c)} nodes")
    print(f"  Quantum: {len(final_q)} nodes")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))
    fig.patch.set_facecolor('#0d1117')
    
    brain_x, brain_y = brain_outline_2d()
    node_positions = np.array([pos[n] for n in nodes])
    
    for ax, final_set, title, color, subtitle in [
        (ax1, final_c, 'CLASSICAL', '#4fc3f7', f'{len(final_c)} neurons activated'),
        (ax2, final_q, 'QUANTUM-BIASED', '#ff7043', f'{len(final_q)} neurons activated')
    ]:
        ax.set_facecolor('#0d1117')
        
        # Brain outline with glow effect
        for lw, alpha in [(8, 0.1), (4, 0.2), (2, 0.5)]:
            ax.plot(brain_x, brain_y, color=color, linewidth=lw, alpha=alpha)
        ax.fill(brain_x, brain_y, facecolor='#1a1a2e', edgecolor=color, linewidth=1.5, alpha=0.9)
        
        # Edges
        for u, v in G_c.edges():
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                   color='#2a2a4a', alpha=0.08, linewidth=0.2)
        
        # Nodes
        colors = []
        sizes = []
        for node in nodes:
            if node == center_node:
                colors.append('#00ff00')
                sizes.append(120)
            elif node in final_set:
                colors.append(color)
                sizes.append(45)
            else:
                colors.append('#1a1a2a')
                sizes.append(12)
        
        ax.scatter(node_positions[:, 0], node_positions[:, 1], c=colors, s=sizes, 
                  zorder=5, alpha=0.9, edgecolors='none')
        
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.4, 1.4)
        ax.set_aspect('equal')
        ax.axis('off')
        
        ax.text(0.5, 1.05, title, transform=ax.transAxes, fontsize=24, 
               fontweight='bold', color=color, ha='center')
        ax.text(0.5, -0.05, subtitle, transform=ax.transAxes, fontsize=14,
               color='white', ha='center', alpha=0.8)
    
    fig.suptitle('SAME SEED, DIFFERENT OUTCOMES',
                 fontsize=28, fontweight='bold', color='white', y=0.98)
    
    fig.text(0.5, 0.02, 'Quantum bias recruits more neurons through selective edge strengthening',
            ha='center', fontsize=12, color='#888888')
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.93])
    plt.savefig(save_path, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches='tight')
    print(f"  [OK] Saved: {save_path}")
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ENHANCED BRAIN VISUALIZATIONS")
    print("=" * 60)
    print()
    
    # Static images first (fast)
    create_master_summary('data/master_summary.png')
    create_brain_comparison_hq('data/brain_comparison_hq.png')
    
    # Animations (slower)
    create_2d_brain_cascade_with_pulse('data/brain_2d_pulse.gif', fps=10)
    create_3d_brain_cascade('data/brain_3d_rotate.gif', fps=10)
    
    print("\n" + "=" * 60)
    print("ALL VISUALIZATIONS COMPLETE")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - data/master_summary.png (single image, whole story)")
    print("  - data/brain_comparison_hq.png (high-quality comparison)")
    print("  - data/brain_2d_pulse.gif (2D with pulse effect)")
    print("  - data/brain_3d_rotate.gif (3D rotating brain)")
