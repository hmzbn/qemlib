from .insertion import insert_dd_sequences
from .seq import xx


def run_dd(circuit, executor, sequence=xx, trials=1):
    values = []

    for _ in range(trials):
        dd_circuit = insert_dd_sequences(circuit, sequence)
        values.append(executor(dd_circuit))

    return sum(values) / len(values), values
