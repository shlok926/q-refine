import matplotlib.pyplot as plt
import numpy as np
import os

class QRefineDashboard:
    """
    Enterprise visualization module for Q-Refine.
    Generates professional, presentation-ready charts comparing
    Unmitigated vs Mitigated success probabilities.
    """

    @staticmethod
    def generate_report(raw_prob, mitigated_prob, scales, noisy_probs, output_path="q_refine_dashboard.png"):
        """
        Creates a high-quality visualization combining a bar chart (Before/After)
        and a line chart (ZNE Extrapolation curve).
        """
        print("[Dashboard] Generating visual analytics report...")
        
        # Set a professional dark theme style
        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Q-Refine: Quantum AI Robustness Benchmark', fontsize=18, fontweight='bold', color='#00d2ff')

        # --- Plot 1: Before vs After Bar Chart ---
        labels = ['Raw (Unmitigated)', 'Q-Refine (Mitigated)']
        values = [raw_prob * 100, mitigated_prob * 100]
        colors = ['#ff4b4b', '#00d2ff']
        
        bars = ax1.bar(labels, values, color=colors, width=0.5)
        ax1.set_ylim(0, 105)
        ax1.set_ylabel('Success Probability (%)', fontsize=12)
        ax1.set_title('Overall Accuracy Improvement', fontsize=14)
        ax1.grid(axis='y', linestyle='--', alpha=0.3)

        # Add data labels on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, yval + 1.5, f'{yval:.2f}%', 
                     ha='center', va='bottom', fontweight='bold', fontsize=12)

        # --- Plot 2: ZNE Extrapolation Line Chart ---
        ax2.plot(scales, [p * 100 for p in noisy_probs], marker='o', linestyle='-', color='#ff4b4b', 
                 linewidth=2, markersize=8, label='Measured Noise')
        
        # Plot the zero-noise extrapolated point
        ax2.plot([0], [mitigated_prob * 100], marker='*', color='#00d2ff', markersize=15, 
                 label='ZNE Prediction (Zero Noise)')
                 
        # Connect the extrapolated point to the scale=1 point
        ax2.plot([0, scales[0]], [mitigated_prob * 100, noisy_probs[0] * 100], 
                 linestyle='--', color='#00d2ff', alpha=0.7)

        ax2.set_xlim(-0.5, max(scales) + 0.5)
        ax2.set_ylim(min(noisy_probs) * 100 - 5, max(mitigated_prob, max(noisy_probs)) * 100 + 5)
        ax2.set_xlabel('Noise Scale Factor', fontsize=12)
        ax2.set_ylabel('Success Probability (%)', fontsize=12)
        ax2.set_title('Zero Noise Extrapolation (ZNE) Curve', fontsize=14)
        ax2.grid(True, linestyle='--', alpha=0.3)
        ax2.legend(loc='lower left')

        plt.tight_layout()
        
        # Save and close
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close()
        
        print(f"[Dashboard] Report saved successfully to: {os.path.abspath(output_path)}")

