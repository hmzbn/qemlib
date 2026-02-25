from qiskit import QuantumCircuit
from .seq import SEQUENCES

def _build_mask(circuit: QuantumCircuit):
    """
    Build a qubit-moment activity mask.
    """
    n = circuit.num_qubits
    d = len(circuit.data)

    mask = [[0] * d for _ in range(n)]

    for col, instruction in enumerate(circuit.data):
        for q in instruction.qubits:
            qi = circuit.qubits.index(q)
            mask[qi][col] = 1

    return mask


def _compute_slack(mask):
    """
    Compute slack windows per qubit.
    """
    n = len(mask)
    d = len(mask[0])

    slack = [[0] * d for _ in range(n)]

    for q in range(n):
        c = 0
        while c < d:
            if mask[q][c] == 0:
                length = 0
                start = c
                
                while c < d and mask[q][c] == 0:
                    length += 1
                    c += 1
                    
                slack[q][start] = length
            else:
                c += 1

    return slack



def insert_dd_sequences(circuit: QuantumCircuit, sequence_name: str):
    """
    Insert DD sequences inside idle windows of a circuit.

    The DD sequence is repeated to fill the slack windows.
    Partial slack is left idle if it cannot fit a full block.

    Args:
        circuit: QuantumCircuit
        sequence_name: str, must exist in SEQUENCES

    Returns:
        QuantumCircuit with DD inserted
    """

    if sequence_name not in SEQUENCES:
        raise ValueError(f"Unknown sequence {sequence_name}")

    block_fn, block_length = SEQUENCES[sequence_name]

    n_qubits = circuit.num_qubits
    d = len(circuit.data)

    # Build qubit-moment activity mask
    mask = [[0] * d for _ in range(n_qubits)]
    for col, instruction in enumerate(circuit.data):
        for q in instruction.qubits:
            qi = circuit.qubits.index(q)
            mask[qi][col] = 1

    # Compute slack windows per qubit
    slack = [[0] * d for _ in range(n_qubits)]
    for q in range(n_qubits):
        c = 0
        while c < d:
            if mask[q][c] == 0:
                start = c
                length = 0
                while c < d and mask[q][c] == 0:
                    length += 1
                    c += 1
                slack[q][start] = length
            else:
                c += 1

    # New circuit with same qregs/cregs
    new_qc = QuantumCircuit(*circuit.qregs, *circuit.cregs)

    # Iterate over the original circuit and insert DD in idle windows
    for col, instruction in enumerate(circuit.data):
        inst, qargs, cargs = instruction.operation, instruction.qubits, instruction.clbits

        for q in range(n_qubits):
            if slack[q][col] >= block_length:
                num_blocks = slack[q][col] // block_length
                for _ in range(num_blocks):
                    block = block_fn()
                    for gate in block.data:
                        new_qc.append(gate.operation, [q])
                slack[q][col] -= num_blocks * block_length  # update remaining slack

        # Append the original instruction
        new_qc.append(inst, qargs, cargs)

    return new_qc
