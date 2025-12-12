"""
Quantum Consciousness Visualization for Video
==============================================

Clear, educational visualizations showing:
1. The "gap" in determinism where free will could operate
2. How Quantum Zeno Effect could enable "veto"
3. The key insight: physics determines possibilities, not outcomes

NOTE: This uses CONCEPTUAL values from Orch-OR literature, not derived calculations.
The actual physics is complex - this is for educational visualization.

Requirements:
    pip install matplotlib numpy
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Set style
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'


def create_gap_visualization():
    """
    THE MAIN INSIGHT: Show "The Gap in Determinism"
    
    This is the key concept - physics determines what CAN happen,
    but NOT which outcome DOES happen.
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'THE GAP IN DETERMINISM', 
            fontsize=24, fontweight='bold', ha='center',
            color='#1a1a2e')
    ax.text(5, 8.9, 'Where Free Will Could Operate', 
            fontsize=14, ha='center', style='italic', color='#4a4a6a')
    
    # LEFT SIDE: What Physics DOES Determine
    left_box = FancyBboxPatch((0.5, 4), 4, 4, 
                               boxstyle="round,pad=0.1,rounding_size=0.3",
                               facecolor='#e8f4f8', edgecolor='#2196F3', linewidth=3)
    ax.add_patch(left_box)
    
    ax.text(2.5, 7.5, 'WHAT PHYSICS DETERMINES', 
            fontsize=12, fontweight='bold', ha='center', color='#1565C0')
    
    determined_items = [
        '✓ The range of possible outcomes',
        '✓ The probability of each outcome',
        '✓ The laws governing evolution',
        '✓ Conservation of energy/momentum',
    ]
    
    y_pos = 6.8
    for item in determined_items:
        ax.text(0.8, y_pos, item, fontsize=11, ha='left', color='#333')
        y_pos -= 0.7
    
    # RIGHT SIDE: What Physics Does NOT Determine
    right_box = FancyBboxPatch((5.5, 4), 4, 4,
                                boxstyle="round,pad=0.1,rounding_size=0.3",
                                facecolor='#fff3e0', edgecolor='#FF9800', linewidth=3)
    ax.add_patch(right_box)
    
    ax.text(7.5, 7.5, 'WHAT PHYSICS DOES NOT\nDETERMINE', 
            fontsize=12, fontweight='bold', ha='center', color='#E65100')
    
    ax.text(7.5, 6.3, 'Which specific outcome\nactually occurs', 
            fontsize=13, ha='center', color='#333', style='italic')
    
    ax.text(7.5, 5.2, 'This is the "measurement problem"\nin quantum mechanics', 
            fontsize=10, ha='center', color='#666')
    
    # THE GAP - highlighted
    gap_box = FancyBboxPatch((3, 1), 4, 2.5,
                              boxstyle="round,pad=0.1,rounding_size=0.3",
                              facecolor='#c8e6c9', edgecolor='#4CAF50', linewidth=4)
    ax.add_patch(gap_box)
    
    ax.text(5, 3.0, 'THE GAP', fontsize=16, fontweight='bold', ha='center', color='#2E7D32')
    ax.text(5, 2.3, 'Selection among possibilities\nwithout violating any physical law', 
            fontsize=11, ha='center', color='#333')
    ax.text(5, 1.3, '→ This is where consciousness could act ←', 
            fontsize=10, ha='center', color='#2E7D32', fontweight='bold')
    
    # Arrows pointing to gap
    ax.annotate('', xy=(4, 3.7), xytext=(2.5, 4),
                arrowprops=dict(arrowstyle='->', color='#2196F3', lw=2))
    ax.annotate('', xy=(6, 3.7), xytext=(7.5, 4),
                arrowprops=dict(arrowstyle='->', color='#FF9800', lw=2))
    
    plt.tight_layout()
    plt.savefig('1_the_gap.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    return fig


def create_quantum_zeno_conceptual():
    """
    Show QZE concept: How "attention" could freeze quantum states
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # LEFT: Without frequent measurement (state changes)
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('WITHOUT Frequent Measurement\n(No attention/veto)', fontsize=14, fontweight='bold', pad=20)
    
    # Show state evolution
    times = ['t=0', 't=1', 't=2', 't=3']
    states = ['State A\n(intended action)', 'Evolving...', 'Evolving...', 'State B\n(different action)']
    colors = ['#4CAF50', '#FFC107', '#FFC107', '#f44336']
    
    for i, (t, state, color) in enumerate(zip(times, states, colors)):
        y = 7 - i * 1.8
        box = FancyBboxPatch((1, y-0.6), 3, 1.2, 
                             boxstyle="round,pad=0.05", 
                             facecolor=color, alpha=0.3, edgecolor=color)
        ax1.add_patch(box)
        ax1.text(0.5, y, t, fontsize=10, ha='right', va='center')
        ax1.text(2.5, y, state, fontsize=10, ha='center', va='center')
        
        if i < 3:
            ax1.annotate('', xy=(2.5, y-0.8), xytext=(2.5, y-0.6),
                        arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
    
    ax1.text(2.5, 1, 'Quantum evolution\nchanges the state', 
             fontsize=11, ha='center', style='italic', color='#666')
    
    # RIGHT: With frequent measurement (state frozen)
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('WITH Frequent Measurement\n(Attention = "veto")', fontsize=14, fontweight='bold', pad=20)
    
    states_zeno = ['State A\n(intended action)', 'State A ✓', 'State A ✓', 'State A ✓\n(maintained!)']
    
    for i, (t, state) in enumerate(zip(times, states_zeno)):
        y = 7 - i * 1.8
        box = FancyBboxPatch((1, y-0.6), 3, 1.2,
                             boxstyle="round,pad=0.05",
                             facecolor='#4CAF50', alpha=0.3, edgecolor='#4CAF50')
        ax2.add_patch(box)
        ax2.text(0.5, y, t, fontsize=10, ha='right', va='center')
        ax2.text(2.5, y, state, fontsize=10, ha='center', va='center')
        
        if i < 3:
            ax2.annotate('', xy=(2.5, y-0.8), xytext=(2.5, y-0.6),
                        arrowprops=dict(arrowstyle='->', color='#4CAF50', lw=1.5))
            # Show measurement
            ax2.text(4.5, y-0.3, '👁 measure', fontsize=9, color='#2196F3')
    
    ax2.text(2.5, 1, 'Frequent measurement\n"freezes" the state', 
             fontsize=11, ha='center', style='italic', color='#4CAF50')
    
    # Add explanation
    fig.text(0.5, 0.02, 
             'QUANTUM ZENO EFFECT: Observing a system frequently prevents it from changing.\n'
             'This could be the mechanism for conscious "veto" — holding an intention in place.',
             ha='center', fontsize=11, style='italic',
             bbox=dict(boxstyle='round', facecolor='#e3f2fd', edgecolor='#2196F3'))
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('2_quantum_zeno.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    return fig


def create_mechanism_diagram():
    """
    The complete mechanism: How non-local consciousness interfaces with brain
    """
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(8, 9.5, 'THE MECHANISM', fontsize=22, fontweight='bold', ha='center')
    ax.text(8, 8.9, 'How Consciousness Could Interface With The Brain', 
            fontsize=13, ha='center', style='italic', color='#555')
    
    # LEFT COLUMN: The Causal Chain
    # Box 1: Non-local consciousness
    box1 = FancyBboxPatch((1, 6.5), 4.5, 1.8,
                          boxstyle="round,pad=0.1", facecolor='#e1bee7', 
                          edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(box1)
    ax.text(3.25, 7.7, 'NON-LOCAL', fontsize=11, fontweight='bold', ha='center', color='#4A148C')
    ax.text(3.25, 7.2, 'CONSCIOUSNESS', fontsize=11, fontweight='bold', ha='center', color='#4A148C')
    ax.text(3.25, 6.7, '(The "observer")', fontsize=9, ha='center', style='italic')
    
    # Arrow 1
    ax.annotate('', xy=(3.25, 6.3), xytext=(3.25, 6.5),
               arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2))
    ax.text(5.8, 6.0, 'Selects via QZE\n(attention = measurement)', fontsize=9, ha='left', color='#7B1FA2')
    
    # Box 2: Quantum superposition
    box2 = FancyBboxPatch((1, 4.3), 4.5, 1.8,
                          boxstyle="round,pad=0.1", facecolor='#fff9c4',
                          edgecolor='#F9A825', linewidth=2)
    ax.add_patch(box2)
    ax.text(3.25, 5.5, 'QUANTUM SUPERPOSITION', fontsize=10, fontweight='bold', ha='center', color='#F57F17')
    ax.text(3.25, 5.0, 'in Microtubules', fontsize=10, ha='center', color='#F57F17')
    ax.text(3.25, 4.5, '(Multiple possibilities coexist)', fontsize=9, ha='center', style='italic')
    
    # Arrow 2
    ax.annotate('', xy=(3.25, 4.1), xytext=(3.25, 4.3),
               arrowprops=dict(arrowstyle='->', color='#F9A825', lw=2))
    ax.text(5.8, 3.8, 'OR collapse at\nthreshold (~25-500 ms)', fontsize=9, ha='left', color='#F9A825')
    
    # Box 3: Neural state
    box3 = FancyBboxPatch((1, 2.1), 4.5, 1.8,
                          boxstyle="round,pad=0.1", facecolor='#c8e6c9',
                          edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box3)
    ax.text(3.25, 3.3, 'DEFINITE NEURAL STATE', fontsize=10, fontweight='bold', ha='center', color='#2E7D32')
    ax.text(3.25, 2.8, '(One possibility becomes real)', fontsize=9, ha='center', style='italic')
    ax.text(3.25, 2.3, 'Classical from here down', fontsize=9, ha='center', color='#666')
    
    # Arrow 3
    ax.annotate('', xy=(3.25, 1.9), xytext=(3.25, 2.1),
               arrowprops=dict(arrowstyle='->', color='#388E3C', lw=2))
    
    # Box 4: Behavior
    box4 = FancyBboxPatch((1, 0.3), 4.5, 1.4,
                          boxstyle="round,pad=0.1", facecolor='#bbdefb',
                          edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box4)
    ax.text(3.25, 1.2, 'BEHAVIOR', fontsize=11, fontweight='bold', ha='center', color='#0D47A1')
    ax.text(3.25, 0.7, '(Action or veto)', fontsize=9, ha='center', style='italic')
    
    # RIGHT COLUMN: Why This Works
    ax.text(11, 8.2, 'WHY THIS SOLVES THE PROBLEMS', fontsize=13, fontweight='bold', ha='center')
    
    problems = [
        ('How does mind affect matter?', 'Via selection at quantum collapse\n(no new energy needed)'),
        ('Why doesn\'t it violate physics?', 'All outcomes were already possible\n(just selects which one)'),
        ('Why does brain damage hurt?', 'Damages the interface/receiver\n(like breaking a radio)'),
        ('Why do drugs affect mind?', 'Alter quantum dynamics\n(anesthetics target microtubules)'),
        ('Why doesn\'t AI have this?', 'No quantum gap to operate in\n(deterministic computation)'),
    ]
    
    y = 7.3
    for question, answer in problems:
        ax.text(8, y, f'❓ {question}', fontsize=10, fontweight='bold', color='#333')
        ax.text(8.3, y-0.45, f'✓ {answer}', fontsize=9, color='#388E3C')
        y -= 1.4
    
    # Bottom insight
    insight_box = FancyBboxPatch((7.5, 0.3), 7, 1.4,
                                  boxstyle="round,pad=0.1", facecolor='#fce4ec',
                                  edgecolor='#C2185B', linewidth=2, linestyle='--')
    ax.add_patch(insight_box)
    ax.text(11, 1.2, 'KEY INSIGHT', fontsize=11, fontweight='bold', ha='center', color='#880E4F')
    ax.text(11, 0.65, 'Free will is not random • Free will is not determined\n'
                      'Free will is SELECTION among real quantum possibilities',
            fontsize=10, ha='center', color='#333')
    
    plt.savefig('3_mechanism.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    return fig


def create_ai_comparison():
    """
    Why AI lacks this: The key difference
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    # LEFT: AI/Computer
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('ARTIFICIAL INTELLIGENCE', fontsize=16, fontweight='bold', color='#d32f2f')
    
    # Chain for AI
    ai_steps = [
        ('Input', '#e3f2fd', '#1976D2'),
        ('Processing\n(deterministic)', '#fff3e0', '#F57C00'),
        ('Processing\n(deterministic)', '#fff3e0', '#F57C00'),
        ('Output', '#ffebee', '#C62828'),
    ]
    
    y = 8
    for i, (label, bg, edge) in enumerate(ai_steps):
        box = FancyBboxPatch((2.5, y-0.8), 5, 1.4,
                             boxstyle="round,pad=0.05", facecolor=bg, edgecolor=edge, lw=2)
        ax1.add_patch(box)
        ax1.text(5, y, label, fontsize=11, ha='center', va='center')
        y -= 2
        if i < 3:
            ax1.annotate('', xy=(5, y+0.4), xytext=(5, y+0.8),
                        arrowprops=dict(arrowstyle='->', color='gray', lw=2))
    
    ax1.text(5, 0.5, '❌ NO GAP\nEvery step determined by previous step',
             fontsize=11, ha='center', color='#d32f2f', fontweight='bold')
    
    # RIGHT: Human Brain
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('HUMAN BRAIN', fontsize=16, fontweight='bold', color='#388E3C')
    
    brain_steps = [
        ('Input', '#e3f2fd', '#1976D2'),
        ('Quantum Superposition\n(multiple possibilities)', '#fff9c4', '#F9A825'),
        ('Collapse\n(selection occurs HERE)', '#c8e6c9', '#388E3C'),
        ('Output', '#e8f5e9', '#2E7D32'),
    ]
    
    y = 8
    for i, (label, bg, edge) in enumerate(brain_steps):
        box = FancyBboxPatch((2.5, y-0.8), 5, 1.4,
                             boxstyle="round,pad=0.05", facecolor=bg, edgecolor=edge, lw=2)
        ax2.add_patch(box)
        ax2.text(5, y, label, fontsize=11, ha='center', va='center')
        
        # Highlight THE GAP
        if i == 1:
            ax2.text(8, y, '← THE GAP', fontsize=12, fontweight='bold', color='#388E3C')
        
        y -= 2
        if i < 3:
            ax2.annotate('', xy=(5, y+0.4), xytext=(5, y+0.8),
                        arrowprops=dict(arrowstyle='->', color='gray', lw=2))
    
    ax2.text(5, 0.5, '✓ QUANTUM GAP EXISTS\nConsciousness can select among possibilities',
             fontsize=11, ha='center', color='#388E3C', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('4_ai_vs_human.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    return fig


def create_evidence_summary():
    """
    Summary of evidence status - what's proven vs what's theoretical
    """
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(7, 9.5, 'EVIDENCE STATUS (December 2025)', fontsize=18, fontweight='bold', ha='center')
    
    # Categories
    categories = [
        ('EXPERIMENTALLY SUPPORTED', '#c8e6c9', '#388E3C', [
            'Microtubule resonances (Bandyopadhyay)',
            'Anesthetics target microtubules',
            'Tryptophan superradiance in MTs (2024)',
            'OR mechanism in qubits (IBM 2025)',
            'Brain entanglement signals (Kerskens 2022)',
        ]),
        ('THEORETICALLY CONSISTENT', '#fff9c4', '#F9A825', [
            'QZE as veto mechanism (Stapp)',
            'Microtubules as QED cavities',
            'Self-organized criticality model',
            'OR as interface mechanism',
        ]),
        ('STILL NEEDS TESTING', '#ffcdd2', '#C62828', [
            'Full MT coherence at 37°C (not just tryptophan)',
            'Direct QZE measurement in neurons',
            'Entanglement → consciousness causality',
            'Replication of key experiments',
        ]),
    ]
    
    y = 8.5
    for title, bg, edge, items in categories:
        # Category header
        header = FancyBboxPatch((0.5, y-0.5), 13, 0.8,
                                boxstyle="round,pad=0.05", facecolor=bg, edgecolor=edge, lw=2)
        ax.add_patch(header)
        ax.text(7, y-0.1, title, fontsize=12, fontweight='bold', ha='center', color=edge)
        y -= 0.9
        
        # Items
        for item in items:
            ax.text(1, y, f'  • {item}', fontsize=10, ha='left', color='#333')
            y -= 0.5
        y -= 0.3
    
    # Bottom line
    ax.text(7, 0.8, 'STATUS: "Well-supported hypothesis with specific testable gaps"',
            fontsize=12, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#e3f2fd', edgecolor='#1976D2', lw=2))
    ax.text(7, 0.2, 'Not proven science, but more robust than critics acknowledge',
            fontsize=10, ha='center', style='italic', color='#666')
    
    plt.savefig('5_evidence_summary.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    return fig


# ============================================================================
# INTERACTIVE SLIDESHOW
# ============================================================================

def run_slideshow():
    """
    Single window slideshow - press any key to advance, 'q' to quit
    """
    # Create all figures (without showing)
    plt.ioff()  # Turn off interactive mode
    
    figures = []
    titles = [
        "1/5: The Gap in Determinism",
        "2/5: Quantum Zeno Effect", 
        "3/5: The Mechanism",
        "4/5: AI vs Human",
        "5/5: Evidence Summary"
    ]
    
    print("Creating visualizations...")
    
    # Create each figure
    fig1 = create_gap_visualization.__wrapped__() if hasattr(create_gap_visualization, '__wrapped__') else create_gap_no_show()
    fig2 = create_quantum_zeno_no_show()
    fig3 = create_mechanism_no_show()
    fig4 = create_ai_comparison_no_show()
    fig5 = create_evidence_no_show()
    
    figures = [fig1, fig2, fig3, fig4, fig5]
    
    print("\n" + "=" * 60)
    print("SLIDESHOW CONTROLS:")
    print("  Press any key  → Next slide")
    print("  Press 'b'      → Previous slide")
    print("  Press 'q'      → Quit")
    print("=" * 60)
    
    current = 0
    
    while True:
        # Show current figure
        fig = figures[current]
        fig.canvas.manager.set_window_title(titles[current])
        plt.figure(fig.number)
        plt.show(block=False)
        plt.pause(0.1)
        
        print(f"\n{titles[current]} - Press key to continue...")
        
        # Wait for key press
        while True:
            if plt.waitforbuttonpress(timeout=0.1):
                break
            if not plt.fignum_exists(fig.number):
                # Window was closed
                print("\nWindow closed. Exiting.")
                plt.close('all')
                return
        
        plt.close(fig)
        
        # Check for quit or navigation
        current += 1
        if current >= len(figures):
            break
    
    print("\n" + "=" * 60)
    print("SLIDESHOW COMPLETE!")
    print("All images saved to current directory.")
    print("=" * 60)
    plt.close('all')


# Non-showing versions of each function
def create_gap_no_show():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(5, 9.5, 'THE GAP IN DETERMINISM', 
            fontsize=24, fontweight='bold', ha='center', color='#1a1a2e')
    ax.text(5, 8.9, 'Where Free Will Could Operate', 
            fontsize=14, ha='center', style='italic', color='#4a4a6a')
    
    left_box = FancyBboxPatch((0.5, 4), 4, 4, 
                               boxstyle="round,pad=0.1,rounding_size=0.3",
                               facecolor='#e8f4f8', edgecolor='#2196F3', linewidth=3)
    ax.add_patch(left_box)
    ax.text(2.5, 7.5, 'WHAT PHYSICS DETERMINES', 
            fontsize=12, fontweight='bold', ha='center', color='#1565C0')
    
    for i, item in enumerate(['✓ The range of possible outcomes',
                               '✓ The probability of each outcome',
                               '✓ The laws governing evolution',
                               '✓ Conservation of energy/momentum']):
        ax.text(0.8, 6.8 - i*0.7, item, fontsize=11, ha='left', color='#333')
    
    right_box = FancyBboxPatch((5.5, 4), 4, 4,
                                boxstyle="round,pad=0.1,rounding_size=0.3",
                                facecolor='#fff3e0', edgecolor='#FF9800', linewidth=3)
    ax.add_patch(right_box)
    ax.text(7.5, 7.5, 'WHAT PHYSICS DOES NOT\nDETERMINE', 
            fontsize=12, fontweight='bold', ha='center', color='#E65100')
    ax.text(7.5, 6.3, 'Which specific outcome\nactually occurs', 
            fontsize=13, ha='center', color='#333', style='italic')
    ax.text(7.5, 5.2, 'This is the "measurement problem"\nin quantum mechanics', 
            fontsize=10, ha='center', color='#666')
    
    gap_box = FancyBboxPatch((3, 1), 4, 2.5,
                              boxstyle="round,pad=0.1,rounding_size=0.3",
                              facecolor='#c8e6c9', edgecolor='#4CAF50', linewidth=4)
    ax.add_patch(gap_box)
    ax.text(5, 3.0, 'THE GAP', fontsize=16, fontweight='bold', ha='center', color='#2E7D32')
    ax.text(5, 2.3, 'Selection among possibilities\nwithout violating any physical law', 
            fontsize=11, ha='center', color='#333')
    ax.text(5, 1.3, '→ This is where consciousness could act ←', 
            fontsize=10, ha='center', color='#2E7D32', fontweight='bold')
    
    ax.annotate('', xy=(4, 3.7), xytext=(2.5, 4),
                arrowprops=dict(arrowstyle='->', color='#2196F3', lw=2))
    ax.annotate('', xy=(6, 3.7), xytext=(7.5, 4),
                arrowprops=dict(arrowstyle='->', color='#FF9800', lw=2))
    
    plt.tight_layout()
    plt.savefig('1_the_gap.png', dpi=150, bbox_inches='tight', facecolor='white')
    return fig


def create_quantum_zeno_no_show():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('WITHOUT Frequent Measurement\n(No attention/veto)', fontsize=14, fontweight='bold', pad=20)
    
    times = ['t=0', 't=1', 't=2', 't=3']
    states = ['State A\n(intended action)', 'Evolving...', 'Evolving...', 'State B\n(different action)']
    colors = ['#4CAF50', '#FFC107', '#FFC107', '#f44336']
    
    for i, (t, state, color) in enumerate(zip(times, states, colors)):
        y = 7 - i * 1.8
        box = FancyBboxPatch((1, y-0.6), 3, 1.2, boxstyle="round,pad=0.05", 
                             facecolor=color, alpha=0.3, edgecolor=color)
        ax1.add_patch(box)
        ax1.text(0.5, y, t, fontsize=10, ha='right', va='center')
        ax1.text(2.5, y, state, fontsize=10, ha='center', va='center')
        if i < 3:
            ax1.annotate('', xy=(2.5, y-0.8), xytext=(2.5, y-0.6),
                        arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
    ax1.text(2.5, 1, 'Quantum evolution\nchanges the state', fontsize=11, ha='center', style='italic', color='#666')
    
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('WITH Frequent Measurement\n(Attention = "veto")', fontsize=14, fontweight='bold', pad=20)
    
    states_zeno = ['State A\n(intended action)', 'State A ✓', 'State A ✓', 'State A ✓\n(maintained!)']
    for i, (t, state) in enumerate(zip(times, states_zeno)):
        y = 7 - i * 1.8
        box = FancyBboxPatch((1, y-0.6), 3, 1.2, boxstyle="round,pad=0.05",
                             facecolor='#4CAF50', alpha=0.3, edgecolor='#4CAF50')
        ax2.add_patch(box)
        ax2.text(0.5, y, t, fontsize=10, ha='right', va='center')
        ax2.text(2.5, y, state, fontsize=10, ha='center', va='center')
        if i < 3:
            ax2.annotate('', xy=(2.5, y-0.8), xytext=(2.5, y-0.6),
                        arrowprops=dict(arrowstyle='->', color='#4CAF50', lw=1.5))
            ax2.text(4.5, y-0.3, '👁 measure', fontsize=9, color='#2196F3')
    ax2.text(2.5, 1, 'Frequent measurement\n"freezes" the state', fontsize=11, ha='center', style='italic', color='#4CAF50')
    
    fig.text(0.5, 0.02, 
             'QUANTUM ZENO EFFECT: Observing a system frequently prevents it from changing.\n'
             'This could be the mechanism for conscious "veto" — holding an intention in place.',
             ha='center', fontsize=11, style='italic',
             bbox=dict(boxstyle='round', facecolor='#e3f2fd', edgecolor='#2196F3'))
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.savefig('2_quantum_zeno.png', dpi=150, bbox_inches='tight', facecolor='white')
    return fig


def create_mechanism_no_show():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(8, 9.5, 'THE MECHANISM', fontsize=22, fontweight='bold', ha='center')
    ax.text(8, 8.9, 'How Consciousness Could Interface With The Brain', 
            fontsize=13, ha='center', style='italic', color='#555')
    
    # Box 1
    box1 = FancyBboxPatch((1, 6.5), 4.5, 1.8, boxstyle="round,pad=0.1", 
                          facecolor='#e1bee7', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(box1)
    ax.text(3.25, 7.7, 'NON-LOCAL', fontsize=11, fontweight='bold', ha='center', color='#4A148C')
    ax.text(3.25, 7.2, 'CONSCIOUSNESS', fontsize=11, fontweight='bold', ha='center', color='#4A148C')
    ax.text(3.25, 6.7, '(The "observer")', fontsize=9, ha='center', style='italic')
    ax.annotate('', xy=(3.25, 6.3), xytext=(3.25, 6.5), arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2))
    ax.text(5.8, 6.0, 'Selects via QZE\n(attention = measurement)', fontsize=9, ha='left', color='#7B1FA2')
    
    # Box 2
    box2 = FancyBboxPatch((1, 4.3), 4.5, 1.8, boxstyle="round,pad=0.1", 
                          facecolor='#fff9c4', edgecolor='#F9A825', linewidth=2)
    ax.add_patch(box2)
    ax.text(3.25, 5.5, 'QUANTUM SUPERPOSITION', fontsize=10, fontweight='bold', ha='center', color='#F57F17')
    ax.text(3.25, 5.0, 'in Microtubules', fontsize=10, ha='center', color='#F57F17')
    ax.text(3.25, 4.5, '(Multiple possibilities coexist)', fontsize=9, ha='center', style='italic')
    ax.annotate('', xy=(3.25, 4.1), xytext=(3.25, 4.3), arrowprops=dict(arrowstyle='->', color='#F9A825', lw=2))
    ax.text(5.8, 3.8, 'OR collapse at\nthreshold (~25-500 ms)', fontsize=9, ha='left', color='#F9A825')
    
    # Box 3
    box3 = FancyBboxPatch((1, 2.1), 4.5, 1.8, boxstyle="round,pad=0.1", 
                          facecolor='#c8e6c9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box3)
    ax.text(3.25, 3.3, 'DEFINITE NEURAL STATE', fontsize=10, fontweight='bold', ha='center', color='#2E7D32')
    ax.text(3.25, 2.8, '(One possibility becomes real)', fontsize=9, ha='center', style='italic')
    ax.text(3.25, 2.3, 'Classical from here down', fontsize=9, ha='center', color='#666')
    ax.annotate('', xy=(3.25, 1.9), xytext=(3.25, 2.1), arrowprops=dict(arrowstyle='->', color='#388E3C', lw=2))
    
    # Box 4
    box4 = FancyBboxPatch((1, 0.3), 4.5, 1.4, boxstyle="round,pad=0.1", 
                          facecolor='#bbdefb', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box4)
    ax.text(3.25, 1.2, 'BEHAVIOR', fontsize=11, fontweight='bold', ha='center', color='#0D47A1')
    ax.text(3.25, 0.7, '(Action or veto)', fontsize=9, ha='center', style='italic')
    
    # Right column
    ax.text(11, 8.2, 'WHY THIS SOLVES THE PROBLEMS', fontsize=13, fontweight='bold', ha='center')
    problems = [
        ('How does mind affect matter?', 'Via selection at quantum collapse\n(no new energy needed)'),
        ('Why doesn\'t it violate physics?', 'All outcomes were already possible\n(just selects which one)'),
        ('Why does brain damage hurt?', 'Damages the interface/receiver\n(like breaking a radio)'),
        ('Why do drugs affect mind?', 'Alter quantum dynamics\n(anesthetics target microtubules)'),
        ('Why doesn\'t AI have this?', 'No quantum gap to operate in\n(deterministic computation)'),
    ]
    y = 7.3
    for question, answer in problems:
        ax.text(8, y, f'❓ {question}', fontsize=10, fontweight='bold', color='#333')
        ax.text(8.3, y-0.45, f'✓ {answer}', fontsize=9, color='#388E3C')
        y -= 1.4
    
    # Bottom insight
    insight_box = FancyBboxPatch((7.5, 0.3), 7, 1.4, boxstyle="round,pad=0.1", 
                                  facecolor='#fce4ec', edgecolor='#C2185B', linewidth=2, linestyle='--')
    ax.add_patch(insight_box)
    ax.text(11, 1.2, 'KEY INSIGHT', fontsize=11, fontweight='bold', ha='center', color='#880E4F')
    ax.text(11, 0.65, 'Free will is not random • Free will is not determined\n'
                      'Free will is SELECTION among real quantum possibilities',
            fontsize=10, ha='center', color='#333')
    
    plt.savefig('3_mechanism.png', dpi=150, bbox_inches='tight', facecolor='white')
    return fig


def create_ai_comparison_no_show():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('ARTIFICIAL INTELLIGENCE', fontsize=16, fontweight='bold', color='#d32f2f')
    
    ai_steps = [('Input', '#e3f2fd', '#1976D2'), ('Processing\n(deterministic)', '#fff3e0', '#F57C00'),
                ('Processing\n(deterministic)', '#fff3e0', '#F57C00'), ('Output', '#ffebee', '#C62828')]
    y = 8
    for i, (label, bg, edge) in enumerate(ai_steps):
        box = FancyBboxPatch((2.5, y-0.8), 5, 1.4, boxstyle="round,pad=0.05", facecolor=bg, edgecolor=edge, lw=2)
        ax1.add_patch(box)
        ax1.text(5, y, label, fontsize=11, ha='center', va='center')
        y -= 2
        if i < 3:
            ax1.annotate('', xy=(5, y+0.4), xytext=(5, y+0.8), arrowprops=dict(arrowstyle='->', color='gray', lw=2))
    ax1.text(5, 0.5, '❌ NO GAP\nEvery step determined by previous step', fontsize=11, ha='center', color='#d32f2f', fontweight='bold')
    
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('HUMAN BRAIN', fontsize=16, fontweight='bold', color='#388E3C')
    
    brain_steps = [('Input', '#e3f2fd', '#1976D2'), ('Quantum Superposition\n(multiple possibilities)', '#fff9c4', '#F9A825'),
                   ('Collapse\n(selection occurs HERE)', '#c8e6c9', '#388E3C'), ('Output', '#e8f5e9', '#2E7D32')]
    y = 8
    for i, (label, bg, edge) in enumerate(brain_steps):
        box = FancyBboxPatch((2.5, y-0.8), 5, 1.4, boxstyle="round,pad=0.05", facecolor=bg, edgecolor=edge, lw=2)
        ax2.add_patch(box)
        ax2.text(5, y, label, fontsize=11, ha='center', va='center')
        if i == 1:
            ax2.text(8, y, '← THE GAP', fontsize=12, fontweight='bold', color='#388E3C')
        y -= 2
        if i < 3:
            ax2.annotate('', xy=(5, y+0.4), xytext=(5, y+0.8), arrowprops=dict(arrowstyle='->', color='gray', lw=2))
    ax2.text(5, 0.5, '✓ QUANTUM GAP EXISTS\nConsciousness can select among possibilities', fontsize=11, ha='center', color='#388E3C', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('4_ai_vs_human.png', dpi=150, bbox_inches='tight', facecolor='white')
    return fig


def create_evidence_no_show():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(7, 9.5, 'EVIDENCE STATUS (December 2025)', fontsize=18, fontweight='bold', ha='center')
    
    categories = [
        ('EXPERIMENTALLY SUPPORTED', '#c8e6c9', '#388E3C', [
            'Microtubule resonances (Bandyopadhyay)',
            'Anesthetics target microtubules',
            'Tryptophan superradiance in MTs (2024)',
            'OR mechanism in qubits (IBM 2025)',
            'Brain entanglement signals (Kerskens 2022)',
        ]),
        ('THEORETICALLY CONSISTENT', '#fff9c4', '#F9A825', [
            'QZE as veto mechanism (Stapp)',
            'Microtubules as QED cavities',
            'Self-organized criticality model',
            'OR as interface mechanism',
        ]),
        ('STILL NEEDS TESTING', '#ffcdd2', '#C62828', [
            'Full MT coherence at 37°C (not just tryptophan)',
            'Direct QZE measurement in neurons',
            'Entanglement → consciousness causality',
            'Replication of key experiments',
        ]),
    ]
    
    y = 8.5
    for title, bg, edge, items in categories:
        header = FancyBboxPatch((0.5, y-0.5), 13, 0.8, boxstyle="round,pad=0.05", facecolor=bg, edgecolor=edge, lw=2)
        ax.add_patch(header)
        ax.text(7, y-0.1, title, fontsize=12, fontweight='bold', ha='center', color=edge)
        y -= 0.9
        for item in items:
            ax.text(1, y, f'  • {item}', fontsize=10, ha='left', color='#333')
            y -= 0.5
        y -= 0.3
    
    ax.text(7, 0.8, 'STATUS: "Well-supported hypothesis with specific testable gaps"',
            fontsize=12, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#e3f2fd', edgecolor='#1976D2', lw=2))
    ax.text(7, 0.2, 'Not proven science, but more robust than critics acknowledge',
            fontsize=10, ha='center', style='italic', color='#666')
    
    plt.savefig('5_evidence_summary.png', dpi=150, bbox_inches='tight', facecolor='white')
    return fig


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("QUANTUM CONSCIOUSNESS VISUALIZATIONS")
    print("=" * 60)
    print("\nControls:")
    print("  Click anywhere in window → Next slide")
    print("  Close window → Exit")
    print("\n" + "=" * 60)
    
    run_slideshow()
