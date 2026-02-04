from qiskit import QuantumCircuit


def fold_global_circuit(circuit: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """
    Perform global circuit folding for Zero-Noise Extrapolation (ZNE).

    Parameters
    ----------
    circuit : QuantumCircuit
        Original quantum circuit.
    scale_factor : int
        Noise scaling factor (must be an odd integer >= 1).

    Returns
    -------
    QuantumCircuit
        Folded quantum circuit with increased noise.
    """
    if scale_factor < 1 or scale_factor % 2 == 0:
        raise ValueError("scale_factor must be an odd integer >= 1")

    if scale_factor == 1:
        return circuit.copy()

    n_repeat = (scale_factor - 1) // 2

    folded_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    folded_circuit.append(circuit, folded_circuit.qubits)

    inverse_circuit = circuit.inverse()

    for _ in range(n_repeat):
        folded_circuit.append(inverse_circuit, folded_circuit.qubits)
        folded_circuit.append(circuit, folded_circuit.qubits)

    return folded_circuit.decompose()
