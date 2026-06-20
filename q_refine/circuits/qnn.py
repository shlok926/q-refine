from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
import numpy as np

def generate_trained_qnn(num_qubits: int, num_layers: int = 2) -> QuantumCircuit:
    """
    Generates a Parameterized Quantum Circuit (PQC) which forms the backbone
    of Quantum Neural Networks (QNNs) and VQE algorithms.
    
    For benchmarking purposes, we return a 'trained' circuit where parameters
    are already bound to optimal values (simulating a converged AI model).
    """
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # Create parameters for our QNN layers
    num_params = num_qubits * (num_layers + 1)
    params = ParameterVector('theta', num_params)
    param_idx = 0
    
    # Layer 0 (Input features / Initial Rotations)
    for i in range(num_qubits):
        qc.ry(params[param_idx], i)
        param_idx += 1
        
    # Hidden Layers (Entanglement + Rotations)
    for layer in range(num_layers):
        # Entanglement
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)
        qc.cx(num_qubits - 1, 0) # Ring connection
        
        # Rotations
        for i in range(num_qubits):
            qc.rz(params[param_idx], i)
            param_idx += 1
            
    # Measure all qubits
    qc.measure(range(num_qubits), range(num_qubits))
    
    # To benchmark this, we bind it to a fixed set of "trained" weights.
    # We choose weights such that the circuit highly favors the state |00...0>
    # (By setting angles close to 0 or 2*pi)
    np.random.seed(42)
    # Give it small random angles near 0 so the |000> state is highly probable.
    trained_weights = np.random.normal(0, 0.1, num_params)
    
    bound_qnn = qc.assign_parameters({params: trained_weights})
    return bound_qnn
