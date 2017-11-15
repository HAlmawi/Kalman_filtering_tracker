import math

def norm_vector(v):
    sum = 0
    for num in v:
        sum = sum + pow(num,2)
    return math.sqrt(sum)

def transpose_matrix(matrix):
    transposed_matrix = [[0 for x in range(len(matrix))] for y in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            transposed_matrix[j][i] = matrix[i][j]
    return transposed_matrix

def matrix_multiply(a,b):
    result = [[0 for x in range(len(a))] for y in range(len(b[0]))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] = a[i][k]*b[k][j]
    return result

def matrix_addition(a,b):


def quaterProd(a,b):
    ab = [0]*4
    ab[0] = a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3]
    ab[1] = a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2]
    ab[2] = a[0]*b[2] - a[1]*b[3] + a[2]*b[0] + a[3]*b[1]
    ab[3] = a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + a[3]*b[0]
    return ab

def quaterConj(a):
    result = [0]*4
    result[0] = a[0]
    result[1] = -1*a[1]
    result[2] = -1*a[2]
    result[3] = -1*a[3]
    return result