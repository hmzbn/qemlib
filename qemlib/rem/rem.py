import numpy as np
from itertools import product
from typing import Callable, Dict
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp


# Executor
def counts_executor(backend, shots: int = 1024) -> Callable:
    """
    Creates an executor function returning counts.

    Args:
        backend: Qiskit backend
        shots: Number of shots

    Returns:
        Callable[[QuantumCircuit], Dict[str, int]]
    """
    def executor(circuit: QuantumCircuit) -> Dict[str, int]:
        job = backend.run(circuit, shots=shots)
        result = job.result()
        return result.get_counts()

    return executor


# Readout Mitigator
class ReadoutMitigator:
    """
    Global Readout Error Mitigator.

    Args:
        executor: Function returning counts dict.
        n_qubits: Number of qubits.
    """

    def __init__(self, executor: Callable, n_qubits: int):
        self.executor = executor
        self.n_qubits = n_qubits
        self.labels = ["".join(bits) for bits in product("01", repeat=n_qubits)]
        self.Minv = None

    ## Calibration
    def calibrate(self):
        """Builds and inverts confusion matrix."""
        dim = 2 ** self.n_qubits
        M = np.zeros((dim, dim))

        for i, label in enumerate(self.labels):
            qc = QuantumCircuit(self.n_qubits)

            for q, bit in enumerate(label[::-1]):
                if bit == "1":
                    qc.x(q)

            qc.measure_all()

            counts = self.executor(qc)
            shots = sum(counts.values())

            for bitstring, c in counts.items():
                bitstring = bitstring.replace(" ", "")
                j = self.labels.index(bitstring)
                M[j, i] = c / shots

        self.Minv = np.linalg.pinv(M)

    ## Mitigation
    def mitigate(self, circuit: QuantumCircuit) -> Dict[str, float]:
        """
        Executes circuit and returns mitigated probabilities.
        """
        if self.Minv is None:
            raise RuntimeError("Must call calibrate() first.")

        counts = self.executor(circuit)
        return _mitigate_counts(counts, self.Minv, self.labels)


# Internal Utilities
def _mitigate_counts(counts, Minv, labels):
    dim = len(labels)
    vec = np.zeros(dim)

    shots = sum(counts.values())

    for bitstring, c in counts.items():
        bitstring = bitstring.replace(" ", "")
        idx = labels.index(bitstring)
        vec[idx] = c / shots

    mitigated = Minv @ vec
    mitigated = np.clip(mitigated, 0, 1)
    mitigated /= np.sum(mitigated)

    return dict(zip(labels, mitigated))


def _rotate_to_measurement_basis(circuit, pauli_string):
    qc = circuit.remove_final_measurements(inplace=False)

    for i, p in enumerate(pauli_string):
        if p == "X":
            qc.h(i)
        elif p == "Y":
            qc.sdg(i)
            qc.h(i)

    qc.measure_all()
    return qc


def _expectation_from_probs(probs, pauli_string):
    exp = 0.0

    for bitstring, prob in probs.items():
        parity = 1
        for i, p in enumerate(pauli_string):
            if p == "I":
                continue

            bit = int(bitstring[len(pauli_string) - 1 - i])
            if bit == 1:
                parity *= -1

        exp += parity * prob

    return exp


# Public API
def rem_expectation(circuit: QuantumCircuit,
                    observable: SparsePauliOp,
                    mitigator: ReadoutMitigator) -> float:
    """
    Computes mitigated expectation value of a SparsePauliOp.

    Args:
        circuit: Quantum circuit (without final measurements).
        observable: SparsePauliOp observable.
        mitigator: Calibrated ReadoutMitigator.

    Returns:
        Mitigated expectation value.
    """
    total = 0.0

    for pauli, coeff in zip(observable.paulis, observable.coeffs):
        pauli_str = pauli.to_label()

        rotated = _rotate_to_measurement_basis(circuit, pauli_str)
        probs = mitigator.mitigate(rotated)

        exp_val = _expectation_from_probs(probs, pauli_str)
        total += coeff.real * exp_val

    return total
