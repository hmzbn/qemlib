from typing import Callable, Dict, List, Optional
import numpy as np

from .twirl import twirl_circuit


class PauliTwirler:
    """
    Pauli Twirling workflow.

    Replaces supported two-qubit gates with randomly twirled
    equivalents and averages the expectation value.

    Args:
        shots: Number of random twirling instances.
        seed: Optional seed for reproducibility.
    """

    def __init__(
        self,
        shots: int = 20,
        seed: Optional[int] = None,
    ):
        self.shots = shots
        self.seed = seed

    def run(
        self,
        circuit,
        executor: Callable,
    ) -> Dict:
        """
        Executes Pauli twirling and averages results.

        Args:
            circuit: Base quantum circuit.
            executor: Callable(circuit) -> float expectation value.

        Returns:
            Dictionary containing:
                - "mean": averaged expectation value
                - "values": individual twirled results
        """
        values: List[float] = []

        for i in range(self.shots):
            twirled = twirl_circuit(
                circuit,
                seed=(self.seed + i) if self.seed is not None else None,
            )
            values.append(executor(twirled))

        return {
            "mean": float(np.mean(values)),
            "values": np.array(values),
        }
