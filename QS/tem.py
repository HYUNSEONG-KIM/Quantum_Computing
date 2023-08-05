import numpy as np

def diff_matrix_three_point(n, t="f", step_size=1/2):
    M = np.zeros(shape=(n,n))
    i, j = np.indices(M.shape)

    if t =="f":
        M[i==j] = -3
        M[i == j-1] = 4
        M[i == j-2] = -1
    elif t == "b":
        M[i==j] = 3
        M[i == j+1] = -4
        M[i == j+2] = 1
    elif t =="c":
        M[i==j+1] = -1
        M[i==j-1] = 1
    else:
        M[i==j+1] = -1
        M[i==j-1] = 1

        # Forward
        M[0, 0 ] = -3
        M[0, 1 ] = 4
        M[0, 2 ] = -1
        # Backward
        M[n-1, n-1 -2 ] = 1
        M[n-1, n-1 -1 ] = -4
        M[n-1, n-1 ]    = 3
    return M/(2*step_size)