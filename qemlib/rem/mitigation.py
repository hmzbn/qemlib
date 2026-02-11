import numpy as np


def calibration_matrix_from_counts(counts_list, labels):
    dim = len(labels)
    M = np.zeros((dim, dim))

    for col, counts in enumerate(counts_list):
        shots = sum(counts.values())

        for bitstring, c in counts.items():
            row = labels.index(bitstring)
            M[row, col] = c / shots

    return M


def invert_calibration_matrix(M):
    return np.linalg.pinv(M)

def mitigate_counts(counts, Minv, labels):
    dim = len(labels)
    vec = np.zeros(dim)

    shots = sum(counts.values())

    for bitstring, c in counts.items():
        idx = labels.index(bitstring)
        vec[idx] = c / shots

    mitigated = Minv @ vec
    mitigated = np.clip(mitigated, 0, 1)
    mitigated /= mitigated.sum()

    return dict(zip(labels, mitigated))
