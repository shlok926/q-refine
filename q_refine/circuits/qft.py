import math
from qiskit import QuantumCircuit

def qft_benchmark_circuit(num_qubits=3):
    """
    Generates a Quantum Fourier Transform (QFT) followed by Inverse QFT circuit for benchmarking.
    In an ideal, noiseless scenario, the output is exactly |0...0>.
    
    Args:
        num_qubits (int): Number of qubits. Default is 3.
        
    Returns:
        QuantumCircuit: The QFT-IQFT benchmarking circuit.
    """
    qc = QuantumCircuit(num_qubits, num_qubits, name="QFT")
    
    # --- Forward QFT ---
    for j in range(num_qubits):
        qc.h(j)
        for k in range(j + 1, num_qubits):
            angle = math.pi / (2 ** (k - j))
            qc.cp(angle, k, j)
            
    for i in range(num_qubits // 2):
        qc.swap(i, num_qubits - i - 1)
        
    qc.barrier()
    
    # --- Inverse QFT ---
    for i in range(num_qubits // 2):
        qc.swap(i, num_qubits - i - 1)
        
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            angle = -math.pi / (2 ** (k - j))
            qc.cp(angle, k, j)
        qc.h(j)
        
    qc.barrier()
    
    # Measure all qubits
    for i in range(num_qubits):
        qc.measure(i, i)
        
    return qc
