import sys
import math
sys.path.append('../tools/')
import math_functions

# Kalman filter needs to predict the quaternions to get rotation matrix

# function predict_state(F,prev_state): Step 1. Estimate the current state based on previous state and the gyro measurement
# Input:
# 1- F: state transition model
# 2- prev_state: the previous quaternion
# Output:
# 1- pred_state: the predicted state
def predict_state(F,prev_state):
    pred_state = math_functions.matrix_multiply(F,prev_state)
    return pred_state

# predict_priori_covariance(prev_cov,Q_variance,F): Step 2. Estimate the a priori error covariance matrix based on the previous error covariance matrix
# Input:
# 1- prev_cov: the previous error covariance matrix
# 2- Q_variance: the bias and noise from instrument measurements
# 3- F: The state transition model
# Output:
# 1- the predicted priori covariance matrix
def predict_priori_covariance(prev_cov,Q_variance,F):
    pred_cov = math_functions.matrix_addition(math_functions.matrix_multiply(math_functions.matrix_multiply(F,prev_cov),math_functions.transpose_matrix(F)),Q_variance)
    return pred_cov

# get_F_matrix(g,delta_t): produces a state transition model based on the gyroscope readings and the time interval
# Input:
# 1- g: gyroscope readings
# 2- delta_t: the time elapsed
# Output:
# 1- get state transition model
def get_F_matrix(g,delta_t):
    F1 = [1.0,-1.0*delta_t/2.0*g[0][0],-1.0*delta_t/2.0*g[1][0],-1.0*delta_t/2.0*g[2][0]]
    F2 = [delta_t/2.0*g[0][0],1.0,delta_t/2.0*g[2][0],-1.0*delta_t/2.0*g[1][0]]
    F3 = [delta_t/2.0*g[1][0],-1.0*delta_t/2.0*g[2][0],1.0,delta_t/2.0*g[1][0]]
    F4 = [-1.0*delta_t/2.0*g[2][0],delta_t/2.0*g[1][0],-1.0*delta_t/2.0*g[0][0],1.0]
    F = [F1,F2,F3,F4]
    return F


# get_Q_matrix(g_var): produces Q matrix with noise in gyroscope readings
# Input:
# 1- g: gyroscope noise readings variances
# Output:
# 1- Q matrix
def get_Q_matrix(g_var):
    Q1 = [g_var[0][0]+g_var[1][0]+g_var[2][0],-1.0*g_var[0][0]+g_var[1][0]-g_var[2][0],-1.0*g_var[0][0]-g_var[1][0]+g_var[2][0],g_var[0][0]-g_var[1][0]-g_var[2][0]]
    Q2 = [-1.0*g_var[0][0]+g_var[1][0]-g_var[2][0],g_var[0][0]+g_var[1][0]+g_var[2][0],g_var[0][0]-g_var[1][0]-g_var[2][0],-1.0*g_var[0][0]-g_var[1][0]+g_var[2][0]]
    Q3 = [-1.0*g_var[0][0]-g_var[1][0]+g_var[2][0],g_var[0][0]-g_var[1][0]-g_var[2][0],g_var[0][0]+g_var[1][0]+g_var[2][0],-1.0*g_var[0][0]+g_var[1][0]-g_var[2][0]]
    Q4 = [g_var[0][0]-g_var[1][0]-g_var[2][0],-1.0*g_var[0][0]+g_var[1][0]-g_var[2][0],-1.0*g_var[0][0]+g_var[1][0]-g_var[2][0],g_var[0][0]+g_var[1][0]+g_var[2][0]]
    Q = [Q1,Q2,Q3,Q4]
    return Q
