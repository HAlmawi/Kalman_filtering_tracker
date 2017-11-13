# Kalman filter needs to predict the IMU readings

# Step 1.  Estimate the current state based on all previous states and the gyro measurement

def predict_state(prev_state,delta_t,rate_k):
    F = {{1,-1*delta_t},{0,1}}
    B = {{delta_t},{0}}
    pred_state = F*prev_state + B*rate_k
    return pred_state

# Step 2. Estimate the a priori error covariance matrix based on the previous error covariance matrix
def predict_priori_covariance(prev_cov,delta_t,imu_variance,bias_variance):
    F = {{1,-1*delta_t},{0,1}}
    Q = {{imu_variance, 0},{0,bias_variance}}*delta_t
    pred_cov = F*prev_cov*F + Q
    return pred_cov