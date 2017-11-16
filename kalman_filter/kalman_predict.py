import sys
import math
sys.path.append('../tools/')
import math_functions

# Kalman filter needs to predict the quaternions to get rotation matrix

# Step 1.  Estimate the current state based on all previous states and the gyro measurement

def predict_state(F,prev_state):
    #Compute state transition model F
    pred_state = math_functions.matrix_multiply(F,prev_state)
    return pred_state

# Step 2. Estimate the a priori error covariance matrix based on the previous error covariance matrix
def predict_priori_covariance(prev_cov,Q_variance,F):
    pred_cov = math_function.matrix_addition(math_function.matrix_multiply(math_function.matrix_multiply(F,prev_cov),math_functions.transpose_matrix(F)),Q_variance)
    return pred_cov

def get_F_matrix(g,delta_t):
    F1 = [[1],[-1*delta_t/2*g[0][0]],[-1*delta_t/2*g[1][0]],[-1*delta_t/2*g[2][0]]]
    F2 = [[delta_t/2*g[0][0]],[1],[delta_t/2*g[2][0]],[-1*delta_t/2*g[1][0]]]
    F3 = [[delta_t/2*g[1][0]],[-1*delta_t/2*g[2][0]],[1],[delta_t/2*g[1][0]]]
    F4 = [[-1*delta_t/2*g[2][0]],[delta_t/2*g[1][0]],[-1*delta_t/2*g[0][0]],[1]]
    F = [F1,F2,F3,F4]
    return F

def get_Q_matrix(g_var):
    Q1 = [[g_var[0][0]+g_var[1][0]+g_var[2][0]],[-1*g_var[0][0]+g_var[1][0]-g_var[2][0]],[-1*g_var[0][0]-g_var[1][0]+g_var[2][0]],[g_var[0][0]-g_var[1][0]-g_var[2][0]]]
    Q2 = [[-1*g_var[0][0]+g_var[1][0]-g_var[2][0]],[g_var[0][0]+g_var[1][0]+g_var[2][0]],[g_var[0][0]-g_var[1][0]-g_var[2][0]],[-1*g_var[0][0]-g_var[1][0]+g_var[2][0]]]
    Q3 = [[-1*g_var[0][0]-g_var[1][0]+g_var[2][0]],[g_var[0][0]-g_var[1][0]-g_var[2][0]],[g_var[0][0]+g_var[1][0]+g_var[2][0]],[-1*g_var[0][0]+g_var[1][0]-g_var[2][0]]]
    Q4 = [[g_var[0][0]-g_var[1][0]-g_var[2][0]],[-1*g_var[0][0]+g_var[1][0]-g_var[2][0]],[-1*g_var[0][0]+g_var[1][0]-g_var[2][0]],[g_var[0][0]+g_var[1][0]+g_var[2][0]]]
    Q = [Q1,Q2,Q3,Q4]
    return Q