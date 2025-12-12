"""
ANIMATED Quantum Simulation - Actually shows the physics!

This creates real animations showing:
1. Quantum state evolution (probability waves)
2. Wavefunction collapse in action
3. Quantum Zeno Effect - how measurement "freezes" evolution
4. The "selection" moment where determinism breaks

Requirements:
    pip install matplotlib numpy
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, FancyArrowPatch
import matplotlib.gridspec as gridspec

# ============================================================================
# SIMULATION 1: Quantum State Evolution & Collapse
# ============================================================================

def run_collapse_simulation():
    """
    Shows a quantum superposition evolving, then COLLAPSING to one state.
    This visualizes the "gap" - before collapse, both outcomes exist.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('QUANTUM SUPERPOSITION → COLLAPSE', fontsize=16, fontweight='bold')
    
    # Parameters
    x = np.linspace(-5, 5, 500)
    frames = 150
    collapse_frame = 100
    
    # Two Gaussian states (representing |0⟩ and |1⟩ possibilities)
    def psi_0(x, t):
        # State centered at -2, oscillating
        center = -2 + 0.3 * np.sin(t * 0.1)
        return np.exp(-(x - center)**2) * np.cos(t * 0.2)
    
    def psi_1(x, t):
        # State centered at +2, oscillating
        center = 2 + 0.3 * np.sin(t * 0.1 + np.pi)
        return np.exp(-(x - center)**2) * np.cos(t * 0.2 + np.pi/4)
    
    # Initialize plots
    ax1, ax2, ax3 = axes
    
    # Left: Probability amplitudes
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_xlabel('Position')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Wavefunction Amplitudes')
    line0, = ax1.plot([], [], 'b-', lw=2, label='|possibility A⟩')
    line1, = ax1.plot([], [], 'r-', lw=2, label='|possibility B⟩')
    ax1.legend(loc='upper right')
    ax1.axhline(0, color='gray', lw=0.5)
    
    # Middle: Total probability (what we'd measure)
    ax2.set_xlim(-5, 5)
    ax2.set_ylim(0, 2)
    ax2.set_xlabel('Position')
    ax2.set_ylabel('Probability')
    ax2.set_title('Measurement Probability |ψ|²')
    prob_line, = ax2.plot([], [], 'purple', lw=2)
    prob_fill = None
    
    # Right: State indicator
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')
    ax3.set_title('System State')
    state_text = ax3.text(5, 5, '', fontsize=14, ha='center', va='center',
                          bbox=dict(boxstyle='round', facecolor='wheat'))
    time_text = ax3.text(5, 8, '', fontsize=12, ha='center')
    
    # Store collapse outcome (randomly chosen at collapse_frame)
    collapse_outcome = [None]
    
    def init():
        line0.set_data([], [])
        line1.set_data([], [])
        prob_line.set_data([], [])
        state_text.set_text('')
        time_text.set_text('')
        return line0, line1, prob_line, state_text, time_text
    
    def animate(frame):
        nonlocal prob_fill
        
        t = frame * 0.5
        
        if frame < collapse_frame:
            # SUPERPOSITION PHASE - both states exist
            y0 = psi_0(x, t)
            y1 = psi_1(x, t)
            
            # Superposition amplitude
            amp_0 = np.cos(t * 0.05) * 0.7 + 0.5
            amp_1 = np.sin(t * 0.05) * 0.7 + 0.5
            
            line0.set_data(x, y0 * amp_0)
            line1.set_data(x, y1 * amp_1)
            
            # Total probability
            psi_total = y0 * amp_0 + y1 * amp_1
            prob = np.abs(psi_total)**2
            prob_line.set_data(x, prob)
            
            # Update probability fill
            if prob_fill is not None:
                prob_fill.remove()
            prob_fill = ax2.fill_between(x, prob, alpha=0.3, color='purple')
            
            state_text.set_text('SUPERPOSITION\n\nBoth outcomes\ncoexist')
            state_text.set_bbox(dict(boxstyle='round', facecolor='#fff9c4', edgecolor='orange'))
            time_text.set_text(f'Before collapse: t = {frame}')
            
        elif frame == collapse_frame:
            # COLLAPSE MOMENT - randomly choose outcome
            collapse_outcome[0] = np.random.choice(['A', 'B'])
            
        else:
            # POST-COLLAPSE - only one state remains
            decay = np.exp(-(frame - collapse_frame) * 0.1)
            
            if collapse_outcome[0] == 'A':
                y0 = psi_0(x, t)
                line0.set_data(x, y0)
                line1.set_data(x, psi_1(x, t) * decay)
                prob = np.abs(y0)**2
                state_text.set_text('COLLAPSED → A\n\n"Selection" made!\nOne outcome real')
                state_text.set_bbox(dict(boxstyle='round', facecolor='#c8e6c9', edgecolor='green'))
            else:
                y1 = psi_1(x, t)
                line0.set_data(x, psi_0(x, t) * decay)
                line1.set_data(x, y1)
                prob = np.abs(y1)**2
                state_text.set_text('COLLAPSED → B\n\n"Selection" made!\nOne outcome real')
                state_text.set_bbox(dict(boxstyle='round', facecolor='#c8e6c9', edgecolor='green'))
            
            prob_line.set_data(x, prob)
            if prob_fill is not None:
                prob_fill.remove()
            prob_fill = ax2.fill_between(x, prob, alpha=0.3, color='green')
            
            time_text.set_text(f'After collapse: t = {frame}\n\nTHIS is where physics\ndoesn\'t determine outcome')
        
        return line0, line1, prob_line, state_text, time_text
    
    anim = FuncAnimation(fig, animate, init_func=init, frames=frames, 
                         interval=50, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()
    return anim


# ============================================================================
# SIMULATION 2: Quantum Zeno Effect - Measurement Freezes Evolution
# ============================================================================

def run_zeno_simulation():
    """
    Shows how measurement frequency affects quantum evolution.
    More measurements = state stays frozen (the "veto" mechanism)
    """
    fig = plt.figure(figsize=(14, 8))
    gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1])
    
    ax_no_meas = fig.add_subplot(gs[0, 0])
    ax_meas = fig.add_subplot(gs[0, 1])
    ax_prob = fig.add_subplot(gs[1, :])
    
    fig.suptitle('QUANTUM ZENO EFFECT: How "Attention" Could Freeze States', 
                 fontsize=16, fontweight='bold')
    
    # Parameters
    T_total = 100  # Total time
    omega = 0.1    # Natural oscillation frequency
    
    # Initialize state: |ψ⟩ = |0⟩ (initial state we want to maintain)
    # Without measurement, evolves to |1⟩
    
    ax_no_meas.set_title('WITHOUT Frequent Measurement\n(State evolves freely)', fontsize=12)
    ax_no_meas.set_xlim(0, T_total)
    ax_no_meas.set_ylim(-0.1, 1.1)
    ax_no_meas.set_xlabel('Time')
    ax_no_meas.set_ylabel('P(|0⟩) - Probability of initial state')
    
    ax_meas.set_title('WITH Frequent Measurement\n(State "frozen" by observation)', fontsize=12)
    ax_meas.set_xlim(0, T_total)
    ax_meas.set_ylim(-0.1, 1.1)
    ax_meas.set_xlabel('Time')
    ax_meas.set_ylabel('P(|0⟩) - Probability of initial state')
    
    ax_prob.set_title('Comparison: Final probability of staying in initial state', fontsize=12)
    ax_prob.set_xlabel('Number of measurements')
    ax_prob.set_ylabel('Survival probability')
    
    # Lines
    line_no_meas, = ax_no_meas.plot([], [], 'r-', lw=2)
    line_meas, = ax_meas.plot([], [], 'g-', lw=2)
    scatter_meas = ax_meas.scatter([], [], c='blue', s=50, zorder=5, label='Measurement')
    
    # Pre-calculate the comparison data
    n_measurements_list = [1, 2, 5, 10, 20, 50, 100]
    survival_probs = []
    for n in n_measurements_list:
        dt = T_total / n
        # Survival probability with n measurements: P = cos^2(ωdt/2)^n
        p = (np.cos(omega * dt / 2)**2) ** n
        survival_probs.append(p)
    
    bar_container = ax_prob.bar(range(len(n_measurements_list)), [0]*len(n_measurements_list),
                                 tick_label=[str(n) for n in n_measurements_list],
                                 color='steelblue', alpha=0.7)
    ax_prob.set_ylim(0, 1.1)
    ax_prob.axhline(1.0, color='green', linestyle='--', alpha=0.5, label='Perfect freezing')
    ax_prob.legend()
    
    # State indicators
    state_no = ax_no_meas.text(T_total/2, 0.5, '', fontsize=11, ha='center',
                               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    state_yes = ax_meas.text(T_total/2, 0.5, '', fontsize=11, ha='center',
                              bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    n_measurements = 20  # Number of measurements in the "with measurement" case
    measurement_times = np.linspace(0, T_total, n_measurements + 1)[1:]
    
    def animate(frame):
        t_current = frame
        
        # WITHOUT measurement: smooth oscillation
        t_range = np.linspace(0, t_current, max(2, t_current))
        p_no_meas = np.cos(omega * t_range / 2)**2
        line_no_meas.set_data(t_range, p_no_meas)
        
        # WITH measurement: step function with resets
        t_meas = []
        p_meas = []
        current_p = 1.0
        last_t = 0
        
        for m_time in measurement_times:
            if m_time > t_current:
                break
            # Evolution from last measurement to this one
            dt = m_time - last_t
            t_segment = np.linspace(last_t, m_time, 20)
            p_segment = current_p * np.cos(omega * (t_segment - last_t) / 2)**2
            t_meas.extend(t_segment)
            p_meas.extend(p_segment)
            # Measurement "resets" - probability of staying in |0⟩
            current_p = p_segment[-1]
            if np.random.random() < current_p:
                current_p = 1.0  # Measured in |0⟩, reset
            else:
                current_p = 0.0  # Measured in |1⟩, failed
                break
            last_t = m_time
        
        # Continue to current time if not collapsed
        if current_p > 0 and last_t < t_current:
            t_segment = np.linspace(last_t, t_current, 20)
            p_segment = current_p * np.cos(omega * (t_segment - last_t) / 2)**2
            t_meas.extend(t_segment)
            p_meas.extend(p_segment)
        
        line_meas.set_data(t_meas, p_meas)
        
        # Show measurement points
        meas_done = measurement_times[measurement_times <= t_current]
        scatter_meas.set_offsets(np.column_stack([meas_done, np.ones_like(meas_done) * 0.95]) if len(meas_done) > 0 else np.empty((0, 2)))
        
        # Update state text
        if t_current > 0:
            p_final_no = np.cos(omega * t_current / 2)**2
            state_no.set_text(f'P(|0⟩) = {p_final_no:.2f}')
            if len(p_meas) > 0:
                state_yes.set_text(f'P(|0⟩) = {p_meas[-1]:.2f}')
        
        # Update bar chart progressively
        progress = min(1.0, t_current / T_total)
        for i, (bar, final_prob) in enumerate(zip(bar_container, survival_probs)):
            bar.set_height(final_prob * progress)
        
        return line_no_meas, line_meas, scatter_meas, state_no, state_yes
    
    anim = FuncAnimation(fig, animate, frames=range(1, T_total + 1),
                         interval=50, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()
    return anim


# ============================================================================
# SIMULATION 3: Bloch Sphere - Quantum State Visualization
# ============================================================================

def run_bloch_simulation():
    """
    Shows quantum state on a Bloch sphere - the standard visualization.
    Superposition = point on sphere surface
    Collapse = jumping to north or south pole
    """
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122)
    
    fig.suptitle('QUANTUM STATE ON BLOCH SPHERE', fontsize=16, fontweight='bold')
    
    # Draw Bloch sphere
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax1.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1, color='blue')
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_zlim(-1.5, 1.5)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Bloch Sphere\n|0⟩ = North Pole, |1⟩ = South Pole')
    
    # Mark poles
    ax1.scatter([0], [0], [1], color='green', s=100, label='|0⟩')
    ax1.scatter([0], [0], [-1], color='red', s=100, label='|1⟩')
    ax1.legend()
    
    # State vector
    state_point, = ax1.plot([0], [0], [1], 'o', color='purple', markersize=15)
    state_line, = ax1.plot([0, 0], [0, 0], [0, 1], '-', color='purple', lw=2)
    
    # Right panel: probabilities
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 1.1)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Probability')
    ax2.set_title('Measurement Probabilities')
    
    prob0_line, = ax2.plot([], [], 'g-', lw=2, label='P(|0⟩)')
    prob1_line, = ax2.plot([], [], 'r-', lw=2, label='P(|1⟩)')
    ax2.legend()
    ax2.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
    
    time_data = []
    prob0_data = []
    prob1_data = []
    
    collapse_frame = 150
    collapsed = [False]
    collapse_state = [None]
    
    def animate(frame):
        t = frame * 0.02
        
        if frame < collapse_frame:
            # Evolving superposition - state precesses around sphere
            theta = np.pi/2 + 0.4 * np.sin(t * 2)  # Polar angle
            phi = t * 3  # Azimuthal angle (precession)
            
            x = np.sin(theta) * np.cos(phi)
            y = np.sin(theta) * np.sin(phi)
            z = np.cos(theta)
            
            state_point.set_data([x], [y])
            state_point.set_3d_properties([z])
            state_line.set_data([0, x], [0, y])
            state_line.set_3d_properties([0, z])
            
            # Probabilities
            p0 = (1 + z) / 2  # |⟨0|ψ⟩|²
            p1 = (1 - z) / 2  # |⟨1|ψ⟩|²
            
            ax1.set_title(f'SUPERPOSITION\nθ={theta:.2f}, φ={phi:.2f}')
            
        elif frame == collapse_frame:
            # Collapse!
            collapsed[0] = True
            # Random collapse based on current probabilities
            theta = np.pi/2 + 0.4 * np.sin(t * 2)
            z = np.cos(theta)
            p0 = (1 + z) / 2
            collapse_state[0] = '0' if np.random.random() < p0 else '1'
            
        else:
            # Post-collapse - fixed at pole
            if collapse_state[0] == '0':
                x, y, z = 0, 0, 1
                p0, p1 = 1.0, 0.0
                ax1.set_title('COLLAPSED TO |0⟩\n\nOutcome determined!')
            else:
                x, y, z = 0, 0, -1
                p0, p1 = 0.0, 1.0
                ax1.set_title('COLLAPSED TO |1⟩\n\nOutcome determined!')
            
            state_point.set_data([x], [y])
            state_point.set_3d_properties([z])
            state_line.set_data([0, x], [0, y])
            state_line.set_3d_properties([0, z])
        
        # Update probability plot
        if frame < collapse_frame:
            theta = np.pi/2 + 0.4 * np.sin(t * 2)
            z = np.cos(theta)
            p0 = (1 + z) / 2
            p1 = (1 - z) / 2
        
        time_data.append(t)
        prob0_data.append(p0)
        prob1_data.append(p1)
        
        # Keep only recent data for scrolling effect
        if len(time_data) > 200:
            time_data.pop(0)
            prob0_data.pop(0)
            prob1_data.pop(0)
        
        prob0_line.set_data(time_data, prob0_data)
        prob1_line.set_data(time_data, prob1_data)
        
        if len(time_data) > 1:
            ax2.set_xlim(time_data[0], time_data[-1] + 0.5)
        
        return state_point, state_line, prob0_line, prob1_line
    
    anim = FuncAnimation(fig, animate, frames=200, interval=50, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()
    return anim


# ============================================================================
# MAIN MENU
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("QUANTUM CONSCIOUSNESS SIMULATIONS")
    print("=" * 60)
    print("\nChoose a simulation to run:\n")
    print("  1. Wavefunction Collapse   - See superposition → collapse")
    print("  2. Quantum Zeno Effect     - See how measurement 'freezes' states")
    print("  3. Bloch Sphere           - See quantum state evolution in 3D")
    print("  q. Quit")
    print("\n" + "=" * 60)
    
    while True:
        choice = input("\nEnter choice (1/2/3/q): ").strip().lower()
        
        if choice == '1':
            print("\nRunning Collapse Simulation...")
            print("Watch: Both possibilities exist, then ONE is selected!")
            print("(Close window to return to menu)\n")
            run_collapse_simulation()
            
        elif choice == '2':
            print("\nRunning Quantum Zeno Simulation...")
            print("Watch: More measurements = state stays 'frozen'!")
            print("This is the proposed 'veto' mechanism.")
            print("(Close window to return to menu)\n")
            run_zeno_simulation()
            
        elif choice == '3':
            print("\nRunning Bloch Sphere Simulation...")
            print("Watch: State precesses on sphere, then collapses to a pole!")
            print("(Close window to return to menu)\n")
            run_bloch_simulation()
            
        elif choice == 'q':
            print("\nGoodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, 3, or q.")
