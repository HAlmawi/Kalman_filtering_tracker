import sys
sys.path.append('../tools')
sys.path.append('../objects')
sys.path.append('./')
import random
import math
import world_to_camera
import object_x
import object_c
import line_to_IMU
import IMU_to_quaternion
import quaternion_to_rotation
import IMU_to_Translation

def randomize_readings(filename,rate,num_readings):
    f = open(filename,'w+')
    imu_lag = random.uniform(0,rate)
    tc = 0
    tx = imu_lag
    for i in range(num_readings):
        # first line must have camera reading of X position relative to camera reference frame
        if i==0:
            X = get_reading(tx,0,0)
            C = get_reading(tc,1,1)
            f.write(C+"\n"+X+"\n")
        else:
            X = get_reading(tx,0,0)
            C = get_reading(tc,1,0)
            f.write(C+"\n"+X+"\n")
        tc += rate
        tx += rate
    f.close()
    return

def enforce_specifications(filename,rate,save_filename):
    # Read lines
    x = object_x.ObjectX()
    c = object_c.ObjectC()
    beta = 0.1
    with open(filename, 'r') as file:
        data = file.readlines()
    s_f = open(save_filename,'w')
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
            s_f.write(data[i])
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
                # Check if the distance it traveled is less than 3m
                if distance_flag(x,d) == 0:
                    # If traveled more than 3m, update the input file, and update the distances in X
                    s_f.write(info[0][0]+" "+info[0][1]+" "+str(-1*float(info[0][2]))+" "+str(-1*float(info[0][3]))+" "+str(-1*float(info[0][4]))+"\n")
                    d[0][0] = -1*d[0][0]
                    d[1][0] = -1*d[1][0]
                    d[2][0] = -1*d[2][0]
                else:
                    s_f.write(data[i])
                x.update_w(d)
            else: #C
                # Is X outside of Camera reference frame?
                # Get the accelerometer readings
                a = [[float(info[0][2])], [float(info[0][3])], [float(info[0][4])]]
                # Get the gyroscope readings
                g = [[float(info[0][5])*(math.pi/180.0)], [float(info[0][6])*(math.pi/180.0)], [float(info[0][7])*(math.pi/180.0)]]
                # Get the magnetometer readings
                m = [[float(info[0][8])], [float(info[0][9])], [float(info[0][10])]]
                # Quaternion calculated
                Q = IMU_to_quaternion.IMU_to_Quaternion(g,a,m,c.q,beta, rate)
                # Rotation matrix calculated
                R_M = quaternion_to_rotation.quaternion2rotation(c.q)
                # Translation matrix calculated
                T_M = IMU_to_Translation.calcTranslation(a,c.v0,rate)
                #update camera's initial velocity
                c.update_v(a,rate)
    #             Get X's camera coords, if all positive, then add position to input file
                #Check if translation is greater than 3m
                # Check if the distance it traveled is less than 3m
                if distance_flag(x,T_M) == 0:
                    # If traveled more than 3m, update the input file, and update the distances in X
                    s_f.write(info[0][0]+" "+info[0][1]+" "+str(-1*float(info[0][2]))+" "+str(-1*float(info[0][3]))+" "+str(-1*float(info[0][4]))+" ")
                    T_M[0][0] = -1*T_M[0][0]
                    T_M[1][0] = -1*T_M[1][0]
                    T_M[2][0] = -1*T_M[2][0]
                P = world_to_camera.world_to_camera(R_M,x.w,T_M)
                x.update_c(P)
                P = world_to_camera.camera_to_world(R_M,x.c,T_M)
                x.update_w(P)
                for i in range(5,12):
                    s_f.write(str(info[0][i])+" ")
                if check_in_camera_ref(R_M,T_M,x.w):
                    s_f.write("1 "+str(P[0][0])+" "+str(P[1][0])+" "+str(P[2][0])+"\n")
                else:
                    s_f.write("0\n")
    s_f.close()
    return

#accelerometer, gyroscope, magnetometer information
def get_reading(time,XC_flag, position_flag):
    result = str(time)+" "+str(XC_flag)+" "
    #add in accelerometer information ax, ay, az
    result += str(random.uniform(-0.5,0.5))+" "+str(random.uniform(-0.5,0.5))+" "+str(random.uniform(-0.5,0.5))
    if XC_flag==1:
        #add in gyroscope information gx, gy, gz
        result += " "+str(random.uniform(-360,360))+" "+str(random.uniform(-360,360))+" "+str(random.uniform(-360,360))+" "
        #add in magnetometer information mx, my, mz
        result += str(random.uniform(-0.5,0.5))+" "+str(random.uniform(-0.5,0.5))+" "+str(random.uniform(-0.5,0.5))
        # if the camera sees X (used only in the case of the first reading of data creation
        if position_flag == 1:
            result += " 1 "+str(random.uniform(0,3))+" "+str(random.uniform(0,3))+" "+str(random.uniform(0,3))
        else:
            result += " 0 "
    return result

def check_in_camera_ref(R,T,W):
    P = world_to_camera.world_to_camera(R,W,T)
    if ((P[0][0] > 0) & (P[1][0] > 0) & (P[2][0] > 0)):
        return 1
    else:
        return 0

#distance = sqrt(x^2 + y^2 + z^2)
#Enforcing the distance to be 3m. Returns 0 if it distance needs to be flipped, 1 otherwise
def distance_flag(Q,d):
    x_square = pow(Q.w[0][0] +d[0][0],2)
    y_square = pow(Q.w[1][0] +d[1][0],2)
    z_square = pow(Q.w[2][0] +d[2][0],2)

    if math.sqrt(x_square+y_square+z_square) > 3.0:
        return 0
    else:
        return 1
