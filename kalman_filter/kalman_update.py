# Kalman filter needs to update based on errors from prediction

# Step 1. Compute the difference between the measurement and the a priori state to get the innovation
def get_innovation(measurement,pred_state):
    return measurement - pred_state

# Step 2. Calculate the innovation covariance
def calc_innovation_covariance(prev_cov,measurement_cov):
    H = {1,0}
    S = H*prev_cov*H + measurement_cov
    return S

# Step 3. Calculate the Kalman gain to determine how much we trust the innovation
def calc_Kalman_gain(prev_cov, innovation_cov):
    H = {1,0}
    return prev_cov*H*(1/innovation_cov)

# Step 4. Update the a posteriori estimate of the current state
def update_posteriori(pred_state,kalman_gain,innovation):
    return pred_state + kalman_gain*innovation

# Step 5. Update the a posteriori error covariance matrix
def update_posteriori_covariance(kalman_gain,prev_cov):
    I = {{1,0},{0,1}}
    H = {1,0}
    return (I-kalman_gain*H)*prev_cov
