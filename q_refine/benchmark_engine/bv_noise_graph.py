from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import matplotlib.pyplot as plt

def bernstein_vazirani(secret_string):
    n = len(secret_string)
    qc = QuantumCircuit(n + 1, n)

    qc.x(n)
    qc.h(n)

    for i in range(n):
        qc.h(i)

    for i, bit in enumerate(secret_string):
        if bit == '1':
            qc.cx(i, n)

    for i in range(n):
        qc.h(i)

    qc.measure(range(n), range(n))
    return qc


def create_noise_model(p):
    noise_model = NoiseModel()
    error_1q = depolarizing_error(p, 1)
    error_2q = depolarizing_error(p, 2)

    noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x'])
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])
    return noise_model


# -------- Experiment --------
secret = "1011"
shots = 1024
noise_levels = [0.0, 0.01, 0.05, 0.10]
success_probs = []

for p in noise_levels:
    circuit = bernstein_vazirani(secret)
    noise_model = create_noise_model(p)
    backend = AerSimulator(noise_model=noise_model)
    result = backend.run(circuit, shots=shots).result()
    counts = result.get_counts()

    measured = max(counts, key=counts.get)
    success_prob = counts[measured] / shots
    success_probs.append(success_prob)

# -------- Robustness Score --------
# Area under curve approximation (simple average)
robustness_score = sum(success_probs) / len(success_probs)

print("Noise levels:", noise_levels)
print("Success probabilities:", success_probs)
print("Robustness Score:", round(robustness_score, 3))

# -------- Plot --------
plt.figure()
plt.plot(noise_levels, success_probs, marker='o')
plt.xlabel("Noise Probability (p)")
plt.ylabel("Success Probability")
plt.title("BV Algorithm Robustness under Depolarizing Noise")
plt.grid(True)
plt.show()
