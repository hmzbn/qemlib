from qiskit import QuantumCircuit

def rotate_to_measurement_basis(circuit, pauli_string):
    """
    Rotates circuit so Pauli string can be measured in Z basis.
    """
    qc = circuit.copy()

    for i, p in enumerate(pauli_string):
        if p == "X":
            qc.h(i)
        elif p == "Y":
            qc.sdg(i)
            qc.h(i)

    qc.measure_all()
    return qc

def expectation_from_probs(probs, pauli_string):
    exp = 0.0

    for bitstring, p in probs.items():
        value = 1

        for i, pauli in enumerate(pauli_string):
            if pauli == "I":
                continue

            bit = int(bitstring[::-1][i])
            value *= (1 if bit == 0 else -1)

        exp += value * p

    return exp

import numpy as np
from qiskit.quantum_info import SparsePauliOp
from .rem import run_rem
from .calibration import build_calibration_circuits 
from .mitigation import calibration_matrix_from_counts, invert_calibration_matrix


def rem_expectation(circuit, observable: SparsePauliOp, executor, num_qubits):
    """
    Compute expectation value of observable using REM.
    """
    counts_l = [executor(qc) for qc in build_calibration_circuits(num_qubits)[0]]
    labels = build_calibration_circuits(num_qubits)[1]
    cal_matrix = calibration_matrix_from_counts(counts_l, labels)
    inv_cal = invert_calibration_matrix(cal_matrix)

    total_energy = 0.0

    for pauli, coeff in zip(observable.paulis, observable.coeffs):
        pauli_str = pauli.to_label()

        rotated = rotate_to_measurement_basis(circuit, pauli_str)

        mitigated_probs = run_rem(
            executor,
            num_qubits,
            circuit
        )

        exp_val = expectation_from_probs(mitigated_probs, pauli_str)
        total_energy += coeff.real * exp_val

    return total_energy
