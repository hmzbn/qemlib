def test_global_folding_scale_1():
    qc = QuantumCircuit(1)
    qc.h(0)

    folded = fold_global_circuit(qc, 1)
    assert folded == qc
