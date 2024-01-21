from adiaframe import *


def krons(*oper_list): # Operator Kronecker delta
    if len(oper_list) == 1:
        oper_list = oper_list[0]
    return reduce(np.kron, oper_list)
def frobenius_inner(A, B): # Frobenius inner product.
    n, n2 = A.shape
    return np.trace((A.conj().T)@B)/(n)

def commute_reggio(pa:Tuple[int, int], pb:Tuple[int, int]):
    #Reggio et al, Fast Partitioning of Pauli Strings into Commuting Families for Optimal Expectation Value Measurements of Dense Operators, 2023-06-07
    nx_a, nz_a = pa
    nx_b, nz_b = pb
    
    a = bin(nx_a & nz_b).count("1")%2
    b = bin(nx_b & nz_a).count("1")%2
    return a==b
    
def commute_reggio_df(s):
    a = bin(s[0] & s[3]).count("1")%2
    b = bin(s[1] & s[2]).count("1")%2
    return a == b

def integer_order_map(int_list):
    sorted_unique = np.unique(np.array(int_list))
    return {num: idx for idx, num in enumerate(sorted_unique)}

def get_coef(x_str, z_str): 
    # i coefficient in construction of general pauli-element from XZ elements.
    n = len(x_str)
    x_str = x_str.replace("X", "1")
    x_str = x_str.replace("I", "0")
    z_str = z_str.replace("Z", "1")
    z_str = z_str.replace("I", "0")
    
    x_int = int(x_str, 2)
    z_int = int(z_str, 2)
    
    y_pos = format(x_int&z_int, f"0{n}b")
    z_pos = format((x_int|z_int) - x_int, f"0{n}b")
    x_pos = format((x_int|z_int) - z_int, f"0{n}b")

    g_str = []
    for x,y,z in zip(x_pos, y_pos, z_pos):
        if x==y and y==z:
            g_str.append("I")
        elif x== "1":
            g_str.append("X")
        elif y == "1":
            g_str.append("Y")
        else:
            g_str.append("Z")
    return 1j**y_pos.count("1"), "".join(g_str)