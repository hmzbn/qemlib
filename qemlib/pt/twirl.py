from qiskit import QuantumCircuit
from .pauli import random_pauli, PAULIS_CNOT, PAULIS_ECR


def apply_pauli(qc, p, qubit):
    if p == "X":
        qc.x(qubit)
    elif p == "Y":
        qc.y(qubit)
    elif p == "Z":
        qc.z(qubit)


def twirl_cx(circuit: QuantumCircuit) -> QuantumCircuit:
    """
    Apply Pauli twirling to CX gates.
    """
    new_qc = QuantumCircuit(*circuit.qregs)

    for instruction in circuit.data:
        inst = instruction.operation
        qargs = instruction.qubits
        cargs = instruction.clbits

        if inst.name == "cx":
            p1, p2, p3, p4 = random_pauli(PAULIS_CNOT)

            apply_pauli(new_qc, p1, qargs[0])
            apply_pauli(new_qc, p2, qargs[1])

            new_qc.append(instruction)

            apply_pauli(new_qc, p3, qargs[0])
            apply_pauli(new_qc, p4, qargs[1])

        elif inst.name == "ecr":
            p1, p2, p3, p4 = random_pauli(PAULIS_ECR)          

            apply_pauli(new_qc, p1, qargs[0])
            apply_pauli(new_qc, p2, qargs[1])

            new_qc.append(instruction)

            apply_pauli(new_qc, p3, qargs[0])
            apply_pauli(new_qc, p4, qargs[1])

        else:
            new_qc.append(instruction)

    return new_qc
