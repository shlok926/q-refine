from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer


def simon_algorithm(secret_string):
    n = len(secret_string)
    qc = QuantumCircuit(2 * n, n)

    # Step 1: Hadamard on first register
    for i in range(n):
        qc.h(i)

    # Step 2: Oracle (simple simulated oracle)
    for i, bit in enumerate(secret_string):
        if bit == '1':
            qc.cx(i, i + n)

    # Step 3: Hadamard again on first register
    for i in range(n):
        qc.h(i)

    # Step 4: Measurement
    qc.measure(range(n), range(n))

    return qc


# -------- RUN --------
secret = "1011"
circuit = simon_algorithm(secret)

# Save circuit diagram
circuit_drawer(circuit, output="mpl", filename="simon_circuit.png")

# Run simulation
backend = AerSimulator()
result = backend.run(circuit, shots=1024).result()
counts = result.get_counts()

print("Secret string:", secret)
print("Measurement result:", counts)

