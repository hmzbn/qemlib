from qiskit import QuantumCircuit


def _build_mask(circuit: QuantumCircuit):
    n = circuit.num_qubits
    d = len(circuit.data)

    mask = [[0] * d for _ in range(n)]

    for col, (instruction) in enumerate(circuit.data):
        inst = instruction.operation
        qargs = instruction.qubits
        for q in qargs:
            qi = circuit.qubits.index(q)
            mask[qi][col] = 1

    return mask


def _compute_slack(mask):
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


def insert_dd_sequences(circuit: QuantumCircuit, rule):
    new_qc = circuit.copy()

    mask = _build_mask(circuit)
    slack = _compute_slack(mask)

    for moment in range(len(circuit.data)):
        inst, qargs, cargs = circuit.data[moment]

        for q in range(circuit.num_qubits):
            slack_len = slack[q][moment]

            if slack_len > 1:
                seq = rule(slack_len)

                for op in seq.data:
                    new_qc.append(op.operation, [q])

    return new_qc
