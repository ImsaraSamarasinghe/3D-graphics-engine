import pygame
from transforms import project_3d_to_2d, rotation_matrix, apply_rotation
from config import COLORS, screen, width, height

class Axes:

    def __init__(self, center = [0,0,0], side_length=10):
        self.vertices = self._generate_axis_vertices(center, side_length)
    
    def _generate_axis_vertices(self, center, side_length):
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
    
    def _generate_axis_edges(self):
        '''
        Define the edges that connect the vertex points
        '''
        return [(0,1),(2,3),(4,5)]
    
    def draw_axes(self, angle_x, angle_y, angle_z, viewer_distance):
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
        for vertex in self.vertices:
            aug_vertex = apply_rotation(vertex, r_matrix)
            proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
            final_vertices.append(proj_vertex)

        # Draw the edges of the axes
        edges = self._generate_axis_edges()
        colors = [COLORS['RED'],COLORS['GREEN'],COLORS['BLUE']]
        for i, edge in enumerate(edges):
            pygame.draw.line(screen, colors[i], final_vertices[edge[0]], final_vertices[edge[1]], 2)
        
        # Draw center of sim
        pygame.draw.circle(screen, COLORS['RED'], (width/2,height/2), 4) # center point of the screen

class Floor:

    def __init__(self, center=[0,0,0], side_length=30):
        self.vertices = self._generate_floor_vertices(center,side_length)

    def _generate_floor_vertices(self,center,side_length):
        cx, _, cz = center
        return [
                [cx-side_length/2,0,cz-side_length/2],
                [cx+side_length/2,0,cz-side_length/2],
                [cx+side_length/2,0,cz+side_length/2],
                [cx-side_length/2,0,cz+side_length/2]
                ]
    
    def _generate_floor_edges(self):
        return [(0,1),(1,2),(2,3),(3,0)]
    
    def _generate_floor_face(self):
        return [(0,1,2,3)]
    
    def draw_floor(self, angle_x, angle_y, angle_z, viewer_distance):
        alpha = 128
        fov=256
        final_vertices = []
        r_matrix = rotation_matrix(angle_x,angle_y,angle_z)
        floor_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for vertex in self.vertices:
            aug_vertex = apply_rotation(vertex, r_matrix)
            proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
            final_vertices.append(proj_vertex)

        faces = self._generate_floor_face()
        face_color = COLORS['P_BLUE']
        for face in faces:
            polygon_points = [final_vertices[i] for i in face]
            pygame.draw.polygon(floor_surface, (face_color[0], face_color[1], face_color[2], alpha), polygon_points)
        
        screen.blit(floor_surface, (0, 0))