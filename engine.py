import pygame
import sys
import math
from shapes import *

# initialise
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D CAD Visualization")

##### Colors #####
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
GREY = (128, 128, 128)

def generate_axis_vertices(center, side_length):
    cx, cy, cz = center
    # Create vertices for each axis, offset by the center coordinates
    vertices = [
        [cx, cy, cz],                  # Origin (0,0,0)
        [cx + side_length, cy, cz],   # X-axis end (side_length, 0, 0)
        [cx, cy, cz],                  # Origin (0,0,0)
        [cx, cy + side_length, cz],   # Y-axis end (0, side_length, 0)
        [cx, cy, cz],                  # Origin (0,0,0)
        [cx, cy, cz + side_length]     # Z-axis end (0, 0, side_length)
    ]
    return vertices

def generate_axis_edges():

    return [(0,1),(2,3),(4,5)]

# function for defining the rotation matrix
def rotation_matrix(angle_x,angle_y,angle_z):
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
    coords = [[x] for x in vertex]
    result = [[sum(a * b for a, b in zip(A_row, B_col)) 
                        for B_col in zip(*coords)]
                                for A_row in rotation_matrix]
    return [x[0] for x in result]

# function to project point in 3D to 2D
def project_3d_to_2d(point3d, fov, viewer_distance):
    factor = fov / (viewer_distance + point3d[2])
    x = point3d[0] * factor + width / 2
    y = -point3d[1] * factor + height / 2
    return (int(x), int(y))


def draw_axes(axes_vertices, angle_x, angle_y, angle_z, viewer_distance):
    fov = 256
    final_vertices = []
    r_matrix = rotation_matrix(angle_x, angle_y, angle_z) # find the rotation matrix for the given angle
    for vertex in axes_vertices:
        aug_vertex = apply_rotation(vertex, r_matrix)
        proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
        final_vertices.append(proj_vertex)

    # Draw the edges of the cube
    edges = generate_axis_edges()
    colors = [RED,GREEN,BLUE]
    for i, edge in enumerate(edges):
        pygame.draw.line(screen, colors[i], final_vertices[edge[0]], final_vertices[edge[1]], 2)
    pygame.draw.circle(screen, RED, (400,300), 4) # center point of the cube

def main():
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0
    run = True
    rotating = False
    last_mouse_pos = None
    viewer_distance = 20
    while run:
        screen.fill(WHITE) # screen background

        # loop for closing the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left mouse click
                rotating = True
                last_mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                rotating = False
            if event.type == pygame.MOUSEMOTION and rotating: # calculate the angles
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0]-last_mouse_pos[0]
                dy = current_mouse_pos[1] - last_mouse_pos[1]

                # create angles
                angle_x += dy * 0.01
                angle_y += dx * 0.01

                last_mouse_pos = current_mouse_pos
            if event.type == pygame.MOUSEWHEEL:
                viewer_distance += event.y
        
        # vertices
        cube_vertices_1 = generate_cube_vertices(center=[0,0,0], side_length = 3)
        cube_vertices_2 = generate_cube_vertices(center=[0,0,-4],side_length=1)
        cylinder_vertices = generate_cylinder_vertices([0,0,0],3,5,100)
        cylinder = generate_cylinder_vertices([5,3,-6],1,10,100)
        torus_1 = generate_torus_vertices([0,0,0],2,0.5,30,15)
        
        # draw
        #draw_cube(cube_vertices_1, angle_x, angle_y, angle_z, viewer_distance)
        draw_cube(cube_vertices_2, angle_x, angle_y, angle_z, viewer_distance)
        #draw_cylinder(cylinder_vertices, angle_x, angle_y, angle_z, viewer_distance)
        draw_cylinder(cylinder, angle_x, angle_y, angle_z, viewer_distance)
        draw_torus(torus_1, angle_x, angle_y, angle_z, viewer_distance, 30, 15)
      
        ## axes ##
        axes_vertices = generate_axis_vertices(center=[0,0,0], side_length = 0.5)
        draw_axes(axes_vertices, angle_x, angle_y, angle_z, viewer_distance) # draw the axes at the center point
        ##########

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit

if __name__ == '__main__':
    main()

