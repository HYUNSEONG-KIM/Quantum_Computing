import sympy as sp
from sympy.physics.quantum import TensorProduct as tp
from sympy.physics.quantum.dagger import Dagger as dag
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum import gate as gt
from sympy.physics.quantum.qapply import qapply

from functools import reduce

def combie_circuit_gate(circuit):
    return reduce(lambda x,y: x*y, circuit)

# Default Gates
Xg = sp.Matrix([[0, 1], [1,0]])
Yg = sp.Matrix([[0, complex(0, 1)], [complex(0, -1),0]])
Zg = sp.Matrix([[1, 0], [0,-1]])
Ig = sp.eye(2)
Hg = sp.Matrix([[1, 1],[1, -1]])/sp.sqrt(2)
Sg = sp.Matrix([[1, 0],[0, -complex(0,1)]])
CNOT0 = sp.Matrix([[1,0],[0,0]])
CNOT1 = sp.Matrix([[0,0],[0,1]])

def RX(theta):
    return sp.Matrix([
        [sp.cos(theta/2), complex(0,-1)*sp.sin(theta/2)],
        [complex(0,-1)*sp.sin(theta/2), sp.cos(theta/2)]
        ])
def RY(theta):
    return sp.Matrix([
        [sp.cos(theta/2), -1*sp.sin(theta/2)],
        [sp.sin(theta/2), sp.cos(theta/2)]
        ])
def RZ(theta):
    return sp.Matrix([
        [1,0],
        [0, sp.exp(complex(0,1)*theta)]
        ])
# Multi-qubit gates
def X(i, n:int):
    assert type(i) is int, "Index i must be integer." 
    assert type(n) is int, "Qubit number n must be integer."
    assert i<n, "Index must be smaller than total qubit number."
    assert i>-1, "Index must be positive integer including 0."
    glist = n*[Ig]
    glist[i] = Xg
    return tp(*glist)
def Y(i, n:int):
    assert type(i) is int, "Index i must be integer." 
    assert type(n) is int, "Qubit number n must be integer."
    assert i<n, "Index must be smaller than total qubit number."
    assert i>-1, "Index must be positive integer including 0."
    glist = n*[Ig]
    glist[i] = Yg
    return tp(*glist)
def Z(i, n:int):
    assert type(i) is int, "Index i must be integer." 
    assert type(n) is int, "Qubit number n must be integer."
    assert i<n, "Index must be smaller than total qubit number."
    assert i>-1, "Index must be positive integer including 0."
    glist = n*[Ig]
    glist[i] = Zg
    return tp(*glist)
def CNOT(i:int, j:int, n:int):
    assert i != j, "Two qubit gate must have 2 different qubit index."
    assert type(i) is int, "Index i must be integer." 
    assert type(j) is int, "Index j must be integer." 
    assert type(n) is int, "Qubit number n must be integer."
    assert i<n and j<n, "Index must be smaller than total qubit number."
    assert i>-1 and j>-1, "Index must be positive integer including 0."
    
    glist0 = n*[Ig]
    glist1 = n*[Ig]
    
    glist0[i] = CNOT0
    glist1[i] = CNOT1
    glist1[j] = Xg    
    return tp(*glist0) + tp(*glist1) 
def Uni(U, i, n:int): # Using this function for multi-qubit Rx,Ry,and Rz and arbitary single gates. 
    assert type(i) is int, "Index i must be integer." 
    assert type(n) is int, "Qubit number n must be integer."
    assert i<n, "Index must be smaller than total qubit number."
    assert i>-1, "Index must be positive integer including 0."
    glist = n*[Ig]
    glist[i] = U
    return tp(*glist)
def ArbiUnitary(sym_st):
    sy = sym_st.lower()
    a1, a2, a3, a4 = sp.symbols([f"{sy}_{i}" for i in range(1,5)])
    return sp.Matrix([[a1, a2],[a3, a4]]), (a1, a2, a3, a4)