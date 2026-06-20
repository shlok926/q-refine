from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

def bernstein_vazirani(secret):
    n = len(secret)
    qc = QuantumCircuit(n + 1, n)

    qc.x(n)
    qc.h(n)

    for i in range(n):
        qc.h(i)

    for i, bit in enumerate(secret):
        if bit == "1":
            qc.cx(i, n)

    for i in range(n):
        qc.h(i)

    qc.measure(range(n), range(n))
    return qc


secret = "1011"
qc = bernstein_vazirani(secret)

service = QiskitRuntimeService()
backend = service.least_busy(simulator=False, operational=True)

print("Using backend:", backend.name)

qc = transpile(qc, backend)

sampler = Sampler(backend)
job = sampler.run([qc], shots=512)
result = job.result()

counts = result[0].data.c.get_counts()

print("Secret string:", secret)
print("Real hardware counts:", counts)
