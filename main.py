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

def main():
    filename = "./result_readings.txt"
    rate = 1.0/30.0
    x = object_x.ObjectX()
    c = object_c.ObjectC()
    gyro_var = [[math.pow(random.random()/180.0*math.pi,2)],[math.pow(random.random()/180.0*math.pi,2)],[math.pow(random.random()/180.0*math.pi,2)]]
    Q_matrix = kalman_predict.get_Q_matrix(gyro_var)
    sigmaR = [[0.0001],[0.0001],[0.0001],[0.0001]]
    beta = 0.1
    P_Update = math_functions.matrix_coeff_mult(math_functions.get_identity_matrix(4),0.01)
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
            g = [[float(info[0][5])*(math.pi/180.0)], [float(info[0][6])*(math.pi/180.0)], [float(info[0][7])*(math.pi/180.0)]]
            # Get the magnetometer readings
            m = [[float(info[0][8])], [float(info[0][9])], [float(info[0][10])]]
            # Set camera's quaternions to be equal to the result of IMU to Quaternion
            c.set_q(IMU_to_quaternion.IMU_to_Quaternion(g,a,m,c.q,beta, rate))
            # Set camera's rotation matrix to be equal to the result of Quaternion to Rotation matrix
            c.set_r_m(quaternion_to_rotation.quaternion2rotation(c.q))
            # Set camera's translation matrix to be equal to the result of accelerometer to translation
            c.set_t_m(IMU_to_Translation.calcTranslation(a,c.v0,rate))
            c.update_v(a,rate) #update camera's initial velocity
        else:
            #rest: for X: see if distance traveled is greater than 3m and fix the line
            # for C: check if rotation matrix with translation causes X to be 3m away
            if int(info[0][1])==0: #X
                # Get the accelerometer read
                a = [[float(info[0][2])], [float(info[0][3])], [float(info[0][4])]]
                # Calculate X's world coordinates
                x.calc_world_coords(c.r_m,c.t_m)
                # Get the distance traveled based on the accelerometer read
                d = IMU_to_Translation.calcTranslation(a,x.v0,rate)
                # Update X's initial velocity
                x.update_v(a,rate)
            else: #C
                # Get the accelerometer readings
                a = [[float(info[0][2])], [float(info[0][3])], [float(info[0][4])]]
                # Get the gyroscope readings
                g = [[float(info[0][5])*(math.pi/180.0)], [float(info[0][6])*(math.pi/180.0)], [float(info[0][7])*(math.pi/180.0)]]
                # Get the magnetometer readings
                m = [[float(info[0][8])], [float(info[0][9])], [float(info[0][10])]]
                # Quaternion calculated
                quatern_C = IMU_to_quaternion.IMU_to_Quaternion(g,a,m,c.q,beta, rate)

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


if __name__ == "__main__":
    main()
