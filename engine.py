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
###################

def generate_axis_vertices(center, side_length):
    '''
    Generate the vertices for the axis lines

    :param center: list or tuple of the coordinates in 3D for the center location for the axes to be displayed
    :param side_length: Define the length of the axes to be drawn
    :return vertices: list of vertices (list of 3D coordinates) defining the axes 
    '''
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
    '''
    Define the edges that connect the vertex points
    '''
    return [(0,1),(2,3),(4,5)]

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

# function for drawing the axes and the center point of the screen
def draw_axes(axes_vertices, angle_x, angle_y, angle_z, viewer_distance):
    '''
    function to draw the axes from the generated axes vertices and edges,
    after rotations and projections

    :param axes_vertices: list of axes vertices in 3D i.e [[1,2,3],[4,5,6],....]
    :param angle_x: angle change about x axis
    :param angle_y: angle change about y axis
    :param angle_z: angle change about z axis
    :param viewer_distance: set the zoom level based on the scrollwheel input
    '''
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
    pygame.draw.circle(screen, RED, (width/2,height/2), 4) # center point of the cube

def main():
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0 # Initialise angles
    run = True # variable for sim window
    rotating = False # variable for finding roation status
    last_mouse_pos = None # store last know mouse position
    viewer_distance = 20 # initialise zoom
    while run:
        screen.fill(WHITE) # screen background

        # event loop for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # close simulation
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # find left mouse click position
                rotating = True
                last_mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # find the left mouse button up
                rotating = False
            if event.type == pygame.MOUSEMOTION and rotating: # calculate the angles based on mouse positions
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0]-last_mouse_pos[0]
                dy = current_mouse_pos[1] - last_mouse_pos[1]

                # create angles
                angle_x += dy * 0.01
                angle_y += dx * 0.01

                last_mouse_pos = current_mouse_pos
            if event.type == pygame.MOUSEWHEEL: # change zoom based on the scrollwheel
                viewer_distance += event.y
            # Check for the fullscreen toggle event
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                # Toggle fullscreen mode
                pygame.display.toggle_fullscreen()
        
        # Define the vertices of the shape
        cube_1 = generate_cube_vertices(center=[0,0,0],side_length=3)
        torus = generate_torus_vertices(center=[0,0,10], R=5, r=2, segments_u=50, segments_v=30)
        cylinder = generate_cylinder_vertices(center=[0,0,-10],radius=2,height=6,segments=40)
        
        # Draw using the defined vertices
        draw_cube(cube_1, angle_x, angle_y, angle_z, viewer_distance)
        draw_torus(torus, angle_x, angle_y, angle_z, viewer_distance, seg_u=50, seg_v=30)
        draw_cylinder(cylinder, angle_x, angle_y, angle_z, viewer_distance)

        ## axes ##
        axes_vertices = generate_axis_vertices(center=[0,0,0], side_length = 0.5)
        draw_axes(axes_vertices, angle_x, angle_y, angle_z, viewer_distance) # draw the axes at the center point
        ##########

        pygame.display.flip() # Update the screen
        clock.tick(60) # set refresh rate

    pygame.quit()
    sys.exit

if __name__ == '__main__':
    main()

