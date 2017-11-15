import sys
import math
sys.path.append('../tools/')
import IMU_to_quaternion

a = [0.0190, -0.0522, 0.9780]
g = [-0.9375, -1.2500, 0.8750]
m = [0.2100, 0.0312,-0.4487]
q = [1,0,0,0]
beta = 0.1
samplePeriod = 1.0/256.0

g = [num * (math.pi/180.0)  for num in g]

result = IMU_to_quaternion.IMU_to_Quaternion(g,a,m,q,beta, samplePeriod)
