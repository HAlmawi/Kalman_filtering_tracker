import math

# norm_vector(v): get the norm of the vector -> sqrt(x^2 + x2^2+ ....)
# Input:
# 1- v: the vector to be normalized
# Output:
# 1- the norm of the vector
def norm_vector(v):
    sum = 0
    for i in range(len(v)):
        for j in range(len(v[0])):
            sum = sum + pow(v[i][j],2)
    return math.sqrt(sum)

# transpose_matrix(matrix): transpose the given matrix
# Input:
# 1- matrix: the matrix to be transposed
# Output:
# 1- the tranposed matrix
def transpose_matrix(matrix):
    transposed_matrix = [[0 for x in range(len(matrix))] for y in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            transposed_matrix[j][i] = matrix[i][j]
    return transposed_matrix

# matrix_multiply(a,b): multiplies two matrices together
# Input:
# 1- a: the first matrix
# 2- b: the second matrix
# Output:
# 1- result: the matrix product of a and b
def matrix_multiply(a,b):
    result = [[0 for x in range(len(b[0]))] for y in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k]*b[k][j]

    return result

# matrix_addition(a,b): adds 2 matrices together
# Input:
# 1- a: the first matrix
# 2- b: the second matrix
# Output:
# 1- result: the matrix sum of a and b
def matrix_addition(a,b):
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] = a[i][j]+b[i][j]
    return a

