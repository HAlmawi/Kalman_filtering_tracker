class ObjectX:
    def __init__(self):
        self.x = 0 #x position in world
        self.y = 0 #y position in world
        self.z = 0 #z position in world
        self.a = {0,0,0} #accelerometer data taken from IMU reading
        self.g = {0,0,0} #gyroscope data taken from IMU reading
        self.m = {0,0,0} #magnometer data taken from IMU reading
