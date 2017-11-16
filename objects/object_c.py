class ObjectC:
    def __init__(self):
        self.a = [[0],[0],[0]] #accelerometer data taken from IMU reading
        self.g =  [[0],[0],[0]] #accelerometer data taken from IMU reading
        self.m =  [[0],[0],[0]] #accelerometer data taken from IMU reading
        self.r_m =  [[0,0,0],[0,0,0],[0,0,0]] #accelerometer data taken from IMU reading
        self.q =  [[0],[0],[0],[0]] #quaternions
        self.t_m = [[0],[0],[0]] #translation matrix