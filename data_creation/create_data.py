import sys
sys.path.append('./')
import data_functions

#create data

#Data specifications:
# 1- IMU readings are not synchronized
# 2- C provides occasional 3D positional information for X in C's coordinate (noisy and only available when C sees X)
# 3- X's IMU only broadcasts accelerometer information
# 4- Sensors are tracked within range of 3m
# 5- Lag has been calibrated for IMU devices and 3D positional information
# 6- X and C are held by two different people

def create_data():
    filename = "./readings.txt" #Name of file to save in the readings from
    save_filename = "./result_readings.txt" #Name of file to save in the readings from
    rate = 1.0/30.0 #Rate of IMU data is 30 Hz
    num_readings = 250 # 1 minute of readings from each device

    data_functions.randomize_readings(filename,rate,num_readings)
    # include_camera_readings(filename)
    data_functions.enforce_specifications(filename,rate,save_filename)