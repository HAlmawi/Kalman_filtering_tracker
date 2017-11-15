#Calculate translation in X,Y,Z given the acceleration measurement in x,y,z and time interval
#Input: ax, ay, az the acceleration in x,y,z respectively retrieved from IMU
#Output: delta_x, delta_y, delta_z the distance moved in time interval
def calcTranslation(ax,ay,az, delta_t):
    delta_x = ax * pow(delta_t,2)
    delta_y = ay * pow(delta_t,2)
    delta_z = az * pow(delta_t,2)
    return delta_x, delta_y, delta_z
