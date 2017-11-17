#Calculate translation in X,Y,Z given the acceleration measurement in x,y,z and time interval
#Input: ax, ay, az the acceleration in x,y,z respectively retrieved from IMU
#Output: delta_x, delta_y, delta_z the distance moved in time interval
def calcTranslation(a, v0, delta_t):
    t = [[0],[0],[0]]
    t[0][0] = delta_t*((v0[0][0]+ a[0][0] * delta_t)+v0[0][0])/2
    t[1][0] = delta_t*((v0[1][0]+ a[1][0] * delta_t)+v0[1][0])/2
    t[2][0] = delta_t*((v0[2][0]+ a[2][0] * delta_t)+v0[2][0])/2
    return t
