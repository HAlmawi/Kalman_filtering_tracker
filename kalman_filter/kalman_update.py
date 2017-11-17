import sys
import math
sys.path.append('../tools/')
import math_functions

# Kalman filter needs to update based on errors from prediction

# function get_innovation(measurement,pred_state): Step 1. Compute the difference between the measurement and the a priori state to get the innovation
# Input:
# 1- measurement: the observation of the quaternion
# 2- pred_state: the predicted quaternion
# Output:
# 1- innovation: the difference between measurements
def get_innovation(measurement,pred_state):
    return math_functions.vector_subtraction(measurement ,pred_state)

#function calc_innovation_covariance(prev_cov,sigma_R): Step 2. Calculate the innovation covariance
# Input:
# 1- prev_cov: the previous state covariance
# 2- sigma_R: used to produce measurement covariance matrix
# Output:
# 1- S: the innovation covariance matrix
def calc_innovation_covariance(prev_cov,sigma_R):
    H = math_functions.get_identity_matrix(4)
    R = get_measurement_cov(sigma_R)
    S = math_functions.matrix_addition(math_functions.matrix_multiply(math_functions.matrix_multiply(H,prev_cov),math_functions.transpose_matrix(H)),R)
    return S

# calc_Kalman_gain(prev_cov, innovation_cov): Step 3. Calculate the Kalman gain to determine how much we trust the innovation
# Input:
# 1- prev_cov: previous covariance matrix
# 2- innovation_cov: innovation covariance matrix calculated above
# Output:
# 1- the Kalman gain
def calc_Kalman_gain(prev_cov, innovation_cov):
    H = math_functions.get_identity_matrix(4)
    return math_functions.matrix_multiply(prev_cov,math_functions.matrix_multiply(math_functions.transpose_matrix(H),math_functions.invert_4x4_matrix(innovation_cov)))

#update_posteriori(pred_state,kalman_gain,innovation): Step 4. Update the a posteriori estimate of the current state
# Input:
# 1- pred_state: the predicted quaternion
# 2- kalman_gain: trust in innovation, calculate above
# 3- innovation: difference in readings and prediction, calculated above
# Output:
# 1- the updated posteriori
def update_posteriori(pred_state,kalman_gain,innovation):
    return math_functions.matrix_addition(pred_state,math_functions.matrix_multiply(kalman_gain,innovation))

# update_posteriori_covariance(kalman_gain,prev_cov): Step 5. Update the a posteriori error covariance matrix
# Input:
# 1- kalman_gain: trust in innovation, calculated above
# 2- prev_cov: the previous covariance matrix
# Output:
# 1- the updated posteriori covariance (how much we trust the posteriori)
def update_posteriori_covariance(kalman_gain,prev_cov):
    I = math_functions.get_identity_matrix(4)
    H = math_functions.get_identity_matrix(4)
    return math_functions.matrix_multiply(math_functions.matrix_subtraction(I,math_functions.matrix_multiply(kalman_gain,H)),prev_cov)

# get_measurement_cov(sigma_R): function to generate measurement covariance matrix
# Input:
# 1- Sigma_R:4x1 float list  with the variances
# Output:
# 1- measurement covariance matrix
def get_measurement_cov(sigma_R):
    matrix = [[0 for x in range(4)] for y in range(4)]
    matrix[0][0] = sigma_R[0][0]
    matrix[1][1] = sigma_R[1][0]
    matrix[2][2] = sigma_R[2][0]
    matrix[3][3] = sigma_R[3][0]
    return matrix
