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
    print(zizj(3, 0, 1))
    print(zizj(2, 0, 1))
    print(zizj(5, 2, 3))