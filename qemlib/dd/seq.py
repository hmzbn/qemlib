from qiskit import QuantumCircuit


def xx(slack_length: int) -> QuantumCircuit:
    qc = QuantumCircuit(1)
    for _ in range(slack_length // 2):
        qc.x(0)
        qc.x(0)
    return qc


def xp_xm(slack_length: int) -> QuantumCircuit:
    qc = QuantumCircuit(1)
    for _ in range(slack_length // 2):
        qc.x(0)
        qc.rx(-3.141592653589793, 0)
    return qc


def xy4(slack_length: int) -> QuantumCircuit:
    qc = QuantumCircuit(1)
    base = ["x", "y", "x", "y"]

    for i in range(min(slack_length, 4)):
        getattr(qc, base[i])(0)

    return qc
