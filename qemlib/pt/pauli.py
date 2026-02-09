import random

PAULIS_CNOT = [['Z', 'Z', 'I', 'I'], ['X', 'X', 'I', 'X'], ['X', 'Y', 'Y', 'Z']]
PAULIS_ECR = [['X', 'X', 'Y', 'Y'], ['X', 'X', 'Z', 'Z'], ['I', 'I','X', 'X']]

def random_pauli(PAULIS):
    return random.choice(PAULIS)