import sys
sys.path.append('./')
from . import math_functions

def IMU_to_Quaternion(g,a,m,q,beta, samplePeriod):
    # Normalize accelerometer measurement
    norm_a = math_functions.norm_vector(a)
    normalized_a = [num / norm_a for num in a]

    # Normalize magnetometer measurement
    norm_m = math_functions.norm_vector(m)
    normalized_m = [num / norm_m for num in m]

    # Reference direction of Earth's magnetic field
    h = math_functions.quaterProd(q,math_functions.quaterProd([0]+normalized_m,math_functions.quaternConj(q)))
    b = [0] + [math_functions.norm_vector({h[1],h[2]})]+[0]+[h(3)]

    #Gradient decent algorithm corrective step
    F = [2*(q[1]*q[3] - q[0]*q[3])-normalized_a[0]]\
        +[2*(q[0]*q[1] - q[2]*q[3])-normalized_a[1]]\
        +[2*(0.5-pow(q[1],2)-pow(q[2],2))-normalized_a[2]]\
        +[2*b[1]*(0.5-pow(q[2],2)-pow(q[3],2))+2*b[3]*(q[1]*q[3]-q[0]*q[2])-normalized_m[0]]\
        +[2*b[1]*(q[1]*q[2]-q[0]*q[3])+2*(b[3]*(q[0]*q[1]+q[2]*q[3]))-normalized_m[1]]\
        +[2*b[1]*(q[0]*q[2]+q[1]*q[3])+2*b[3]*(0.5-pow(q[1],2)-pow(q[2],2))-normalized_m[2]]

    J = [[0 for x in range(4)] for y in range(6)]
    J[0][0] = -2*q[2]
    J[0][1] = 2*q[3]
    J[0][2] = -2*q[0]
    J[0][3] = 2*q[1]
    J[1][0] = 2*q[1]
    J[1][1] = 2*q[0]
    J[1][2] = 2*q[3]
    J[1][3] = 2*q[2]
    J[2][0] = 0
    J[2][1] = -4*q[1]
    J[2][2] = -4*q[2]
    J[2][3] = 0
    J[3][0] = -2*b[3]*q[2]
    J[3][1] = 2*b[3]*q[3]
    J[3][2] = -4*b[1]*q[2]-2*b[3]*q[0]
    J[3][3] = -4*b[1]*q[3]+2*b[3]*q[1]
    J[4][0] = -2*b[1]*q[3]+2*b[3]*q[1]
    J[4][1] = 2*b[1]*q[2]+2*b[3]*q[0]
    J[4][2] = 2*b[1]*q[1]+2*b[3]*q[3]
    J[4][3] = -2*b[1]*q[0]+2*b[3]*q[2]
    J[5][0] = 2*b[1]*q[2]
    J[5][1] = 2*b[1]*q[3]-4*b[3]*q[1]
    J[5][2] = 2*b[1]*q[0]-4*b[3]*q[2]
    J[5][3] = 2*b[1]*q[1]

    step = math_functions.matrix_multiply(math_functions.transpose_matrix(J),F)
    norm_s = math_functions.norm_matrix(step)
    normalize_step = [num / norm_s  for num in step] #Normalize step magnitude

    #Compute rate of change of quaternion
    qDot = [0]*4
    qDot = 0.5 * math_functions.quaterProd(q,[0,g[0],g[1],g[2]])-beta*math_functions.transpose_matrix(normalize_step)

    #Integrate to yield quaternion
    q = q + qDot*samplePeriod
    norm_q = math_functions.norm_matrix(q)
    normalized_q = [num / norm_q  for num in q] #normalize quaternion
    return normalized_q
