from adiaframe import *


def krons(*oper_list): # Operator Kronecker delta
    if len(oper_list) == 1:
        oper_list = oper_list[0]
    return reduce(np.kron, oper_list)
def frobenius_inner(A, B): # Frobenius inner product.
    n, n2 = A.shape
    return np.trace((A.conj().T)@B)/(n)
