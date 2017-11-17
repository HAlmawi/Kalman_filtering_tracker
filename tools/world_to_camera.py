import sys
sys.path.append('.')
import math_functions

def world_to_camera(R,P,T):
    return math_functions.matrix_multiply(R,math_functions.matrix_addition(P,math_functions.matrix_coeff_mult(T,-1)))

def camera_to_world(R,P,T):
    return math_functions.matrix_addition(math_functions.matrix_multiply(R,P),T)