# matrix_subtraction(a,b):subtracts 2 matrices together
# Input:
# 1- a: the first matrix
# 2- b: the second matrix
# Output:
# 1- result: the matrix difference of a and b
def matrix_subtraction(a,b):
    result = [[0 for x in range(len(a[0]))] for y in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            result[i][j] = a[i][j]-b[j][i]
    return result

# vector_subtraction(a,b):subtracts 2 vectors together
# Input:
# 1- a: the first vector
# 2- b: the second vector
# Output:
# 1- result: the vector difference of a and b
def vector_subtraction(a,b):
    result = [[0 for x in range(len(a[0]))] for y in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            result[i][j] = a[i][j]-b[i][j]
    return result

# matrix_coeff_mult(a,b): multiplies matrix a with coefficient b
# Input:
# 1- a: the matrix
# 2- b: the coefficient
# Output:
# result of a*b
def matrix_coeff_mult(a,b):
    for i in range(len(a)):
            for j in range(len(a[0])):
                a[i][j] = a[i][j]*b
    return a

# matrix_inverse(matrix): inverts a matrix
# Input:
# 1- matrix: matrix to be inverted
# Output:
# 1- the inverted matrix
def matrix_inverse(matrix):
    #matrix of minors
    matrix_minors = get_matrix_minors(matrix)
    #matrix of cofactors
    matrix_cofactors = get_matrix_cofactors(matrix_minors)
    #get adjugate matrix
    adjugate_matrix = transpose_matrix(matrix_cofactors)
    #multiply by 1/determinant
    coeff = 1.0/get_determinant(matrix,matrix_minors)
    return matrix_coeff_mult(adjugate_matrix,coeff)

# get_matrix_minors(a): gets matrix minors to be used in matrix inverse calculation
# Input:
# 1- a: the matrix
# Output:
# 1- the matrix of minors
def get_matrix_minors(a):
    matrix = [[0 for x in range(3)] for y in range(3)]
    matrix[0][0] = a[1][1]*a[2][2] - a[1][2]*a[2][1]
    matrix[0][1] = a[1][0]*a[2][2] - a[1][2]*a[2][0]
    matrix[0][2] = a[1][0]*a[2][1] - a[1][1]*a[2][0]
    matrix[1][0] = a[0][1]*a[2][2] - a[0][2]*a[2][1]
    matrix[1][1] = a[0][0]*a[2][2] - a[0][2]*a[2][0]
    matrix[1][2] = a[0][0]*a[2][1] - a[0][1]*a[2][0]
    matrix[2][0] = a[0][1]*a[1][2] - a[0][2]*a[1][1]
    matrix[2][1] = a[0][0]*a[1][2] - a[0][2]*a[1][0]
    matrix[2][2] = a[0][0]*a[1][1] - a[0][1]*a[1][0]
    return matrix

# get_matrix_cofactors(a): get the matrix cofactors for matrix inversion
# Input: a the matrix
# Output: the matrix cofactors
def get_matrix_cofactors(a):
    a[0][1] = -1*a[0][1]
    a[1][0] = -1*a[1][0]
    a[1][2] = -1*a[1][2]
    a[2][1] = -1*a[2][1]
    return a

# get_determinant(a,b): gets the determinant of matrix a
# a: the matrix
# b: the matrix of minors
def get_determinant(a,b):
    return a[0][0]*b[0][0] - a[0][1]*b[0][1] + a[0][2]*b[0][2]

# quaterProd(a,b): product of 2 quaternions
# Input: a,b 2 quaternions
# Outputs: product of 2 quaternions
def quaterProd(a,b):
    ab = [[0],[0],[0],[0]]
    ab[0][0] = a[0][0]*b[0][0] - a[1][0]*b[1][0] - a[2][0]*b[2][0] - a[3][0]*b[3][0]
    ab[1][0] = a[0][0]*b[1][0] + a[1][0]*b[0][0] + a[2][0]*b[3][0] - a[3][0]*b[2][0]
    ab[2][0] = a[0][0]*b[2][0] - a[1][0]*b[3][0] + a[2][0]*b[0][0] + a[3][0]*b[1][0]
    ab[3][0] = a[0][0]*b[3][0] + a[1][0]*b[2][0] - a[2][0]*b[1][0] + a[3][0]*b[0][0]
    return ab

# quaterConj(a):
# Input: a,b 2 quaternions
# Outputs: product of 2 quaternions
def quaterConj(a):
    result = [[0],[0],[0],[0]]
    result[0][0] = a[0][0]
    result[1][0] = -1*a[1][0]
    result[2][0] = -1*a[2][0]
    result[3][0] = -1*a[3][0]
    return result

def get_identity_matrix(sz):
    matrix = [[0 for x in range(sz)] for y in range(sz)]
    for i in range(len(matrix)):
        matrix[i][i] = 1
    return matrix

def get_determinant_4x4(m):
    det = 0
    det += m[0][0]*m[1][1]*m[2][2]*m[3][3] + m[0][0]*m[1][2]*m[2][3]*m[3][1] + m[0][0]*m[1][3]*m[2][1]*m[3][2]
    det += m[0][1]*m[1][0]*m[2][3]*m[3][2] + m[0][1]*m[1][2]*m[2][0]*m[3][3] + m[0][1]*m[1][3]*m[2][2]*m[3][0]
    det += m[0][2]*m[1][0]*m[2][1]*m[3][3] + m[0][2]*m[1][1]*m[2][3]*m[3][0] + m[0][2]*m[1][3]*m[2][0]*m[3][1]
    det += m[0][3]*m[1][0]*m[2][2]*m[3][1] + m[0][3]*m[1][1]*m[2][0]*m[3][2] + m[0][3]*m[1][2]*m[2][1]*m[3][0]
    det -= m[0][0]*m[1][1]*m[2][3]*m[3][2] - m[0][0]*m[1][2]*m[2][1]*m[3][3] - m[0][0]*m[1][3]*m[2][2]*m[3][1]
    det -= m[0][1]*m[1][0]*m[2][2]*m[3][3] - m[0][1]*m[1][2]*m[2][3]*m[3][0] - m[0][1]*m[1][3]*m[2][0]*m[3][2]
    det -= m[0][2]*m[1][0]*m[2][3]*m[3][1] - m[0][2]*m[1][1]*m[2][0]*m[3][3] - m[0][2]*m[1][3]*m[2][1]*m[3][0]
    det -= m[0][3]*m[1][0]*m[2][1]*m[3][2] - m[0][3]*m[1][1]*m[2][2]*m[3][0] - m[0][3]*m[1][2]*m[2][0]*m[3][1]
    return det

# invert_4x4_matrix(m): inverts matrix m of size 4x4
# input: m the matrix
def invert_4x4_matrix(m):
    result = [[0 for x in range(4)] for y in range(4)]
    det = get_determinant_4x4(m)

    result[0][0] = m[1][1]*m[2][2]*m[3][3] + m[1][2]*m[2][3]*m[3][1] + m[1][3]*m[2][1]*m[3][2] - m[1][1]*m[2][3]*m[3][2] - m[1][2]*m[2][1]*m[3][3] - m[1][3]*m[2][2]*m[3][1]
    result[0][1] = m[0][1]*m[2][3]*m[3][2] + m[0][2]*m[2][1]*m[3][3] + m[0][3]*m[2][2]*m[3][1] - m[0][1]*m[2][2]*m[3][3] - m[0][2]*m[2][3]*m[3][1] - m[0][3]*m[2][1]*m[3][2]
    result[0][2] = m[0][1]*m[1][2]*m[3][3] + m[0][2]*m[1][3]*m[3][1] + m[0][3]*m[1][1]*m[3][2] - m[0][1]*m[1][3]*m[3][2] - m[0][2]*m[1][1]*m[3][3] - m[0][3]*m[1][2]*m[3][1]
    result[0][3] = m[0][1]*m[1][3]*m[2][2] + m[0][2]*m[1][1]*m[2][3] + m[0][3]*m[1][2]*m[2][1] - m[0][1]*m[1][2]*m[2][3] - m[0][2]*m[1][3]*m[2][1] - m[0][1]*m[1][1]*m[2][2]
    result[1][0] = m[1][0]*m[2][3]*m[3][2] + m[1][2]*m[2][0]*m[3][3] + m[1][3]*m[2][2]*m[3][0] - m[1][0]*m[2][2]*m[3][0] - m[1][2]*m[2][3]*m[3][0] - m[1][3]*m[2][0]*m[3][2]
    result[1][1] = m[0][0]*m[2][2]*m[3][3] + m[0][2]*m[2][3]*m[3][0] + m[0][3]*m[2][0]*m[3][2] - m[0][0]*m[2][3]*m[3][2] - m[0][2]*m[2][0]*m[3][3] - m[0][3]*m[2][2]*m[3][0]
    result[1][2] = m[0][0]*m[1][3]*m[3][2] + m[0][2]*m[1][0]*m[3][3] + m[0][3]*m[1][2]*m[3][0] - m[0][0]*m[1][2]*m[3][3] - m[0][2]*m[1][3]*m[3][0] - m[0][3]*m[1][0]*m[3][2]
    result[1][3] = m[0][0]*m[1][2]*m[2][3] + m[0][2]*m[1][3]*m[2][0] + m[0][3]*m[1][0]*m[2][2] - m[0][0]*m[1][3]*m[2][2] - m[0][2]*m[1][0]*m[2][3] - m[0][3]*m[1][2]*m[2][0]
    result[2][0] = m[1][0]*m[2][1]*m[3][3] + m[1][1]*m[2][3]*m[3][0] + m[1][3]*m[2][0]*m[3][1] - m[1][0]*m[2][3]*m[3][1] - m[1][1]*m[2][0]*m[3][3] - m[1][3]*m[2][1]*m[3][0]
    result[2][1] = m[0][0]*m[2][3]*m[3][1] + m[0][1]*m[2][0]*m[3][3] + m[0][3]*m[2][1]*m[3][0] - m[0][0]*m[2][1]*m[3][3] - m[0][1]*m[2][3]*m[3][0] - m[0][3]*m[2][0]*m[3][1]
    result[2][2] = m[0][0]*m[1][1]*m[3][3] + m[0][1]*m[1][3]*m[3][0] + m[0][3]*m[1][0]*m[3][1] - m[0][0]*m[1][3]*m[3][1] - m[0][1]*m[1][0]*m[3][3] - m[0][3]*m[1][1]*m[3][0]
    result[2][3] = m[0][0]*m[1][3]*m[2][1] + m[0][1]*m[1][0]*m[2][3] + m[0][3]*m[1][1]*m[2][0] - m[0][0]*m[1][1]*m[2][3] - m[0][1]*m[1][3]*m[2][0] - m[0][3]*m[1][0]*m[2][1]
    result[3][0] = m[1][0]*m[2][2]*m[3][1] + m[1][1]*m[2][0]*m[3][2] + m[1][2]*m[2][1]*m[3][0] - m[1][0]*m[2][1]*m[3][2] - m[1][1]*m[2][2]*m[3][0] - m[1][2]*m[2][0]*m[3][1]
    result[3][1] = m[0][0]*m[2][1]*m[3][2] + m[0][1]*m[2][2]*m[3][0] + m[0][2]*m[2][0]*m[3][1] - m[0][0]*m[2][2]*m[3][1] - m[0][1]*m[2][0]*m[3][2] - m[0][2]*m[2][1]*m[3][0]
    result[3][2] = m[0][0]*m[1][2]*m[3][1] + m[0][1]*m[1][0]*m[3][2] + m[0][2]*m[1][1]*m[3][0] - m[0][0]*m[1][1]*m[3][2] - m[0][1]*m[1][2]*m[3][0] - m[0][2]*m[1][0]*m[3][1]
    result[3][3] = m[0][0]*m[1][1]*m[2][2] + m[0][1]*m[1][2]*m[2][0] + m[0][2]*m[1][0]*m[2][1] - m[0][0]*m[1][2]*m[2][1] - m[0][1]*m[1][0]*m[2][2] - m[0][2]*m[1][1]*m[2][0]

    result = matrix_coeff_mult(result,1.0/det)
    return result
