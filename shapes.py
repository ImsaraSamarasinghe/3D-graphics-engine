import math
import pygame
from engine import *
'''
AUTHOR: Imsara Samarasinghe
EMAIL: imsara256@gmail.com
'''

######## CYLINDER #######

# Function to generate vertices for a cylinder
def generate_cylinder_vertices(center, radius, height, segments):
    cx, cy, cz = center
    vertices = []
    
    # Generate vertices for both top and bottom circles
    for i in range(segments):
        angle = (2 * math.pi / segments) * i
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        
        # Bottom circle vertex
        vertices.append([x, y, cz])  
        # Top circle vertex
        vertices.append([x, y, cz + height])  
    
    return vertices


# Function to define edges of the cylinder
def generate_cylinder_edges(segments):
    edges = []
    # Connect the bottom circle
    for i in range(segments):
        edges.append((i * 2, ((i + 1) % segments) * 2))  # Bottom edges
    # Connect the top circle
    for i in range(segments):
        edges.append((i * 2 + 1, ((i + 1) % segments) * 2 + 1))  # Top edges
    # Connect top and bottom circles
    for i in range(segments):
        edges.append((i * 2, i * 2 + 1))  # Side edges
    return edges

def generate_cylinder_faces(segments):
    faces = []
    
    # Top face
    top_face = [i * 2 + 1 for i in range(segments)]
    faces.append(top_face)

    # Bottom face
    bottom_face = [i * 2 for i in range(segments)]
    faces.append(bottom_face)

    # Side faces
    for i in range(segments):
        next_i = (i + 1) % segments
        faces.append([i * 2, next_i * 2, next_i * 2 + 1, i * 2 + 1])  # Rectangle between bottom and top
        
    return faces

def draw_cylinder(vertices, angle_x, angle_y, angle_z, viewer_distance):
    fov = 256
    final_vertices = []
    r_matrix = rotation_matrix(angle_x, angle_y, angle_z)  # Find the rotation matrix for the given angle
    
    # Apply rotation and projection to each vertex
    for vertex in vertices:
        aug_vertex = apply_rotation(vertex, r_matrix)
        proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
        final_vertices.append(proj_vertex)

    edges = generate_cylinder_edges(len(vertices) // 2)  # Calculate edges based on vertices count
    faces = generate_cylinder_faces(len(vertices) // 2)

    # Draw the faces of the cylinder
    for face in faces:
        polygon_points = [final_vertices[i] for i in face]
        pygame.draw.polygon(screen, GREY, polygon_points)  # Draw filled face
        pygame.draw.polygon(screen, BLACK, polygon_points, 1)  # Draw outline

    # Draw the edges of the cylinder
    for edge in edges:
        pygame.draw.line(screen, BLACK, final_vertices[edge[0]], final_vertices[edge[1]], 2)

#####################################

######### CUBE ###########
# function for defining a cube
def generate_cube_vertices(center, side_length):
    # Half the side length to calculate the offsets from the center
    half_side = side_length / 2
    
    # Unpack center coordinates
    cx, cy, cz = center
    
    # Define all 8 vertices based on center and offsets
    vertices = [
        [cx - half_side, cy - half_side, cz - half_side],  # Vertex 0
        [cx + half_side, cy - half_side, cz - half_side],  # Vertex 1
        [cx + half_side, cy + half_side, cz - half_side],  # Vertex 2
        [cx - half_side, cy + half_side, cz - half_side],  # Vertex 3
        [cx - half_side, cy - half_side, cz + half_side],  # Vertex 4
        [cx + half_side, cy - half_side, cz + half_side],  # Vertex 5
        [cx + half_side, cy + half_side, cz + half_side],  # Vertex 6
        [cx - half_side, cy + half_side, cz + half_side],  # Vertex 7
    ]
    
    return vertices

def generate_cube_faces():
    return [
        (0, 1, 2, 3),  # Front face
        (4, 5, 6, 7),  # Back face
        (0, 1, 5, 4),  # Bottom face
        (2, 3, 7, 6),  # Top face
        (0, 3, 7, 4),  # Left face
        (1, 2, 6, 5),  # Right face
    ]

# puts all processes together to create the projection and draw
def draw_cube(cube_vertices, angle_x, angle_y, angle_z, viewer_distance):
    fov = 256
    final_vertices = []
    r_matrix = rotation_matrix(angle_x, angle_y, angle_z) # find the rotation matrix for the given angle
    for vertex in cube_vertices:
        aug_vertex = apply_rotation(vertex, r_matrix)
        proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
        final_vertices.append(proj_vertex)
    
    faces = generate_cube_faces()

    for face in faces:
        polygon_points = [final_vertices[i] for i in face]
        pygame.draw.polygon(screen, GREY, polygon_points)  # Draw filled face
        #pygame.draw.polygon(screen, BLACK, polygon_points, 1)  # Draw outline

    # Draw the edges of the cube
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
        (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
    ]
    
    
    for edge in edges:
        pygame.draw.line(screen, BLACK, final_vertices[edge[0]], final_vertices[edge[1]], 2)
    

##########################


################ TORUS #################
def generate_torus_vertices(center, R, r, segments_u, segments_v):
    """
    Generate vertices for a torus.
    
    :param center: Tuple of the center coordinates (cx, cy, cz).
    :param R: Major radius (distance from the center of the tube to the center of the torus).
    :param r: Minor radius (radius of the tube).
    :param segments_u: Number of segments around the tube.
    :param segments_v: Number of segments along the torus.
    :return: List of vertices.
    """
    cx, cy, cz = center
    vertices = []
    
    for i in range(segments_u):
        for j in range(segments_v):
            u = (i / segments_u) * 2 * math.pi  # Angle around the tube
            v = (j / segments_v) * 2 * math.pi  # Angle along the torus
            
            # Calculate the vertex position
            x = (R + r * math.cos(v)) * math.cos(u)
            y = (R + r * math.cos(v)) * math.sin(u)
            z = r * math.sin(v)
            
            # Append the vertex to the list
            vertices.append([cx + x, cy + y, cz + z])
    
    return vertices

def generate_torus_edges(segments_u, segments_v):
    """
    Generate edges for a torus.
    
    :param segments_u: Number of segments around the tube.
    :param segments_v: Number of segments along the torus.
    :return: List of edges defined by vertex indices.
    """
    edges = []
    
    for i in range(segments_u):
        for j in range(segments_v):
            # Current vertex index
            current = i * segments_v + j
            next_u = ((i + 1) % segments_u) * segments_v + j  # Wrap around u
            next_v = i * segments_v + ((j + 1) % segments_v)  # Wrap around v
            
            # Add edges for u direction
            edges.append((current, next_u))  # Connect to next in u direction
            
            # Add edges for v direction
            edges.append((current, next_v))  # Connect to next in v direction
    
    return edges

def draw_torus(vertices, angle_x, angle_y, angle_z, viewer_distance, seg_u, seg_v):
    fov = 256
    final_vertices = []
    r_matrix = rotation_matrix(angle_x, angle_y, angle_z)  # Find the rotation matrix for the given angle
    
    # Apply rotation and projection to each vertex
    for vertex in vertices:
        aug_vertex = apply_rotation(vertex, r_matrix)
        proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
        final_vertices.append(proj_vertex)

    edges = generate_torus_edges(seg_u,seg_v)  # Calculate edges based on vertices count

    # Draw the edges of the cylinder
    for edge in edges:
        pygame.draw.line(screen, GREY, final_vertices[edge[0]], final_vertices[edge[1]], 2)

