import numpy as np
from functools import reduce

I = np.matrix(
    [[1, 0],
     [0, -1]], 
    dtype=complex
    )
Z = np.matrix(
    [[1, 0],
     [0, -1]], 
    dtype=complex
    )
def krons(oper_list):
    return reduce(np.kron, oper_list)
def zizj(n, i, j):
    oper_list = n*[I]
    oper_list[i] = Z
    oper_list[j] = Z
    return krons(oper_list)

if __name__ == "__main__":
    m = np.zeros([16, 16], dtype = complex)
    m += zizj(4, 0, 1)
    m += zizj(4, 3, 2)
    m += zizj(4, 2, 3)
    m += zizj(4, 0, 3)
    print(m.real)