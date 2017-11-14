#IMU data format timestamp ax, ay, az, gz, gy, gz, ma, my, mz
# Example IMU is MPU9250. Accelerometer measured in g (9.8 m/s2)
def line_to_IMU(line):
    num = len(line.split())
    imu_info = [0]*num
    count = 0
    for word in line.split():
        imu_info[count]=word
        count = count+ 1

    return imu_info
