from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer


def bernstein_vazirani(secret_string):
    n = len(secret_string)
    qc = QuantumCircuit(n + 1, n)

    # Step 1: Initialize output qubit |1>
    qc.x(n)
    qc.h(n)

    # Step 2: Hadamard on input qubits
    for i in range(n):
        qc.h(i)

    # Step 3: Oracle implementation
    for i, bit in enumerate(secret_string):
        if bit == '1':
            qc.cx(i, n)

    # Step 4: Hadamard again on input qubits
    for i in range(n):
        qc.h(i)

    # Step 5: Measurement
    qc.measure(range(n), range(n))

    return qc


if __name__ == "__main__":
    # -------- RUN --------
    secret = "1011"
    circuit = bernstein_vazirani(secret)

    # Draw and save circuit diagram
    # circuit_drawer(circuit, output="mpl", filename="bv_circuit.png")

    # Run simulation
    backend = AerSimulator()
    result = backend.run(circuit, shots=1024).result()
    counts = result.get_counts()

    print("Secret string:", secret)
    print("Measurement result:", counts)
