import streamlit as st
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer
import io
import sys
import os

# Ensure navigation module is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from navigation import render_sidebar

st.set_page_config(page_title="Shor's Explorer", layout="wide", page_icon="💻")
st.session_state["current_page"] = "Shor's Explorer"
render_sidebar()

st.title("💻 Shor's Algorithm & QFT Explorer")
st.markdown("Explore the algorithm that breaks RSA encryption. Dive into the Quantum Fourier Transform (QFT) and a simplified version of Shor's Algorithm used to factor $N=15$.")

st.divider()

mode = st.radio("Select Advanced Circuit", ["Quantum Fourier Transform (QFT)", "Shor's Factoring (N=15, a=7)"], horizontal=True)

if mode == "Quantum Fourier Transform (QFT)":
    st.header("1. Quantum Fourier Transform (QFT)")
    st.markdown("The **QFT** is the quantum analogue of the discrete Fourier transform. It is the core engine behind Shor's Algorithm, extracting the hidden period of a function.")
    
    num_q = st.slider("Number of Qubits for QFT", min_value=2, max_value=8, value=4)
    
    # Generate and fully decompose the QFT circuit to show internal gates
    qft_circuit = QFT(num_q)
    qc = qft_circuit.decompose()
    
    st.markdown("### QFT Circuit Diagram")
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        circuit_drawer(qc, output='mpl', ax=ax)
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        st.download_button("📥 Download QFT Circuit", data=buf.getvalue(), file_name=f"QFT_{num_q}_qubits.png", mime="image/png")
    except Exception as e:
        st.text(qc.draw(output='text'))
        st.warning("Please install pylatexenc for HD graphics.")

else:
    st.header("2. Shor's Algorithm: Factoring 15")
    st.markdown("This is a highly optimized, simplified version of Shor's Algorithm designed specifically to factor **15 (3 × 5)** using the coprime **a=7**. It uses 2 counting qubits and 4 target qubits (Total: 6 Qubits).")
    
    # Build Shor's N=15, a=7
    qc = QuantumCircuit(6, 2)
    
    # 1. Initialize counting qubits in superposition
    qc.h(0)
    qc.h(1)
    
    # 2. Initialize target qubits to |1> (Qiskit ordering: q2, q3, q4, q5. Let's set q2 to 1)
    qc.x(2)
    
    # 3. Controlled Modular Exponentiation (7^x mod 15)
    # Controlled-7 mod 15 (Target Qubits: 2,3,4,5. Control: 0)
    qc.cx(0, 3)
    qc.cx(0, 4)
    qc.cx(0, 5)
    
    # Controlled-4 mod 15 (Target Qubits: 2,3,4,5. Control: 1)
    qc.cx(1, 2)
    qc.cx(1, 4)
    
    # 4. Inverse QFT on counting qubits
    qc.append(QFT(2, inverse=True).to_gate(label="IQFT"), [0, 1])
    
    # 5. Measure
    qc.measure([0, 1], [0, 1])
    
    st.markdown("### Shor's Circuit Diagram")
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        circuit_drawer(qc, output='mpl', ax=ax)
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        st.download_button("📥 Download Shor's Circuit", data=buf.getvalue(), file_name="shors_15.png", mime="image/png")
    except Exception as e:
        st.text(qc.draw(output='text'))
    
    st.markdown("### Run Simulation")
    if st.button("Simulate Shor's Algorithm 🚀"):
        backend = AerSimulator()
        from qiskit import transpile
        qc_transpiled = transpile(qc, backend)
        result = backend.run(qc_transpiled, shots=1024).result()
        counts = result.get_counts()
        st.bar_chart(counts)
        st.success("Simulation Complete! The peaks represent the hidden period $r=4$. From this period, the factors $3$ and $5$ can be classically computed!")
