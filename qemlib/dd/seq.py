from qiskit import QuantumCircuit
import numpy as np


def xx_block() -> QuantumCircuit:
    qc = QuantumCircuit(1)
    qc.x(0)
    qc.x(0)
    return qc


def xp_xm_block() -> QuantumCircuit:
    qc = QuantumCircuit(1)
    qc.x(0)
    qc.rx(-np.pi, 0)
    return qc


def xy4_block() -> QuantumCircuit:
    qc = QuantumCircuit(1)
    qc.x(0)
    qc.y(0)
    qc.x(0)
    qc.y(0)
    return qc


# Metadata
SEQUENCES = {
    "xx": (xx_block, 2),
    "xp_xm": (xp_xm_block, 2),
    "xy4": (xy4_block, 4),
}