# General imports
import numpy as np

# Pre-defined ansatz circuit and operator class for Hamiltonian
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp

# SciPy minimizer routine
from scipy.optimize import minimize

# Plotting functions
import matplotlib.pyplot as plt

# Qiskit 
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import EstimatorV2 as Estimator


data = {
    "history": []
}


if __name__ == "__main__":
    pass