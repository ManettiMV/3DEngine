import math
import numpy as np

"""
Basic matrixes that make specified things.
https://en.wikipedia.org/wiki/Rotation_matrix
https://www.brainvoyager.com/bv/doc/UsersGuide/CoordsAndTransforms/SpatialTransformationMatrices.html
"""
cos = math.cos
sin = math.sin

def translate(pos):
    tx, ty, tz = pos
    return np.array([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [tx,ty,tz,1]
    ])

def rotate_x(n):
    return np.array([
        [1,0,0,0],
        [0,cos(n),sin(n),0],
        [0,-sin(n),cos(n),0],
        [0,0,0,1]
    ])

def rotate_y(n):
    return np.array([
        [cos(n),0,-sin(n),0],
        [0,1,0,0],
        [sin(n),0,cos(n),0],
        [0,0,0,1]
    ])

def rotate_z(n):
    return np.array([
        [cos(n),sin(n),0,0],
        [-sin(n),cos(n),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])

def scale(n):
    return np.array([
        [n,0,0,0],
        [0,n,0,0],
        [0,0,n,0],
        [0,0,0,1]
    ])