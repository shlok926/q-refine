from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="aMpPMnUXYYcAVkRRK1tBL9iUrAodripbha-zVnf3CF8K",
    overwrite=True
)

print("API key saved successfully")