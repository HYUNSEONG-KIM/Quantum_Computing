
from pennylane.templates import ApproxTimeEvolution
import pennylane as qml
from pennylane.operation import Operation, AnyWires

from pennylane import Hamiltonian


class AdaiabaticProcess(Operation):
    num_params = 5
    num_wires = AnyWires
    par_domain = None
    
    def __init__(
        self, 
        weights,
        wires:int, 
        T:float, steps:int, 
        mu:float, Hi:Hamiltonian=None, Hf:Hamiltonian=None):
        
        self.wires = qubit_n
        self.evolve_time = T if T>0 else -T
        self.evolve_steps = int(steps) if steps >0 else int(-steps) 
        
        self.init_weight = mu
        
    @classmethod
    def from_coeff_and_basis(cls, coeffs, basis):
        return cls()
        