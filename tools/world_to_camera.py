import sys
sys.path.append('.')
import math_functions

# world_to_camera(R,P,T): transforms world coordinates to camera coordinates
# Input: R,P,T: the Rotation matrix, World coordinates, and Translation matrix
# Output: the camera coordinates
def world_to_camera(R,P,T):
    return math_functions.matrix_multiply(R,math_functions.matrix_addition(P,math_functions.matrix_coeff_mult(T,-1)))

# camera_to_world(R,P,T): transforms camera coordinates to world coordinates
# Input: R,P,T: the Rotation matrix, camera coordinates, and Translation matrix
# Output: the world coordinates
def camera_to_world(R,P,T):
    return math_functions.matrix_addition(math_functions.matrix_multiply(R,P),T)
