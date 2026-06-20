from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import matplotlib.pyplot as plt

# ---------------- Simon Circuit ----------------
def simon_circuit(secret):
    n = len(secret)
    qc = QuantumCircuit(2*n, n)

    # Hadamard on input register
    for i in range(n):
        qc.h(i)

    # Oracle construction
    for i, bit in enumerate(secret):
        if bit == '1':
            qc.cx(i, i+n)
    for i in range(n):
        qc.cx(i, i+n)

    # Hadamard again
    for i in range(n):
        qc.h(i)

    qc.measure(range(n), range(n))
    return qc


# ---------------- Noise Model ----------------
def create_noise_model(p):
    noise_model = NoiseModel()

    error_1q = depolarizing_error(p, 1)
    error_2q = depolarizing_error(p, 2)

    noise_model.add_all_qubit_quantum_error(error_1q, ['h'])
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

    return noise_model


# ---------------- Correct Success Check ----------------
def is_valid(bitstring, secret):
    """
    Check Simon condition: y · s = 0 (mod 2)
    bitstring reversed due to Qiskit little-endian
    """
    return sum(int(a) * int(b) for a, b in zip(bitstring, secret)) % 2 == 0


# ---------------- Experiment ----------------
secret = "11"
shots = 1024
noise_levels = [0.0, 0.01, 0.05, 0.10]
success_probs = []

for p in noise_levels:
    circuit = simon_circuit(secret)
    noise_model = create_noise_model(p)
    backend = AerSimulator(noise_model=noise_model)
    result = backend.run(circuit, shots=shots).result()
    counts = result.get_counts()

    # Count only VALID Simon outcomes
    success = sum(
        v for k, v in counts.items()
        if is_valid(k[::-1], secret)
    )
    success_probs.append(success / shots)

# ---------------- Robustness Score ----------------
robustness_score = sum(success_probs) / len(success_probs)

print("Noise levels:", noise_levels)
print("Success probabilities:", success_probs)
print("Robustness Score:", round(robustness_score, 3))

# ---------------- Plot ----------------
plt.figure()
plt.plot(noise_levels, success_probs, marker='o')
plt.xlabel("Noise Probability (p)")
plt.ylabel("Success Probability")
plt.title("Simon’s Algorithm Robustness under Depolarizing Noise")
plt.grid(True)
plt.show()
