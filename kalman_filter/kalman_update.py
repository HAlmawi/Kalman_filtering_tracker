import sys
import math
sys.path.append('../tools/')
import math_functions

# Kalman filter needs to update based on errors from prediction

# Step 1. Compute the difference between the measurement and the a priori state to get the innovation
def get_innovation(measurement,pred_state):
    return measurement - pred_state

# Step 2. Calculate the innovation covariance
def calc_innovation_covariance(prev_cov,sigma_R):
    H = math_functions.get_identity_matrix(4)
    R = get_measurement_cov(sigma_R)
    S = math_functions.matrix_addition(math_functions.matrix_multiplication(math_functions.matrix_multiplication(H,prev_cov),math_functions.transpose_matrix(H)),R)
    return S

# Step 3. Calculate the Kalman gain to determine how much we trust the innovation
def calc_Kalman_gain(prev_cov, innovation_cov):
    H = math_functions.get_identity_matrix(4)
    return math_functions.matrix_multiplication(prev_cov,math_functions.matrix_multiplication(math_functions.transpose_matrix(H),math_functions.invert_4x4_matrix(innovation_cov)))

# Step 4. Update the a posteriori estimate of the current state
def update_posteriori(pred_state,kalman_gain,innovation):
    return math_functions.matrix_addition(pred_state,math_functions.matrix_multiplication(kalman_gain,innovation))

# Step 5. Update the a posteriori error covariance matrix
def update_posteriori_covariance(kalman_gain,prev_cov):
    I = math_functions.get_identity_matrix(4)
    H = math_functions.get_identity_matrix(4)
    return math_functions.matrix_multiplication(math_functions.matrix_subtraction(I,math_functions.matrix_multiplication(kalman_gain,H)),prev_cov)

def get_measurement_cov(sigma_R):
    matrix = [[0 for x in range(4)] for y in range(4)]
    matrix[0][0] = sigma_R[0][0]
    matrix[1][1] = sigma_R[1][0]
    matrix[2][2] = sigma_R[2][0]
    matrix[3][3] = sigma_R[3][0]
    return matrix