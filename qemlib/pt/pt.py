from .twirl import twirl_cx


def run_pt(circuit, executor, shots=10):
    """
    Execute Pauli twirling with averaging.

    executor(circuit) -> expectation value
    """
    values = []

    for _ in range(shots):
        twirled = twirl_cx(circuit)
        values.append(executor(twirled))

    return sum(values) / len(values), values