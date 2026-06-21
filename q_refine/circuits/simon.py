from qiskit import QuantumCircuit

def simon_algorithm(secret_string):
    """
    Generates a quantum circuit for Simon's algorithm.
    """
    n = len(secret_string)
    qc = QuantumCircuit(2*n, n, name="Simon")
    
    # Step 1: Apply H-gates to first n qubits
    for i in range(n):
        qc.h(i)
        
    qc.barrier()
    
    # Step 2: Simon's Oracle
    # Copy first register to second register
    for i in range(n):
        qc.cx(i, i+n)
        
    # Find first '1' in secret string
    j = -1
    for idx, bit in enumerate(secret_string):
        if bit == '1':
            j = idx
            break
            
    # Apply specific XORs if secret_string is not all zeros
    if j != -1:
        for i in range(n):
            if secret_string[i] == '1':
                qc.cx(j, i+n)
                
    qc.barrier()
    
    # Step 3: Apply H-gates to first n qubits
    for i in range(n):
        qc.h(i)
        
    # Step 4: Measure first n qubits
    for i in range(n):
        qc.measure(i, i)
        
    return qc
