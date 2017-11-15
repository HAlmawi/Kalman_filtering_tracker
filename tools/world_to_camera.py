import sys
sys.path.append('./')
from . import math_functions

def world_to_camera(R,P,T):
    return math_function.matrix_multiply(R,math_function.matrix_addition(P,math_function.matrix_coeff_mult(T,-1)))

def camera_to_world(R,P,T):
    return math_function.matrix_addition(math_functions.matrix_multiply(R,P),T)
