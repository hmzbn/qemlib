from qiskit import QuantumCircuit
from qemlib.zne.zne import ZeroNoiseExtrapolator


def dummy_executor(circuit):
    # Fake noise: expectation grows with depth
    return circuit.depth()


def test_zne_runs():
    qc = QuantumCircuit(1)
    qc.h(0)

    zne = ZeroNoiseExtrapolator(scales=[1, 3, 5])
    result = zne.run(qc, dummy_executor)

    assert "zne_value" in result
    assert len(result["values"]) == 3
