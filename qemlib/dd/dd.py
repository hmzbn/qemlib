from .insertion import insert_dd_sequences
from .seq import xx


def run_dd(circuit, executor, sequence=xx, trials=1):
    """
    Run Dynamical Decoupling (DD) with circuit-level insertion.

    Parameters
    ----------
    circuit : QuantumCircuit
        Input circuit.
    executor : callable
        executor(circuit) -> expectation value
    sequence : callable
        DD rule function (e.g., xx, xp_xm, xy4).
        Must accept slack_length and return a 1-qubit circuit.
    trials : int
        Number of executions to average.

    Returns
    -------
    tuple
        (average_value, values_list)
    """
    
    values = []

    for _ in range(trials):
        dd_circuit = insert_dd_sequences(circuit, sequence)
        values.append(executor(dd_circuit))

    return sum(values) / len(values), values
