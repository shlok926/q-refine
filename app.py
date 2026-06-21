import streamlit as st
import numpy as np
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from q_refine.circuits.qnn import generate_trained_qnn
from q_refine.circuits.bv import bernstein_vazirani
from q_refine.circuits.simon import simon_algorithm
from q_refine.circuits.grover import grover_algorithm
from q_refine.mitigation_engine.q_sanitizer import QSanitizer
from q_refine.mitigation_engine.topology_optimizer import TopologyOptimizer
from q_refine.benchmark_engine.hardware_profiler import HardwareProfiler
from q_refine.core.dashboard import QRefineDashboard
from qiskit import transpile
import os

st.set_page_config(page_title="Q-Refine Benchmark Pipeline", layout="wide", page_icon="⚛️", initial_sidebar_state="collapsed")

# Completely hide the sidebar and its toggle button
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {display: none;}
        [data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("⚛️ Q-Refine: Quantum AI Robustness Benchmark")
st.markdown("An enterprise-grade platform for testing and mitigating hardware noise in Quantum AI circuits using Zero-Noise Extrapolation (ZNE).")

st.divider()

# --- Feature Configuration ---
st.header("Pipeline Configuration")
col_c, col_h = st.columns(2)

with col_c:
    st.subheader("1. Quantum Circuit")
    circuit_type = st.selectbox("Select Circuit", ["Quantum Neural Network (QNN)", "Bernstein-Vazirani", "Simon's Algorithm", "Grover's Search (2-Qubit)"])
    
    if circuit_type in ["Bernstein-Vazirani", "Simon's Algorithm"]:
        custom_secret = st.text_input("Enter Secret Bitstring (Real Data Input)", "11")
    else:
        custom_secret = None

with col_h:
    st.subheader("2. Hardware Profiler")
    backend_type = st.selectbox("Select Target Backend", ["IBM Digital Twin (Brisbane)", "Custom Noise Level"])
    
    if backend_type == "Custom Noise Level":
        custom_noise = st.slider("Depolarizing Noise Level (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        noise_val = custom_noise / 100.0
    else:
        st.info("Uses real T1/T2 & Readout Error calibration data from IBM Brisbane.")
        noise_val = None

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    run_btn = st.button("Run Q-Refine Pipeline 🚀", type="primary", use_container_width=True)
with col_btn2:
    sweep_btn = st.button("Run Comparative Robustness Sweep 📈", use_container_width=True)

# --- Core Logic ---
def get_success_probability(circuit, secret, noise_model):
    backend = AerSimulator(noise_model=noise_model)
    result = backend.run(circuit, shots=2000).result()
    counts = result.get_counts()
    
    if circuit.name == "Simon":
        success_shots = 0
        total_shots = sum(counts.values())
        for bitstring, count in counts.items():
            # Dot product modulo 2 should be 0 for valid Simon outputs
            dot_product = sum(int(b) * int(s) for b, s in zip(bitstring[::-1], secret))
            if dot_product % 2 == 0:
                success_shots += count
        return success_shots / total_shots if total_shots > 0 else 0
    else:
        qiskit_secret = secret[::-1]
        return counts.get(qiskit_secret, 0) / 2000.0

if run_btn:
    with st.spinner("Profiling Hardware & Running Pipeline..."):
        # 1. Hardware Profiling
        if backend_type == "IBM Digital Twin (Brisbane)":
            st.info("Loading IBM Digital Twin calibration data...")
            profiler = HardwareProfiler(use_real_hardware=False, backend_name="fake_brisbane")
            noise_model = profiler.get_noise_model()
            coupling_map = profiler.get_coupling_map()
            optimizer_backend = profiler.backend
        else:
            st.info(f"Using Custom Depolarizing Noise: {custom_noise}%")
            noise_model = NoiseModel()
            error_1q = depolarizing_error(noise_val, 1)
            error_2q = depolarizing_error(noise_val, 2)
            noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x', 'ry', 'rz'])
            noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])
            coupling_map = None
            optimizer_backend = None

        # 2. Circuit Generation
        if circuit_type == "Quantum Neural Network (QNN)":
            raw_circuit = generate_trained_qnn(num_qubits=5, num_layers=2)
            secret_string = "00000"
        elif circuit_type == "Bernstein-Vazirani":
            # Sanitize user input to be only 1s and 0s
            safe_secret = ''.join([c for c in custom_secret if c in ['0', '1']])
            if not safe_secret: safe_secret = "1"
            raw_circuit = bernstein_vazirani(safe_secret)
            secret_string = safe_secret
        elif circuit_type == "Simon's Algorithm":
            safe_secret = ''.join([c for c in custom_secret if c in ['0', '1']])
            if not safe_secret: safe_secret = "11"
            raw_circuit = simon_algorithm(safe_secret)
            secret_string = safe_secret
        elif circuit_type == "Grover's Search (2-Qubit)":
            raw_circuit = grover_algorithm()
            secret_string = "11"  # Grover is hardcoded to find |11> in our implementation
            
        # 3. Topology Optimization
        if coupling_map:
            optimizer = TopologyOptimizer(optimizer_backend, coupling_map)
            optimized_circuit = optimizer.optimize(raw_circuit)
        else:
            optimized_circuit = transpile(raw_circuit, AerSimulator())

        # 4. Raw Performance
        raw_prob = get_success_probability(optimized_circuit, secret_string, noise_model)

        # 5. ZNE Mitigation
        sanitizer = QSanitizer(mitigation_method="ZNE")
        folded_circuits = sanitizer.refine(optimized_circuit)
        
        scale_factors = []
        noisy_probs = []
        for scale, folded_circ in folded_circuits.items():
            prob = get_success_probability(folded_circ, secret_string, noise_model)
            scale_factors.append(scale)
            noisy_probs.append(prob)

        mitigated_prob = sanitizer.richardson_extrapolate(noisy_probs, scale_factors)

        # 6. Generate Dashboard
        img_path = "q_refine_dashboard_output.png"
        QRefineDashboard.generate_report(raw_prob, mitigated_prob, scale_factors, noisy_probs, output_path=img_path)

        # --- Display Results ---
        st.success("Pipeline Execution Complete!")
        
        col1, col2 = st.columns(2)
        col1.metric("Raw Accuracy (Unmitigated)", f"{raw_prob*100:.2f}%")
        col2.metric("Q-Refine Accuracy (Mitigated)", f"{mitigated_prob*100:.2f}%", f"{(mitigated_prob - raw_prob)*100:.2f}% improvement")

        st.image(img_path, use_column_width=True)

        # Add Download Button for the generated graph
        with open(img_path, "rb") as file:
            st.download_button(
                label="📥 Download Q-Refine Analytics Report (PNG)",
                data=file,
                file_name="q_refine_analytics.png",
                mime="image/png"
            )
            
        os.remove(img_path)

if sweep_btn:
    import matplotlib.pyplot as plt
    with st.spinner("Running Multi-Algorithm Noise Sweep... This might take a few seconds."):
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
            
            for name, (secret, func) in algos.items():
                if name == "Grover's Search (2-Qubit)":
                    raw_circuit = func(None)
                else:
                    raw_circuit = func(secret)
                
                optimized_circuit = transpile(raw_circuit, AerSimulator())
                prob = get_success_probability(optimized_circuit, secret, noise_model)
                results[name].append(prob)
                
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
        
        st.success("Comparative Sweep Complete!")
        st.image(sweep_img_path, use_column_width=True)
        
        with open(sweep_img_path, "rb") as file:
            st.download_button(
                label="📥 Download Comparative Sweep Graph (PNG)",
                data=file,
                file_name="comparative_sweep.png",
                mime="image/png",
                type="primary"
            )
        os.remove(sweep_img_path)
