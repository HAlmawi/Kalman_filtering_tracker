import sys
sys.path.append('./')
import data_functions

#Purpose of this function is to create the data needed to run the program

#Inputs:
# 1-  Filename: the name of the file to write the initial readings from
# 2- save_filename: file that ensures that the specifications below are met
# 3- rate: the rate of IMU data readings in seconds
# 4- num_readings: the number of readings from each IMU

# Outputs:
# 1- save_filename: A file with readings that includes positions of X when it is visible in C, and ensures specifications are met

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
    num_readings = 250 # 250 readings from each device

    # Creating the filename file with readings
    data_functions.randomize_readings(filename,rate,num_readings)
    # Enforcing the specifications on the readings
    data_functions.enforce_specifications(filename,rate,save_filename)