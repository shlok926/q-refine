import numpy as np
from qiskit_aer import AerSimulator
from q_refine.circuits.qnn import generate_trained_qnn
from q_refine.mitigation_engine.q_sanitizer import QSanitizer
from q_refine.benchmark_engine.hardware_profiler import HardwareProfiler
from q_refine.mitigation_engine.topology_optimizer import TopologyOptimizer
from q_refine.core.dashboard import QRefineDashboard

def get_success_probability(circuit, secret, noise_model):
    """Runs the circuit on a noisy simulator and returns probability of finding the secret."""
    backend = AerSimulator(noise_model=noise_model)
    
    # We assume the circuit is already optimized for the hardware topology
    result = backend.run(circuit, shots=2000).result()
    counts = result.get_counts()
    # print("        [DEBUG] Top 3 raw counts:", sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3])
    
    # Qiskit measures little-endian, so we must reverse the secret string
    qiskit_secret = secret[::-1]
    successes = counts.get(qiskit_secret, 0)
    return successes / 2000.0

def main():
    print("========================================")
    print(" Welcome to Q-Refine Enterprise Pipeline ")
    print("========================================")
    
    secret_string = "00000"
    
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
