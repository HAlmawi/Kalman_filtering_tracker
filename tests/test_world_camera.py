import sys
sys.path.append('../tools')
import IMU_to_Translation
import world_to_camera

R_M = [[1.0000,-0.0001,0.02],
    [0.01,1.0000,-0.08],
   [-0.02,0.08,1.0000]]

a = [[0.0190],[-0.0522],[0.9780]]

delta_t = 1.0/256.0

T_M = IMU_to_Translation.calcTranslation(a, delta_t)

W = [[1],[1.5],[1.5]]

P = world_to_camera.world_to_camera(R_M,W,T_M)



PC = world_to_camera.camera_to_world(R_M,P,T_M)

for i in range(3):
    print(PC[i][0]+" ")