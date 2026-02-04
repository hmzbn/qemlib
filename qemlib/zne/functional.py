from .folding import fold_global_circuit


def run_zne(circuit, scales, executor):
    """
    Run ZNE by folding circuits and executing them.

    executor(scale, folded_circuit) → expectation value
    """
    values = []

    for scale in scales:
        folded = fold_global_circuit(circuit, scale)
        values.append(executor(scale, folded))

    return scales, values
