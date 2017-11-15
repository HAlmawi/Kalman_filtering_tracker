import sys
sys.path.append('./')
import math_functions

def IMU_to_Quaternion(g,a,m,q,beta, samplePeriod):
    # Normalize accelerometer measurement
    norm_a = math_functions.norm_vector(a)
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] *= (1/norm_a)

    # Normalize magnetometer measurement
    norm_m = math_functions.norm_vector(m)
    for i in range(len(m)):
        for j in range(len(m[0])):
            m[i][j] *= (1/norm_m)

    # Reference direction of Earth's magnetic field
    h = math_functions.quaterProd(q,math_functions.quaterProd([[0],m[0],m[1],m[2]],math_functions.quaterConj(q)))
    b = [[0],[math_functions.norm_vector([h[1],h[2]])],[0],h[3]]

    #Gradient decent algorithm corrective step
    F = [[2*(q[1][0]*q[3][0] - q[0][0]*q[3][0])-a[0][0]],[2*(q[0][0]*q[1][0] - q[2][0]*q[3][0])-a[1][0]],[2*(0.5-pow(q[1][0],2)-pow(q[2][0],2))-a[2][0]],[2*b[1][0]*(0.5-pow(q[2][0],2)-pow(q[3][0],2))+2*b[3][0]*(q[1][0]*q[3][0]-q[0][0]*q[2][0])-m[0][0]],[2*b[1][0]*(q[1][0]*q[2][0]-q[0][0]*q[3][0])+2*(b[3][0]*(q[0][0]*q[1][0]+q[2][0]*q[3][0]))-m[1][0]],[2*b[1][0]*(q[0][0]*q[2][0]+q[1][0]*q[3][0])+2*b[3][0]*(0.5-pow(q[1][0],2)-pow(q[2][0],2))-m[2][0]]]

    J = [[0 for x in range(4)] for y in range(6)]
    J[0][0] = -2*q[2][0]
    J[0][1] = 2*q[3][0]
    J[0][2] = -2*q[0][0]
    J[0][3] = 2*q[1][0]
    J[1][0] = 2*q[1][0]
    J[1][1] = 2*q[0][0]
    J[1][2] = 2*q[3][0]
    J[1][3] = 2*q[2][0]
    J[2][0] = 0
    J[2][1] = -4*q[1][0]
    J[2][2] = -4*q[2][0]
    J[2][3] = 0
    J[3][0] = -2*b[3][0]*q[2][0]
    J[3][1] = 2*b[3][0]*q[3][0]
    J[3][2] = -4*b[1][0]*q[2][0]-2*b[3][0]*q[0][0]
    J[3][3] = -4*b[1][0]*q[3][0]+2*b[3][0]*q[1][0]
    J[4][0] = -2*b[1][0]*q[3][0]+2*b[3][0]*q[1][0]
    J[4][1] = 2*b[1][0]*q[2][0]+2*b[3][0]*q[0][0]
    J[4][2] = 2*b[1][0]*q[1][0]+2*b[3][0]*q[3][0]
    J[4][3] = -2*b[1][0]*q[0][0]+2*b[3][0]*q[2][0]
    J[5][0] = 2*b[1][0]*q[2][0]
    J[5][1] = 2*b[1][0]*q[3][0]-4*b[3][0]*q[1][0]
    J[5][2] = 2*b[1][0]*q[0][0]-4*b[3][0]*q[2][0]
    J[5][3] = 2*b[1][0]*q[1][0]

    step = math_functions.matrix_multiply(math_functions.transpose_matrix(J),F)
    norm_s = math_functions.norm_vector(step)
    for i in range(len(step)):
        for j in range(len(step[0])):
            step[i][j] *= (1/norm_s)

    #Compute rate of change of quaternion
    qDot = math_functions.matrix_subtraction(math_functions.matrix_coeff_mult(math_functions.quaterProd(q,[[0],[g[0][0]],[g[1][0]],[g[2][0]]]),0.5 ),math_functions.matrix_coeff_mult(math_functions.transpose_matrix(step),beta))

    #Integrate to yield quaternion
    q = math_functions.matrix_addition(q,math_functions.matrix_coeff_mult(qDot,samplePeriod))
    norm_q = math_functions.norm_vector(q)
    for i in range(len(q)):
        for j in range(len(q[0])):
            q[i][j] *= (1/norm_q)
    return q
