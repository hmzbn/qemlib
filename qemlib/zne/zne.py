from typing import Callable, Sequence, Dict
import numpy as np

from .folding import fold_global_circuit
from .models import extrapolate


class ZeroNoiseExtrapolator:
    """
    Class-based Zero-Noise Extrapolation (ZNE).
    """

    def __init__(
        self,
        scales: Sequence[int],
        extrapolation_method: str = "linear",
    ):
        self.scales = list(scales)
        self.method = extrapolation_method

        if any(s % 2 == 0 or s < 1 for s in self.scales):
            raise ValueError("Noise scales must be odd integers >= 1")

    def run(
        self,
        circuit,
        executor: Callable,
    ) -> Dict:
        """
        Run ZNE.

        Parameters
        ----------
        circuit : QuantumCircuit
            Base quantum circuit.
        executor : callable
            Function that executes a circuit and returns expectation value.

        Returns
        -------
        dict
            {
                "scales": [...],
                "values": [...],
                "zne_value": float,
                "fit_params": tuple
            }
        """
        values = []

        for scale in self.scales:
            folded = fold_global_circuit(circuit, scale)
            val = executor(folded)
            values.append(val)

        result = extrapolate(
            xdata=self.scales,
            ydata=values,
            method=self.method,
        )

        return {
            "scales": np.array(self.scales),
            "values": np.array(values),
            "zne_value": result["zero_noise_value"],
            "fit_params": result["fit_params"],
            "fit_function": result["fit_function"],
        }
