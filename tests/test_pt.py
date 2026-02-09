from qiskit import QuantumCircuit
from qemlib.pt import twirl_cx


def test_twirl_preserves_qubits():
    qc = QuantumCircuit(2)
    qc.cx(0, 1)

    twirled = twirl_cx(qc)

    assert twirled.num_qubits == qc.num_qubits
