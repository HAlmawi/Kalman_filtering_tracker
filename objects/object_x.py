import sys
sys.path.append('../tools')
import world_to_camera

class ObjectX:
    def __init__(self):
        self.w = [[0.0],[0.0],[0.0]] # position in world
        self.c = [[0.0],[0.0],[0.0]] # position in world

    def calc_world_coords(self,R,T):
        self.w = world_to_camera.camera_to_world(R,self.c,T)

    def update_c(self,c):
        self.c[0][0] = c[0][0]
        self.c[1][0] = c[1][0]
        self.c[2][0] = c[2][0]

    def update_w(self,d):
        self.w[0][0] += d[0][0]
        self.w[1][0] += d[1][0]
        self.w[2][0] += d[2][0]