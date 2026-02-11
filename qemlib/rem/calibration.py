import numpy as np
from qiskit import QuantumCircuit


def build_calibration_circuits(n_qubits):
    circuits = []
    labels = []

    for i in range(2**n_qubits):
        bitstring = format(i, f"0{n_qubits}b")

        qc = QuantumCircuit(n_qubits, n_qubits)

        for q, bit in enumerate(reversed(bitstring)):
            if bit == "1":
                qc.x(q)

        qc.measure(range(n_qubits), range(n_qubits))

        circuits.append(qc)
        labels.append(bitstring)

    return circuits, labels
