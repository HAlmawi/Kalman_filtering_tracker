import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
sys.path.append('./tools')
sys.path.append('./objects')
sys.path.append('./kalman_filter')
sys.path.append('./data_creation')
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
import math
import math_functions
import create_data

# Main function
def main():
    # Create data needed for the program to run
    # create_data.create_data()
    filename = "./result_readings.txt"
    # Rate in seconds for data input converted from Hz
    rate = 1.0/30.0
    # Creating X object - handheld with IMU
    x = object_x.ObjectX()
    # Creating C object - stereo camera system
    c = object_c.ObjectC()
    # Initializing the gyroscope variance based on random
    gyro_var = [[math.pow(random.random()/180.0*math.pi,2)],[math.pow(random.random()/180.0*math.pi,2)],[math.pow(random.random()/180.0*math.pi,2)]]
    # Get the Q matrix using the gyroscope variance "readings"
    Q_matrix = kalman_predict.get_Q_matrix(gyro_var)
    # SigmaR in order to construct the measurement covariance matrix
    sigmaR = [[0.000001],[0.000001],[0.000001],[0.000001]]
    # Initializing bias for quaternion calculation
    beta = 0.1
    # Initializing a priori matrix
    P_Update = math_functions.matrix_coeff_mult(math_functions.get_identity_matrix(4),0.01)
    # Initializing X coords used to visualize plot
    X_Coords = [];
    with open(filename, 'r') as file:
        data = file.readlines()
    for i in range(len(data)):
        #first line is to initialize C and X
        info = line_to_IMU.line_to_IMU(data[i])
        if i==0:
            # timestamp
            time = float(info[0][0])
            # Initialize X's position
            x.update_c([[float(info[0][12])],[float(info[0][13])],[float(info[0][14])]])
            # Get the accelerometer readings
            a = [[float(info[0][2])], [float(info[0][3])], [float(info[0][4])]]
            # Get the gyroscope readings
            g = [[float(info[0][5])*(math.pi/180.0)], [float(info[0][6])*(math.pi/180.0)], [float(info[0][7])*(math.pi/180.0)]]
            # Get the magnetometer readings
            m = [[float(info[0][8])], [float(info[0][9])], [float(info[0][10])]]
            # Set camera's quaternions to be equal to the result of IMU to Quaternion
            c.set_q(IMU_to_quaternion.IMU_to_Quaternion(g,a,m,c.q,beta, time))
            # Set camera's rotation matrix to be equal to the result of Quaternion to Rotation matrix
            c.set_r_m(quaternion_to_rotation.quaternion2rotation(c.q))
            # Set camera's translation matrix to be equal to the result of accelerometer to translation
            c.set_t_m(IMU_to_Translation.calcTranslation(a,c.v0,rate))
            c.update_v(a,rate) #update camera's initial velocity
            X_Coords.append([x.c[0][0],x.c[1][0],x.c[2][0]])
        else:
            #rest: for X: calculate its movement in the world coordinate space
            # for C: predict the rotation matrix and translation, predict X's position in C coordinate space, and if observation is present, update the kalman filter
            if int(info[0][1])==0:
                # Get the accelerometer read
                a = [[float(info[0][2])], [float(info[0][3])], [float(info[0][4])]]
                # Calculate X's world coordinates
                x.calc_world_coords(c.r_m,c.t_m)
                # Update X's initial velocity
                x.update_v(a,rate)
            else: #C
                # time
                time = float(info[0][0])
                # Get the accelerometer readings
                a = [[float(info[0][2])], [float(info[0][3])], [float(info[0][4])]]
                # Get the gyroscope readings
                g = [[float(info[0][5])*(math.pi/180.0)], [float(info[0][6])*(math.pi/180.0)], [float(info[0][7])*(math.pi/180.0)]]
                # Get the magnetometer readings
                m = [[float(info[0][8])], [float(info[0][9])], [float(info[0][10])]]
                # Quaternion calculated
                quatern_C = IMU_to_quaternion.IMU_to_Quaternion(g,a,m,c.q,beta,time)

                #Get F matrix
                F = kalman_predict.get_F_matrix(g,rate)
                #Kalman predict state -> input: F,c.q
                quatern_pred = kalman_predict.predict_state(F,c.q)
                #Kalman predict predict_priori_covariance -> p_predicted = P_update,Q_matrix,F
                P_predicted = kalman_predict.predict_priori_covariance(P_Update,Q_matrix,F)
                # If Camera position is known, then kalman update
                if int(info[0][11])==1:
                    #get_innovation -> quatern_predicted is kalman predict state, quatern_C is q observed
                    innovation = kalman_update.get_innovation(quatern_C,quatern_pred)
                    #calc_innovation_covariance(prev_cov,sigma_R) -> prev_cov = P_Predicted; output=innovation_cov
                    innovation_cov = kalman_update.calc_innovation_covariance(P_predicted, sigmaR)
                    #calc_Kalman_gain(prev_cov, innovation_cov) -> prev_cov = P_Predicted
                    kalman_gain  = kalman_update.calc_Kalman_gain(P_predicted, innovation_cov)
                    #c.q = update_posteriori(pred_state,kalman_gain,innovation)
                    c.set_q(kalman_update.update_posteriori(quatern_pred,kalman_gain,innovation))
                    #p_update = update_posteriori_covariance(kalman_gain, prev_cov)
                    P_Update = kalman_update.update_posteriori_covariance(kalman_gain,P_predicted)
                else:
                    c.set_q(quatern_pred)
                # Rotation matrix calculated
                R_M = quaternion_to_rotation.quaternion2rotation(c.q)
                # Translation matrix calculated
                T_M = IMU_to_Translation.calcTranslation(a,c.v0,rate)
                #update camera's initial velocity
                c.update_v(a,rate)
    #             Get X's camera coords, if all positive, then add position to input file
                P = world_to_camera.world_to_camera(R_M,x.w,T_M)
                x.update_c(P)
                X_Coords.append([x.c[0][0],x.c[1][0],x.c[2][0]])
    #Plot the coords
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = [p[0] for p in X_Coords]
    ys = [p[1] for p in X_Coords]
    zs = [p[2] for p in X_Coords]
    surf = ax.plot(xs,ys,zs)
    plt.show()

if __name__ == "__main__":
    main()
