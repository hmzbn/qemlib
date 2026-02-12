from typing import Callable, Sequence, Dict
import numpy as np

from .folding import fold_global_circuit
from .models import extrapolate


class ZeroNoiseExtrapolator:
    """
    Zero-Noise Extrapolation (ZNE) workflow.

    Given a quantum circuit and a set of noise scale factors, this class:
        1. Generates folded circuits with amplified noise,
        2. Executes them using a provided executor,
        3. Extrapolates the expectation value to the zero-noise limit.

    Args:
        scales: A sequence of odd integers >= 1 specifying noise scaling factors.
        extrapolation_method: The functional model used for extrapolation.
            Supported options are:
                - "linear"
                - "quadratic"
                - "exponential"
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

    def collect(self, circuit, executor: Callable):
        """
        Executes folded circuits at different noise scales.

        Args:
            circuit: The base quantum circuit.
            executor: A callable which takes a QuantumCircuit
                and returns a float expectation value.

        Returns:
            A NumPy array of expectation values corresponding to self.scales.
        """
        
        values = []

        for scale in self.scales:
            folded = fold_global_circuit(circuit, scale)
            val = executor(folded)
            values.append(val)

        return np.array(values)

    def extrapolate(self, values):
        return extrapolate(
            xdata=self.scales,
            ydata=values,
            method=self.method,
        )

    def run(self, circuit, executor: Callable) -> Dict:
        """
        Runs the full Zero-Noise Extrapolation workflow.

        Args:
            circuit: The base quantum circuit.
            executor: A callable which executes a circuit
                and returns an expectation value.

        Returns:
            A dictionary containing:
                - "scales": Array of noise scale factors
                - "values": Measured expectation values
                - "zne_value": Extrapolated zero-noise estimate
                - "fit_params": Parameters of the fitted model
                - "fit_function": Callable fit model
        """
        
        values = self.collect(circuit, executor)
        result = self.extrapolate(values)

        return {
            "scales": np.array(self.scales),
            "values": values,
            "zne_value": result["zero_noise_value"],
            "fit_params": result["fit_params"],
            "fit_function": result["fit_function"],
        }
