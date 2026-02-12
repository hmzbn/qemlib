from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator


class EstimatorExecutor:
    """
    Executor wrapper compatible with Qiskit Estimator (V2).

    This class provides a callable interface suitable for
    Zero-Noise Extrapolation workflows.

    Args:
        backend: Qiskit backend (AerSimulator or IBM backend).
        observable: SparsePauliOp to evaluate.
        parameter_values: Optional parameter values for parameterized circuits.
        shots: Number of measurement shots.
    """

    def __init__(
        self,
        backend,
        observable,
        parameter_values=None,
        shots: int = 100_000,
    ):
        """
        Parameters
        ----------
        backend : Backend or AerSimulator
        observable : SparsePauliOp
        parameter_values : array-like or None
        shots : int
        """
        self.backend = backend
        self.observable = observable
        self.parameter_values = parameter_values

        self.estimator = Estimator(
            mode=backend,
            options={"default_shots": shots},
        )

    def __call__(self, circuit):
        """
        Execute a circuit and return expectation value.
        """

        # Transpile
        pm = generate_preset_pass_manager(
            backend=self.backend,
            optimization_level=0,
        )
        transpiled = pm.run(circuit)

        # Apply layout to observable
        observable = self.observable.apply_layout(transpiled.layout)

        # PUB (Estimator V2 format)
        pub = (
            transpiled,
            observable,
            self.parameter_values,
        )

        job = self.estimator.run([pub])
        result = job.result()[0]

        return float(result.data.evs)
