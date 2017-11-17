#IMU data format:
# 1- X: timestamp XCflag=0 ax ay az
# 2- C without X position: timestamp XCflag=1 ax ay az gx gy gz mx my mz pos_flag=0
# 3- C with X position: timestamp XCflag=1 ax ay az gx gy gz mx my mz pos_flag=1 pos_x pos_y pos_z

# Function line_to_IMU(line) tokenizes line of readings for quaternion and/or distance calculations, etc

# Input:
# 1- line: a single line from the readings file

# Output:
# 1- imu_info: list of tokenized readings

def line_to_IMU(line):
    num = len(line.split())
    imu_info = [[0]*num]
    count = 0
    tokens = line.split()
    for word in tokens:
        imu_info[0][count]=word
        count = count+ 1
    return imu_info
