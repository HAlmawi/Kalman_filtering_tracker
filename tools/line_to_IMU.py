#IMU data format ax, ay, az, gz, gy, gz, ma, my, mz
# Example IMU is MPU9250. Accelerometer measured in g (9.8 m/s2)
def line_to_IMU(lines):
    rate = len(lines)
    for line in lines:
        nums = line.split()
