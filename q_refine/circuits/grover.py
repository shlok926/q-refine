from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer


def grover_algorithm():
    qc = QuantumCircuit(2, 2)

    # Step 1: Initialize superposition
    qc.h([0, 1])

    # Step 2: Oracle (mark |11>)
    qc.cz(0, 1)

    # Step 3: Diffusion operator
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])

    # Step 4: Measurement
    qc.measure([0, 1], [0, 1])

    return qc


# -------- RUN --------
circuit = grover_algorithm()

# Save circuit diagram
circuit_drawer(circuit, output="mpl", filename="grover_circuit.png")

# Run simulation
backend = AerSimulator()
result = backend.run(circuit, shots=1024).result()
counts = result.get_counts()

print("Grover measurement result:", counts)
