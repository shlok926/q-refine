import streamlit as st
import numpy as np
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from q_refine.circuits.qnn import generate_trained_qnn
from q_refine.circuits.bv import bernstein_vazirani
from q_refine.circuits.grover import grover_algorithm
from q_refine.mitigation_engine.q_sanitizer import QSanitizer
from q_refine.mitigation_engine.topology_optimizer import TopologyOptimizer
from q_refine.benchmark_engine.hardware_profiler import HardwareProfiler
from q_refine.core.dashboard import QRefineDashboard
from qiskit import transpile
from navigation import render_sidebar
import os

st.set_page_config(page_title="Q-Refine Dashboard", layout="wide", page_icon="⚛️")
st.session_state["current_page"] = "Dashboard"

# Render Custom Sidebar
render_sidebar()

st.title("⚛️ Q-Refine: Quantum AI Robustness Benchmark")
st.markdown("An enterprise-grade platform for testing and mitigating hardware noise in Quantum AI circuits using Zero-Noise Extrapolation (ZNE).")

st.divider()

# --- Feature Configuration ---
st.header("Pipeline Configuration")
col_c, col_h = st.columns(2)

with col_c:
    st.subheader("1. Quantum Circuit")
    circuit_type = st.selectbox("Select Circuit", ["Quantum Neural Network (QNN)", "Bernstein-Vazirani", "Grover's Search (2-Qubit)"])
    
    if circuit_type == "Bernstein-Vazirani":
        custom_secret = st.text_input("Enter Secret Bitstring (Real Data Input)", "1011")
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

run_btn = st.button("Run Q-Refine Pipeline 🚀", type="primary", use_container_width=True)

# --- Core Logic ---
def get_success_probability(circuit, secret, noise_model):
    backend = AerSimulator(noise_model=noise_model)
    result = backend.run(circuit, shots=2000).result()
    counts = result.get_counts()
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
