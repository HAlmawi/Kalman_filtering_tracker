import sys
sys.path.append('./tools/')
from data_creation import line_to_IMU


def main():
    filename = ""
    rate = 1.0/30.0
    with open(filename, 'r') as infile:
        lines = filename.readlines()
    for line in lines:
        line_to_IMU(line)
    infile.close()

if __name__ == "__main__":
    main()