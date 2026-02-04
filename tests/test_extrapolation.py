import numpy as np
from qemlib.zne.models import extrapolate


def test_linear_extrapolation_exact():
    x = np.array([1, 3, 5])
    y = 2 * x + 1

    result = extrapolate(x, y, method="linear")

    assert abs(result["zero_noise_value"] - 1.0) < 1e-6
