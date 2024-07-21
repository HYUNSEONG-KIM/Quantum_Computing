# General imports
import numpy as np

# Pre-defined ansatz circuit and operator class for Hamiltonian
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp

from qiskit import QuantumCircuit

# SciPy minimizer routine
from scipy.optimize import minimize

# Plotting functions
import matplotlib.pyplot as plt

# Qiskit 
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import EstimatorV2 as Estimator

import time 

from qiskit_symb.quantum_info import Statevector

import tkinter as tk

class VQEFrame(tk.LabelFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)


        self.opt_param = None
        self.ansatz = None
        self.state_vector = None
        self.canvas = tk.Canvas(master=self, width=300, height=300, bg = "white")
        self.canvas.pack(side=tk.BOTTOM, fill=tk.X)
    def get_params(self, ansatz, hamiltonian, ansatz_frame):
        cost_history_dict = {
            "prev_vector": None,
            "iters": 0,
            "cost_history": [],
            "params":[]
        }
        estimator = Estimator()
        n_p = ansatz.num_parameters
        x0 = 2*np.pi * np.random.random(n_p)

        def cost_func(params, ansatz, hamiltonian, estimator):
            time.sleep(10/1000)
            pub = (ansatz, [hamiltonian], [params])
            result = estimator.run(pubs=[pub]).result()
            energy = result[0].data.evs[0]

            cost_history_dict["iters"] += 1
            cost_history_dict["prev_vector"] = params
            cost_history_dict["cost_history"].append(energy)

            print(f"Iters. done: {cost_history_dict['iters']} [Current cost: {energy}]")

            self.canvas.create_text(250, 250, 
                                    text=f"{energy:.4}",
                                    font=('Helvetica', 20), 
                                    fill="black")
            ansatz_frame.update_color_by_params(params - 2*np.round(params/(2*np.pi)) *np.pi)
            return energy
        res = minimize(
            cost_func,
            x0,
            args =  (ansatz.decompose(), hamiltonian, estimator),
            method="cobyla" # Cobyla method
        )
        self.opt_param  = res.x
        self.ansatz = ansatz
    def cal_st_vector(self):
        extracted_params = self.ansatz.parameters
        param_bindings = {param: value for param, value in zip(extracted_params, self.opt_param)}
        qc = self.ansatz.bind_parameters(param_bindings)
        st_vec = Statevector(qc)
        self.state_vector = st_vec


 