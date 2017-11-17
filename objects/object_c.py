import sys
sys.path.append('../tools')
import world_to_camera

class ObjectC:
    def __init__(self):
        self.r_m =  [[0,0,0],[0,0,0],[0,0,0]] #accelerometer data taken from IMU reading
        self.q =  [[1],[0],[0],[0]] #quaternions
        self.t_m = [[0],[0],[0]] #translation matrix
        self.v0 = [[0.0],[0.0],[0.0]] #intial velocity used for translation matrix calculation
    # Set the rotation matrix
    def set_r_m(self,r_m):
        self.r_m[0][0] = r_m[0][0]
        self.r_m[0][1] = r_m[0][1]
        self.r_m[0][2] = r_m[0][2]
        self.r_m[1][0] = r_m[1][0]
        self.r_m[1][1] = r_m[1][1]
        self.r_m[1][2] = r_m[1][2]
        self.r_m[2][0] = r_m[2][0]
        self.r_m[2][1] = r_m[2][1]
        self.r_m[2][2] = r_m[2][2]
    # Set the translation matrix
    def set_t_m(self,t_m):
        self.t_m[0][0] = t_m[0][0]
        self.t_m[1][0] = t_m[1][0]
        self.t_m[2][0] = t_m[2][0]
    # Set the quaternions
    def set_q(self,q):
        self.q[0][0] = q[0][0]
        self.q[1][0] = q[1][0]
        self.q[2][0] = q[2][0]
        self.q[3][0] = q[3][0]

    def update_v(self,a,rate):
        self.v0[0][0] = self.v0[0][0]+a[0][0]*rate
        self.v0[1][0] = self.v0[1][0]+a[1][0]*rate
        self.v0[2][0] = self.v0[2][0]+a[2][0]*rate
