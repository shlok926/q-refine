from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import matplotlib.pyplot as plt
import math

# -------- Grover Circuit --------
def grover_circuit(target):
    n = len(target)
    qc = QuantumCircuit(n, n)

    # Superposition
    for i in range(n):
        qc.h(i)

    # Oracle (phase flip)
    for i, bit in enumerate(target):
        if bit == '0':
            qc.x(i)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    for i, bit in enumerate(target):
        if bit == '0':
            qc.x(i)

    # Diffusion operator
    for i in range(n):
        qc.h(i)
        qc.x(i)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    for i in range(n):
        qc.x(i)
        qc.h(i)

    qc.measure(range(n), range(n))
    return qc


# -------- Noise Model --------
def create_noise_model(p):
    noise_model = NoiseModel()
    error_1q = depolarizing_error(p, 1)
    error_2q = depolarizing_error(p, 2)

    noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x'])
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'mcx'])
    return noise_model


# -------- Experiment --------
target = "11"          # marked state
shots = 1024
noise_levels = [0.0, 0.01, 0.05, 0.10]
success_probs = []

for p in noise_levels:
    qc = grover_circuit(target)
    noise_model = create_noise_model(p)
    backend = AerSimulator(noise_model=noise_model)
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()

    # Correct state (little-endian)
    correct = target[::-1]
    success = counts.get(correct, 0)
    success_probs.append(success / shots)

# -------- Robustness Score --------
robustness_score = sum(success_probs) / len(success_probs)

print("Noise levels:", noise_levels)
print("Success probabilities:", success_probs)
print("Robustness Score:", round(robustness_score, 3))

# -------- Plot --------
plt.figure()
plt.plot(noise_levels, success_probs, marker='o')
plt.xlabel("Noise Probability (p)")
plt.ylabel("Success Probability")
plt.title("Grover’s Algorithm Robustness under Depolarizing Noise")
plt.grid(True)
plt.show()
