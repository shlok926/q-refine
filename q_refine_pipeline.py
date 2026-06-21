import numpy as np
import matplotlib.pyplot as plt
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit import transpile
import os

from q_refine.circuits.qnn import generate_trained_qnn
from q_refine.circuits.bv import bernstein_vazirani
from q_refine.circuits.simon import simon_algorithm
from q_refine.circuits.grover import grover_algorithm
from q_refine.mitigation_engine.q_sanitizer import QSanitizer
from q_refine.benchmark_engine.hardware_profiler import HardwareProfiler
from q_refine.mitigation_engine.topology_optimizer import TopologyOptimizer
from q_refine.core.dashboard import QRefineDashboard

def get_success_probability(circuit, secret, noise_model):
    """Runs the circuit on a noisy simulator and returns probability of finding the secret."""
    backend = AerSimulator(noise_model=noise_model)
    result = backend.run(circuit, shots=2000).result()
    counts = result.get_counts()
    
    if circuit.name == "Simon":
        success_shots = 0
        total_shots = sum(counts.values())
        for bitstring, count in counts.items():
            dot_product = sum(int(b) * int(s) for b, s in zip(bitstring[::-1], secret))
            if dot_product % 2 == 0:
                success_shots += count
        return success_shots / total_shots if total_shots > 0 else 0
    else:
        qiskit_secret = secret[::-1]
        return counts.get(qiskit_secret, 0) / 2000.0

def run_comparative_sweep():
    print("\n========================================")
    print(" Running Comparative Robustness Sweep ")
    print("========================================")
    
    noise_levels = [0.0, 0.01, 0.05, 0.10]
    algos = {
        "Bernstein-Vazirani": ("11", bernstein_vazirani),
        "Simon's Algorithm": ("11", simon_algorithm),
        "Grover's Search (2-Qubit)": ("11", lambda _: grover_algorithm())
    }
    
    results = {name: [] for name in algos.keys()}
    
    for p in noise_levels:
        noise_model = NoiseModel()
        if p > 0:
            error_1q = depolarizing_error(p, 1)
            error_2q = depolarizing_error(p, 2)
            noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x', 'ry', 'rz'])
            noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])
        
        print(f"\n[*] Testing at Noise Level p = {p}")
        for name, (secret, func) in algos.items():
            if name == "Grover's Search (2-Qubit)":
                raw_circuit = func(None)
            else:
                raw_circuit = func(secret)
            
            optimized_circuit = transpile(raw_circuit, AerSimulator())
            prob = get_success_probability(optimized_circuit, secret, noise_model)
            results[name].append(prob)
            print(f"    - {name}: {prob:.2%} success")
            
    # Plotting
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    markers = ['o', 's', '^']
    colors = ['#00d2ff', '#ff4b4b', '#2ca02c']
    
    for idx, (name, probs) in enumerate(results.items()):
        plt.plot(noise_levels, probs, marker=markers[idx], color=colors[idx], label=name, linewidth=2, markersize=8)
        
    plt.title('Comparative Algorithm Robustness under Depolarizing Noise', fontsize=14, fontweight='bold', color='white')
    plt.xlabel('Noise Probability (p)', fontsize=12, color='white')
    plt.ylabel('Success Probability', fontsize=12, color='white')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(fontsize=11)
    plt.ylim(0, 1.05)
    
    sweep_img_path = "comparative_sweep.png"
    plt.savefig(sweep_img_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    
    print(f"\n[+] Comparative Sweep Graph saved as {sweep_img_path}")


def main():
    print("========================================")
    print(" Welcome to Q-Refine Enterprise Pipeline ")
    print("========================================")
    
    # Run the Comparative Sweep first
    run_comparative_sweep()
    
    print("\n========================================")
    print(" Running Q-Sanitizer (ZNE Pipeline) ")
    print("========================================")
    
    # Step 0: Profile Hardware
    print("\n[0] Profiling Target Hardware...")
    profiler = HardwareProfiler(use_real_hardware=False, backend_name="fake_brisbane")
    noise_model = profiler.get_noise_model()
    coupling_map = profiler.get_coupling_map()
    
    secret_string = "0" * 5  # The QNN is trained to output 00000
    
    # 1. Generate Raw Circuit (Quantum AI Neural Network)
    print(f"\n[1] Generating Quantum Neural Network (QNN) circuit for 5 qubits...")
    raw_circuit = generate_trained_qnn(num_qubits=5, num_layers=2)
    
    # 1.5 Topology Optimization
    print("\n[1.5] Passing circuit to Topology Optimizer...")
    optimizer = TopologyOptimizer(profiler.backend, coupling_map)
    optimized_circuit = optimizer.optimize(raw_circuit)
    
    # Let's see how the unmitigated circuit performs under REAL hardware noise
    raw_prob = get_success_probability(optimized_circuit, secret_string, noise_model)
    print(f"    Raw Circuit Success Probability (Unmitigated on IBM Brisbane): {raw_prob:.2%}")
    
    # 2. Refine Circuit using ZNE Mitigation Engine
    print("\n[2] Passing circuit to Q-Sanitizer (ZNE Mitigation Engine)...")
    sanitizer = QSanitizer(mitigation_method="ZNE")
    
    # Get folded circuits for scale factors 1, 3, 5
    folded_circuits = sanitizer.refine(optimized_circuit)
    
    scale_factors = []
    noisy_probs = []
    
    for scale, folded_circ in folded_circuits.items():
        prob = get_success_probability(folded_circ, secret_string, noise_model)
        scale_factors.append(scale)
        noisy_probs.append(prob)
        print(f"    - Noise Scale {scale}x (Depth {folded_circ.depth()}): Success Prob = {prob:.2%}")
        
    # 3. Apply Richardson Extrapolation
    print("\n[3] Applying Richardson Extrapolation to estimate Zero-Noise result...")
    mitigated_prob = sanitizer.richardson_extrapolate(noisy_probs, scale_factors)
    
    print(f"    Final Mitigated Success Probability: {mitigated_prob:.2%}")
    
    print("\n========================================")
    print(f" Summary:")
    print(f" Without Q-Refine: {raw_prob:.2%} Accuracy")
    print(f" With Q-Refine:    {mitigated_prob:.2%} Accuracy")
    print("========================================")
    
    # 4. Generate Visual Dashboard
    print("\n[4] Generating Presentation Dashboards...")
    QRefineDashboard.generate_report(raw_prob, mitigated_prob, scale_factors, noisy_probs)

if __name__ == "__main__":
    main()
