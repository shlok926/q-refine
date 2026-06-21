import pytest
from qiskit import QuantumCircuit
from q_refine.circuits.bv import bernstein_vazirani
from q_refine.circuits.simon import simon_algorithm
from q_refine.circuits.grover import grover_algorithm
from q_refine.circuits.qft import qft_benchmark_circuit
from q_refine.circuits.qnn import generate_trained_qnn

def test_bernstein_vazirani():
    qc = bernstein_vazirani("101")
    assert isinstance(qc, QuantumCircuit)
    assert qc.num_qubits == 4

def test_simon_algorithm():
    qc = simon_algorithm("11")
    assert isinstance(qc, QuantumCircuit)
    assert qc.name == "Simon"
    assert qc.num_qubits == 4

def test_grover_algorithm():
    qc = grover_algorithm()
    assert isinstance(qc, QuantumCircuit)
    assert qc.num_qubits == 2

def test_qft_circuit():
    qc = qft_benchmark_circuit(3)
    assert isinstance(qc, QuantumCircuit)
    assert qc.name == "QFT"
    assert qc.num_qubits == 3

def test_generate_trained_qnn():
    qc = generate_trained_qnn(num_qubits=3, num_layers=1)
    assert isinstance(qc, QuantumCircuit)
    assert qc.num_qubits == 3
