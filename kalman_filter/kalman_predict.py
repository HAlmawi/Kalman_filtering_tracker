import sys
import math
sys.path.append('../tools/')
import math_functions
# Kalman filter needs to predict the quaternions to get rotation matrix

# Step 1.  Estimate the current state based on all previous states and the gyro measurement

def predict_state(g,prev_state,delta_t,rate_k):
    #Compute state transition model F
    F1 = [[1],[-1*delta_t/2*g[0][0]],[-1*delta_t/2*g[1][0]],[-1*delta_t/2*g[2][0]]]
    F2 = [[delta_t/2*g[0][0]],[1],[delta_t/2*g[2][0]],[-1*delta_t/2*g[1][0]]]
    F3 = [[delta_t/2*g[1][0]],[-1*delta_t/2*g[2][0]],[1],[delta_t/2*g[1][0]]]
    F4 = [[-1*delta_t/2*g[2][0]],[delta_t/2*g[1][0]],[-1*delta_t/2*g[0][0]],[1]]
    F = [F1,F2,F3,F4]

    pred_state = math_functions.matrix_multiply(F,prev_state)
    return pred_state, F

# Step 2. Estimate the a priori error covariance matrix based on the previous error covariance matrix
def predict_priori_covariance(prev_cov,imu_variance,F):
    Q = {{imu_variance, 0},{0,bias_variance}}*delta_t
    pred_cov = math_function.matrix_addition(math_function.matrix_multiply(math_function.matrix_multiply(F,prev_cov),math_functions.transpose_matrix(F)),Q)
    return pred_cov
