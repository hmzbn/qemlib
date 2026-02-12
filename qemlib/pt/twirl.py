from qiskit import QuantumCircuit
from typing import Optional
import random

from .pauli import random_pauli


def apply_pauli(qc: QuantumCircuit, label: str, qubit):
    """Applies a single-qubit Pauli gate if not identity."""
    if label == "X":
        qc.x(qubit)
    elif label == "Y":
        qc.y(qubit)
    elif label == "Z":
        qc.z(qubit)
    # "I" → do nothing


def twirl_circuit(
    circuit: QuantumCircuit,
    seed: Optional[int] = None,
) -> QuantumCircuit:
    """
    Applies Pauli twirling to supported two-qubit gates.

    Currently supports:
        - CX
        - ECR

    Args:
        circuit: Input quantum circuit.
        seed: Optional seed for reproducibility.

    Returns:
        A new QuantumCircuit with Pauli twirling applied.
    """
    rng = random.Random(seed) if seed is not None else None

    new_qc = QuantumCircuit(*circuit.qregs, *circuit.cregs)

    for instruction in circuit.data:
        inst = instruction.operation
        qargs = instruction.qubits
        cargs = instruction.clbits
        
        if inst.name in ("cx", "ecr"):

            p1, p2, p3, p4 = random_pauli(inst.name, rng)

            apply_pauli(new_qc, p1, qargs[0])
            apply_pauli(new_qc, p2, qargs[1])

            new_qc.append(inst, qargs, cargs)

            apply_pauli(new_qc, p3, qargs[0])
            apply_pauli(new_qc, p4, qargs[1])

        else:
            new_qc.append(inst, qargs, cargs)

    return new_qc
