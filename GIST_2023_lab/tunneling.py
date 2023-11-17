import numpy as np
from itertools import combinations, combinations_with_replacement as re_combi, product
from functools import reduce
from qiskit.quantum_info import SparsePauliOp

# basic gates
I = np.eye(2)
Z = np.array([[1, 0],[ 0, -1]])
i_v = np.array([1,1])
z_v = np.array([1, -1])


def krons(oper_list):
    return reduce(np.kron, oper_list)
def get_pauli_z_family_n_qubit(n):
    return list(map(krons, product([i_v, z_v], repeat=int(n)))), list(map(lambda x: "".join(x), product("IZ", repeat=int(n))))
def V_potential(n, data):
    assert int(2**n)==data.size, f"The data size {data.size} must be same with 2^n: {int(2**n)}."
    V_x = np.matrix(np.diag(data))
    pauli_z, z_symbol = get_pauli_z_family_n_qubit(n)
    # Hilbert-Schmidt inner product of matrices
    pauli_coefficient = np.fromiter(map(lambda x: np.trace(V_x.getH() @ np.matrix(x)), pauli_z), dtype=float) 
    return SparsePauliOp(z_symbol, pauli_coefficient)
def V_potential_from_function(n, x_i, x_f, func):
    xline = np.linspace(x_i, x_f, n, endpoint=True)
    return V_potential(n, func(xline))

#-----------------------------------------------------------------

# Opeartors
def position_operator(n):
    return np.diag(np.arange(0, n))
def momentum_operator(n):
    dia_array = (2*np.pi/(int(2**n)))* np.concatenate(
        [
            np.arange(0, int(2**(n -1)+1)), 
            int(2**(n-1)) - np.arange(int(2**(n -1)+1), int(2**n))
        ])
    return np.diag(dia_array)

# Page-Wootters

class PaW:
    """_summary_
    """
    def __init__(self):
        pass
    
    @staticmethod
    def cal_minimum_qubits(ns, dt, steps):
        """Calculate minimum number of qubits for clock register to get a desired precise clock system.

            Prototype
        Args:
            ns (int): Evolution system register
            dt (float): Evolution step unit
            steps (int): Total steps of the time evolution
        """
        T = dt*steps # total evolution
        nc = int(np.log2(steps)+1)
        return nc
        
