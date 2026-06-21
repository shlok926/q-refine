import pytest
from qiskit import QuantumCircuit
from q_refine.mitigation_engine.q_sanitizer import QSanitizer

def test_q_sanitizer_init():
    sanitizer = QSanitizer(mitigation_method="ZNE")
    assert sanitizer.mitigation_method == "ZNE"
    assert sanitizer.scale_factors == [1, 3, 5]

def test_circuit_folding():
    sanitizer = QSanitizer(mitigation_method="ZNE")
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    
    folded_circuits = sanitizer.refine(qc)
    
    assert 1 in folded_circuits
    assert 3 in folded_circuits
    assert 5 in folded_circuits
    
    assert isinstance(folded_circuits[1], QuantumCircuit)
    assert isinstance(folded_circuits[3], QuantumCircuit)
    assert isinstance(folded_circuits[5], QuantumCircuit)
    
    # Scale 3 circuit depth should be significantly larger
    assert folded_circuits[3].depth() > folded_circuits[1].depth()

def test_richardson_extrapolate():
    sanitizer = QSanitizer(mitigation_method="ZNE")
    
    # Mock data showing degraded probability as scale increases
    noisy_probs = [0.90, 0.80, 0.70]
    scales = [1, 3, 5]
    
    zero_noise_prob = sanitizer.richardson_extrapolate(noisy_probs, scales)
    
    # Expect the zero noise prob to be higher than the scale 1 prob
    assert zero_noise_prob > 0.90
    assert zero_noise_prob <= 1.05  # Sanity check
