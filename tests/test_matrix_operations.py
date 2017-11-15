import sys
sys.path.append('../tools/')
import math_functions

A = [[0 for x in range(3)] for y in range(3)]
A[0][0] = 3
A[0][1] = 0
A[0][2] = 2
A[1][0] = 2
A[1][1] = 0
A[1][2] = -2
A[2][0] = 0
A[2][1] = 1
A[2][2] = 1

# X=[[1,0,1]]

# for i in range(len(A)):
#     for j in range(len(A[0])):
#         print(str(A[i][j])+" "),
#     print "\n"
#
# result = math_functions.matrix_inverse(A)
#
# for i in range(len(result)):
#     for j in range(len(result[0])):
#         print(str(result[i][j])+" "),
#     print "\n"

# for i in range(len(X)):
#     for j in range(len(X[0])):
#         print(str(X[i][j])+" "),
#     print "\n"

# result_2 = math_functions.matrix_multiply(A,X)
#
# for i in range(len(result_2)):
#     for j in range(len(result_2[0])):
#         print(str(result_2[i][j])+" "),
#     print "\n"
