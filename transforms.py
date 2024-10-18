'''
AUTHOR: Imsara Samarasinghe
EMAIL: imsara256@gmail.com
'''
# module Imports
import math

# file imports
from config import width, height

# function for defining the rotation matrix
def rotation_matrix(angle_x,angle_y,angle_z):
    '''
    function to create the rotation matrix. Created by pre-multiplyin the matrices
    defining rotations around the x, y & z axes.

    :param angle_x: angle change about the x axis
    :param angle_y: angle change about the y axis
    :param angle_z: angle change about the z axis
    :return matrix: rotation matrix with all angles applied
    '''
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)

    matrix = [
        [cos_y*cos_z, -cos_y*sin_z, sin_y],
        [sin_x * sin_y * cos_z + cos_x * sin_z, -sin_x * sin_y * sin_z + cos_x * cos_z, -sin_x * cos_y],
        [-cos_x * sin_y * cos_z + sin_x * sin_z, cos_x * sin_y * sin_z + sin_x * cos_z, cos_x * cos_y]
        ]
    return matrix

# function for applying the rotation matrix to a vertex
def apply_rotation(vertex, rotation_matrix):
    '''
    Function to preform the matrix multiplication between rotation matrix
    and a vertex point

    :param vertex: 3D coordinate of the vertex as a list ex: [1,2,3]
    :param rotation_matrix: The matrix with all angles applied
    :return: rotated vertex as a list ex: [1,2,3] 
    '''
    coords = [[x] for x in vertex]
    result = [[sum(a * b for a, b in zip(A_row, B_col)) 
                        for B_col in zip(*coords)]
                                for A_row in rotation_matrix]
    return [x[0] for x in result]

# function to project point in 3D to 2D
def project_3d_to_2d(point3d, fov, viewer_distance):
    '''
    function to peform the tranformation between 3D coordinates to 2D coordinates

    :param point3D: Vertex point in 3D coordinates
    :param fov: Field of view of the user
    :param viewer_distance: Zoom setting for the user
    :return:(x, y) tuple of integer 2D coordinates to be used with PyGame interface
    '''
    factor = fov / (viewer_distance + point3d[2])
    x = point3d[0] * factor + width / 2
    y = -point3d[1] * factor + height / 2
    return (int(x), int(y))