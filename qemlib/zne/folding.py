from qiskit import QuantumCircuit


def fold_global_circuit(circuit: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """
    Applies global unitary folding to scale the noise of a quantum circuit.

    Global folding increases noise by inserting pairs of U†U operations,
    preserving the ideal unitary while amplifying physical noise.

    Args:
        circuit: The input quantum circuit to scale.
        scale_factor: An odd integer >= 1 specifying the noise scaling factor.
            A scale factor of 1 returns the original circuit.
            A scale factor of 3 produces U U† U.
            A scale factor of 5 produces U U† U U† U, etc.

    Returns:
        A new QuantumCircuit with amplified noise.

    Raises:
        ValueError: If scale_factor is not an odd integer >= 1.
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
