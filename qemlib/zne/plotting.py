import numpy as np
import matplotlib.pyplot as plt
from .models import extrapolate


def plot_zne(scales, values, ref_value=None, methods=("linear",)):
    plt.figure(figsize=(8, 5))
    plt.plot(scales, values, "o", label="Noisy data")

    x_plot = np.linspace(0, max(scales), 200)

    for method in methods:
        result = extrapolate(scales, values, method)
        y_plot = result["fit_function"](x_plot, *result["fit_params"])

        plt.plot(
            x_plot,
            y_plot,
            label=f"{method} → {result['zero_noise_value']:.4f}",
        )

    if ref_value is not None:
        plt.axhline(ref_value, linestyle="--", label="Reference")

    plt.axvline(0, linestyle="--", color="gray")
    plt.xlabel("Noise scale")
    plt.ylabel("Expectation value")
    plt.legend()
    plt.grid(True)
    plt.show()
