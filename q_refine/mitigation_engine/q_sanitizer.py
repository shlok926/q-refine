from qiskit import QuantumCircuit
import numpy as np

class QSanitizer:
    """
    Q-Sanitizer: The proprietary Error Mitigation Engine for Q-Refine.
    Built completely from scratch. Provides real-time error mitigation using
    Zero Noise Extrapolation (ZNE) via Global Circuit Folding, which is universally
    applicable to any quantum circuit, making it highly valuable for real-world researchers.
    """

    def __init__(self, mitigation_method="ZNE"):
        """
        Initialize the sanitizer.
        :param mitigation_method: "ZNE" (Zero Noise Extrapolation) is currently supported.
        """
        self.mitigation_method = mitigation_method

    def fold_circuit(self, circuit: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
        """
        Performs Global Circuit Folding. 
        If scale_factor = 3, the circuit C becomes C * C_dagger * C.
        Mathematically, C_dagger * C = Identity. So the logic is unchanged,
        but the hardware noise is artificially amplified by 3x.
        This is required for Zero Noise Extrapolation.
        """
        if scale_factor % 2 == 0 or scale_factor < 1:
            raise ValueError("Scale factor must be an odd integer >= 1 (e.g., 1, 3, 5)")
            
        if scale_factor == 1:
            return circuit.copy()
            
        # Number of times to apply the identity pair (C_dagger * C)
        n_pairs = (scale_factor - 1) // 2
        
        # We only fold the unitary part, NOT the measurements.
        # Let's extract the circuit without measurements
        folded = QuantumCircuit(*circuit.qregs, *circuit.cregs)
        
        # Extract gates (excluding measurements and barriers at the end)
        unitary_gates = []
        measurements = []
        
        for instruction in circuit.data:
            if instruction.operation.name == 'measure':
                measurements.append(instruction)
            else:
                unitary_gates.append(instruction)
                folded.append(instruction) # Base circuit C
                
        # Create inverse circuit C_dagger
        inv_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
        for instruction in reversed(unitary_gates):
            inv_instruction = instruction.replace(operation=instruction.operation.inverse())
            inv_circuit.append(inv_instruction)
            
        # Append (C_dagger * C) pairs
        for _ in range(n_pairs):
            folded.barrier()
            # Append C_dagger
            for inst in inv_circuit.data:
                folded.append(inst)
            folded.barrier()
            # Append C
            for inst in unitary_gates:
                folded.append(inst)
                
        # Re-add measurements at the very end
        folded.barrier()
        for meas in measurements:
            folded.append(meas)
            
        return folded

    def richardson_extrapolate(self, expectation_values: list, scale_factors: list) -> float:
        """
        Applies Richardson Extrapolation to estimate the expectation value
        at a noise scale of 0 (Zero Noise).
        """
        if len(expectation_values) != len(scale_factors):
            raise ValueError("Must have same number of values and scale factors")
            
        # Fit a polynomial to the (scale_factor, expectation_value) points
        # For N points, we use an (N-1) degree polynomial.
        degree = len(scale_factors) - 1
        poly = np.polyfit(scale_factors, expectation_values, degree)
        
        # Extrapolate to noise = 0 by evaluating the polynomial at x=0
        # The last term in np.polyfit output is the constant term (x=0)
        zero_noise_val = poly[-1]
        
        # Probabilities must be capped between 0 and 1
        return max(0.0, min(1.0, zero_noise_val))

    def refine(self, circuit: QuantumCircuit) -> QuantumCircuit:
        """
        The main pipeline to refine a raw circuit.
        For ZNE, it returns the folded circuits needed for mitigation.
        """
        if self.mitigation_method == "ZNE":
            # Real researchers typically use scale factors 1, 3, and 5
            scales = [1, 3, 5]
            folded_circuits = {s: self.fold_circuit(circuit, s) for s in scales}
            return folded_circuits
        else:
            raise ValueError("Unknown mitigation method.")
