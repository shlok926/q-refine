import streamlit as st
import sys
import os

# Ensure navigation module is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from navigation import render_sidebar

st.set_page_config(page_title="Q-Refine Academy", layout="wide", page_icon="🎓")
st.session_state["current_page"] = "Academy"
render_sidebar()

st.title("🎓 Q-Refine Academy: Learnings & Concepts")
st.markdown("Welcome to the Academy! Here you will learn the core concepts behind Quantum Computing, Hardware Noise, and Error Mitigation.")

st.divider()

# --- Section 1: Quantum Basics ---
st.header("1. The Quantum Advantage")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Superposition")
    st.write("""
    Unlike classical bits that are either `0` or `1`, qubits can exist in a **Superposition** of both states simultaneously until measured.
    This allows quantum computers to process massive amounts of possibilities at the same time.
    """)
with col2:
    st.subheader("Entanglement")
    st.write("""
    **Entanglement** links qubits together. If two qubits are entangled, the state of one instantly dictates the state of the other, no matter the distance.
    This provides the exponential scaling power of quantum algorithms.
    """)

st.divider()

# --- Section 2: Hardware Noise ---
st.header("2. The Problem: Quantum Hardware Noise")
st.write("Current Quantum Processing Units (QPUs) belong to the NISQ (Noisy Intermediate-Scale Quantum) era. They suffer from severe errors:")

st.info("**T1 Relaxation Time:** The time it takes for a qubit to lose its energy and fall from `|1>` back to `|0>`.")
st.warning("**T2 Dephasing Time:** The time it takes for a qubit to lose its phase (its superposition state becomes randomized).")
st.error("**Readout Error:** The probability that a `0` is mistakenly measured as a `1`, or vice versa, at the very end of the circuit.")

st.write("In Q-Refine, our **Hardware Profiler** pulls these exact metrics from real IBM Digital Twins to simulate realistic noise.")

st.divider()

# --- Section 3: Q-Refine Error Mitigation ---
st.header("3. The Solution: Zero-Noise Extrapolation (ZNE)")
st.write("Q-Refine uses a proprietary **Zero-Noise Extrapolation (ZNE)** engine to mathematically eliminate errors without requiring extra physical qubits.")

st.markdown("""
### How ZNE Works:
1. **Global Circuit Folding:** We intentionally make the circuit *worse* by folding it (adding identity pairs like $G G^\dagger$) to increase the noise by known scale factors (e.g., 1x, 3x, 5x).
2. **Measurement:** We run the circuit at these different noise levels and plot the success probability.
3. **Richardson Extrapolation:** We fit a mathematical curve to these noisy points and trace the curve backwards to **Scale = 0** (Zero Noise).

This allows Q-Refine to predict the exact accurate answer, even on extremely noisy hardware!
""")

st.divider()

st.markdown("<div align='center'>Made with ❤️ for Quantum Computing Innovation</div>", unsafe_allow_html=True)
