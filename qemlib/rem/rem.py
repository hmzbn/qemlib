from .calibration import build_calibration_circuits
from .mitigation import calibration_matrix_from_counts, invert_calibration_matrix, mitigate_counts


def run_rem(executor, n_qubits):
    cal_circuits, labels = build_calibration_circuits(n_qubits)

    counts_list = [executor(qc) for qc in cal_circuits]

    M = calibration_matrix_from_counts(counts_list, labels)
    Minv = invert_calibration_matrix(M)

    def rem_executor(circuit):
        counts = executor(circuit)
        return mitigate_counts(counts, Minv, labels)

    return rem_executor, M
