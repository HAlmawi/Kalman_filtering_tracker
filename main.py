import sys
sys.path.append('./tools')
sys.path.append('./objects')
sys.path.append('./kalman_filter')
import world_to_camera
import object_x
import object_c
import line_to_IMU
import IMU_to_quaternion
import quaternion_to_rotation
import IMU_to_Translation
import kalman_predict
import kalman_update
import random

def main():
    filename = "./result_readings.txt"
    rate = 1.0/30.0
    x = object_x.ObjectX()
    c = object_c.ObjectC()
    gyro_var = [[],[],[]]
    kalman_predict.get_Q_matrix()
    beta = 0.1
    with open(filename, 'r') as file:
        data = file.readlines()
    for i in range(len(data)):
        #first line is to initialize C and X
        info = line_to_IMU.line_to_IMU(data[i])
        if i==0:
            # Initialize X's position
            x.update_c([[float(info[0][12])],[float(info[0][13])],[float(info[0][14])]])
            # Get the accelerometer readings
            a = [[float(info[0][2])], [float(info[0][3])], [float(info[0][4])]]
            # Get the gyroscope readings
            g = [[float(info[0][5])], [float(info[0][6])], [float(info[0][7])]]
            # Get the magnetometer readings
            m = [[float(info[0][8])], [float(info[0][9])], [float(info[0][10])]]
            # Set camera's quaternions to be equal to the result of IMU to Quaternion
            c.set_q(IMU_to_quaternion.IMU_to_Quaternion(g,a,m,c.q,beta, rate))
            # Set camera's rotation matrix to be equal to the result of Quaternion to Rotation matrix
            c.set_r_m(quaternion_to_rotation.quaternion2rotation(c.q))
            # Set camera's translation matrix to be equal to the result of accelerometer to translation
            c.set_t_m(IMU_to_Translation.calcTranslation(a,rate))
        else:
            #rest: for X: see if distance traveled is greater than 3m and fix the line
            # for C: check if rotation matrix with translation causes X to be 3m away
            if int(info[0][1])==0: #X
                # Get the accelerometer read
                a = [[float(info[0][2])], [float(info[0][3])], [float(info[0][4])]]
                # Calculate X's world coordinates
                x.calc_world_coords(c.r_m,c.t_m)
                # Get the distance traveled based on the accelerometer read
                d = IMU_to_Translation.calcTranslation(a,rate)
                # Check if the distance it traveled is less than 3m
                # If traveled more than 3m, update the input file, and update the distances in X
                d[0][0] = -1*d[0][0]
                d[1][0] = -1*d[1][0]
                d[2][0] = -1*d[2][0]
                x.update_w(d)
            else: #C
                # Is X outside of Camera reference frame?
                # Get the accelerometer readings
                a = [[float(info[0][2])], [float(info[0][3])], [float(info[0][4])]]
                # Get the gyroscope readings
                g = [[float(info[0][5])], [float(info[0][6])], [float(info[0][7])]]
                # Get the magnetometer readings
                m = [[float(info[0][8])], [float(info[0][9])], [float(info[0][10])]]
                # Quaternion calculated
                Q = IMU_to_quaternion.IMU_to_Quaternion(g,a,m,c.q,beta, rate)
                # Rotation matrix calculated
                R_M = quaternion_to_rotation.quaternion2rotation(c.q)
                # Translation matrix calculated
                T_M = IMU_to_Translation.calcTranslation(a,rate)
    #             Get X's camera coords, if all positive, then add position to input file
                P = world_to_camera.world_to_camera(R_M,x.w,T_M)
                x.update_c(P)

if __name__ == "__main__":
    main()