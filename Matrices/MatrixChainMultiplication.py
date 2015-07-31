import sys,time
import numpy as np

INF = sys.maxint

#How many matrices should split to the LHS of the tree for the ideal solution when multiplying matrices A_i...A_j?
def matrix_chain(d, i, j):
    n = len(d)
    N = np.zeros([n-1, n-1], dtype=np.int64)
    S = np.zeros([n-1, n-1], dtype=np.int)
    for b in range(1, n):
        for i in range(n-b-1):
            j = i + b
            N[i, j] = INF
            for k in range(i, j):
                lhs = N[i,j]
                rhs_0 = N[i,k] + N[k+1,j]
                rhs_1 = d[i] * d[k+1] * d[j+1]
                N[i,j] = min(lhs, rhs_0 + rhs_1)
                if N[i,j] != lhs:
                    S[i,j] = k
                    
    return (N, S)

#Returns the minimum number of operations possible when multiplying matrices
def matrix_chain_ops(d, i, j):
    return matrix_chain(d, i, j)[0][0, len(d)-2]

#Recursively find the correct position of the matrix in the parentheticized equation, then format it accordingly
def parenify(S, i, j):
    single_format = "A_%d"
    if i == j:
        return "A_%d" % j
    res1 = parenify(S, i, S[i,j])
    res2 = parenify(S, S[i,j]+1, j)
    return "(%s*%s)" % (res1, res2)

#Given an input [a, b, c, d, e] representing matrices of dimensions AxB, BxC, CxD, DxE..., show human-readable output
#describing the order which they should be multiplied in
def show_result(p, i=None, j=None):
    if i == None:
        i = 1
    if j == None:
        j = len(p)
    res = matrix_chain(p, i, j-1)
    expr = parenify(res[1], 0, j-2)
    print "\nThe solution %s results in %d multiplications." % (expr[1:len(expr)-1], res[0][0, j-2])
    print "\nN"
    print res[0]
    print "\nS"
    print res[1]

if __name__ == '__main__':
    show_result([30, 5, 10, 10, 8,8,18,3,2,8])