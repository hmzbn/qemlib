import random
from typing import List, Optional


PAULIS = {
    "cx": [
        ["Z", "Z", "I", "I"],
        ["X", "X", "I", "X"],
        ["X", "Y", "Y", "Z"],
    ],
    "ecr": [
        ["X", "X", "Y", "Y"],
        ["X", "X", "Z", "Z"],
        ["I", "I", "X", "X"],
    ],
}


def random_pauli(
    gate_name: str,
    rng: Optional[random.Random] = None,
) -> List[str]:
    """
    Returns a random Pauli twirling pattern for a given gate.

    Args:
        gate_name: Name of the two-qubit gate ("cx", "ecr").
        rng: Optional random generator for reproducibility.

    Returns:
        A list of 4 Pauli labels.
    """
    if gate_name not in PAULIS:
        raise ValueError(f"No Pauli set defined for gate '{gate_name}'")

    rng = rng or random
    return rng.choice(PAULIS[gate_name])
