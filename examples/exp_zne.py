zne = ZeroNoiseExtrapolator(
    scales=[1, 3, 5],
    extrapolation_method="exponential",
)

executor = EstimatorExecutor(
    backend=backend,
    observable=hamiltonian,
    parameter_values=opt_params,
)

result = zne.run(circuit, executor)

print("ZNE value:", result["zne_value"])
