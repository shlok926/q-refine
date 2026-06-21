import streamlit as st
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

st.set_page_config(page_title="Circuit Sandbox", layout="wide", page_icon="🧪")

st.title("🧪 Quantum Circuit Sandbox")
st.markdown("Build your own basic quantum circuits or explore pre-built algorithms to understand how gates manipulate quantum states.")

# --- UI Configuration ---
st.sidebar.header("Sandbox Configuration")
mode = st.sidebar.radio("Select Mode", ["Custom Circuit Builder", "Explore Algorithms"])

if mode == "Custom Circuit Builder":
    num_qubits = st.sidebar.selectbox("Number of Qubits", [1, 2, 3])
    
    st.subheader(f"Building a {num_qubits}-Qubit Circuit")
    
    # Initialize session state for circuit building
    if 'gates' not in st.session_state or st.session_state.get('num_qubits') != num_qubits:
        st.session_state.gates = []
        st.session_state.num_qubits = num_qubits

    # Gate selection UI
    col1, col2, col3 = st.columns(3)
    
    with col1:
        available_gates = ["H (Hadamard)", "X (NOT)", "Y", "Z"]
        if num_qubits > 1:
            available_gates.extend(["CX (CNOT)", "CZ"])
        gate_type = st.selectbox("Select Gate", available_gates)
    
    with col2:
        target_q = st.selectbox("Target Qubit", range(num_qubits))
        
    with col3:
        if gate_type in ["CX (CNOT)", "CZ"]:
            control_options = [q for q in range(num_qubits) if q != target_q]
            control_q = st.selectbox("Control Qubit", control_options) if control_options else None
        else:
            control_q = None

    if st.button("Add Gate"):
        if gate_type in ["CX (CNOT)", "CZ"] and control_q is None:
            st.error("Need at least 2 qubits to use this gate!")
        else:
            st.session_state.gates.append({
                "type": gate_type.split()[0],
                "target": target_q,
                "control": control_q
            })
            st.success(f"Added {gate_type} on target qubit {target_q}")

    if st.button("Clear Circuit"):
        st.session_state.gates = []
        st.rerun()

    # Build the Qiskit Circuit
    qc = QuantumCircuit(num_qubits, num_qubits)
    for g in st.session_state.gates:
        if g["type"] == "H": qc.h(g["target"])
        elif g["type"] == "X": qc.x(g["target"])
        elif g["type"] == "Y": qc.y(g["target"])
        elif g["type"] == "Z": qc.z(g["target"])
        elif g["type"] == "CX": qc.cx(g["control"], g["target"])
        elif g["type"] == "CZ": qc.cz(g["control"], g["target"])
    
    qc.measure(range(num_qubits), range(num_qubits))

    # Display Circuit
    st.markdown("### Circuit Diagram")
    try:
        fig, ax = plt.subplots()
        circuit_drawer(qc, output='mpl', ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.text(qc.draw(output='text'))
        st.warning("Install 'pylatexenc' for graphical circuit diagrams.")

    # Simulation
    st.markdown("### Simulation Result (Ideal)")
    if st.button("Run Simulation"):
        backend = AerSimulator()
        result = backend.run(qc, shots=1024).result()
        counts = result.get_counts()
        st.bar_chart(counts)

else:
    # Algorithm Explorer
    from q_refine.circuits.bv import bernstein_vazirani
    from q_refine.circuits.grover import grover_algorithm
    
    algo = st.selectbox("Select Algorithm", ["Bernstein-Vazirani", "Grover's Search (2 Qubit)"])
    
    if algo == "Bernstein-Vazirani":
        secret = st.text_input("Enter Secret String", "101")
        safe_secret = ''.join([c for c in secret if c in ['0', '1']])
        if not safe_secret: safe_secret = "1"
        qc = bernstein_vazirani(safe_secret)
        st.markdown(f"**Goal:** Find the hidden bitstring `{safe_secret}` in exactly 1 query using phase kickback.")
    else:
        qc = grover_algorithm()
        st.markdown("**Goal:** Find the marked state `|11>` with high probability using amplitude amplification.")

    st.markdown("### Circuit Diagram")
    try:
        fig, ax = plt.subplots()
        circuit_drawer(qc, output='mpl', ax=ax)
        st.pyplot(fig)
    except:
        st.text(qc.draw(output='text'))
