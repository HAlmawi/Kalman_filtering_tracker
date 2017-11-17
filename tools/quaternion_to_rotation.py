# Function quaternion2rotation(q): transforms quaternion to rotation matrix
# Input: q the quaternion
# Output: R the rotation matrix
def quaternion2rotation(q):
    R = [[0 for x in range(3)] for y in range(3)]

    R[0][0] = 2*pow(q[0][0],2)-1+2*pow(q[1][0],2)
    R[0][1] = 2*(q[1][0]*q[2][0]+q[0][0]*q[3][0])
    R[0][2] = 2*(q[1][0]*q[3][0]-q[0][0]*q[2][0])
    R[1][0] = 2*(q[1][0]*q[2][0]-q[0][0]*q[3][0])
    R[1][1] = 2*pow(q[0][0],2)-1+2*pow(q[2][0],2)
    R[1][2] = 2*(q[2][0]*q[3][0]+q[0][0]*q[1][0])
    R[2][0] = 2*(q[1][0]*q[3][0]+q[0][0]*q[2][0])
    R[2][1] = 2*(q[2][0]*q[3][0]-q[0][0]*q[1][0])
    R[2][2] = 2*pow(q[0][0],2)-1+2*pow(q[3][0],2)
    return R
