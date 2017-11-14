import sys
sys.path.append('./tools/')
from itertools import islice
from tools import line_to_IMU

def main():
    filename = ""
    rate = 6
    with open(filename, 'r') as infile:
        lines = filename.readlines()
    for line in lines:
        line_to_IMU(line)
    infile.close()

if __name__ == "__main__":
    main()