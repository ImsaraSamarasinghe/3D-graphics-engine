'''
AUTHOR: Imsara Samarasinghe
EMAIL: imsara256@gmail.com
'''
# import packages
import math
import pygame

# import files
from transforms import project_3d_to_2d, rotation_matrix, apply_rotation
from config import COLORS, screen

class Cylinder:
    '''
    defines the atrributes for a cylinder

    attributes:
        __init__: Initialises the key dimensions of a cylinder
        _generate_cylinder_vertices: 
        _generate_cylinder_edges
        _generate_cylinder_faces
        draw_cylinder
    '''
    def __init__(self, center=[0,0,0], radius=2, height=5, segments=20, edge_color = COLORS['BLACK'], face_color = COLORS['GREY']):
        '''
        Initialise the class

        :param center: defines the center of the bottom circle in 3D
        :param radius: defines the radius of the cylinder
        :param height: defines the height of the cylinder
        :param segments: defines the numnerb of segments the cylinder is made up of
        :param edge_color: defines the color of the edges
        :param face_color: defines the colors on the faces 
        '''
        self.vertices = self._generate_cylinder_vertices(center, radius, height, segments)
        self.edge_color = edge_color
        self.face_color = face_color

    def _generate_cylinder_vertices(self, center, radius, height, segments):
        '''
        Creates the vertices of the cylinder

        :param center: defines the center point of the bottom circle as a list
        :param radius: defines the radius of the cylinder
        :param height: defines the height of the cylinder
        :param segments: defines the segements into which the cylinder is divided
        :return vertices: outputs list of defined vertices
        '''
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
    
    def _generate_cylinder_edges(self, segments):
        '''
        Creates the edges of the cylinder

        :param segments: defines the segements into which the cylinder is divided
        :return edges: outputs list of edges
        '''
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
    
    def _generate_cylinder_faces(self, segments):
        '''
        Creates the faces of the cylinder defined through vertices

        :param segments: defines the segements into which the cylinder is divided
        :return faces: outputs list of defined faces
        '''
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

    def draw_cylinder(self, angle_x, angle_y, angle_z, viewer_distance):
        '''
        Draws the cylinder using the defines vertices, edges and faces. Also applies transformations

        :param angle_x: angle about x axis
        :param angle_y: angle about y axis
        :param angle_z: angle about z axis
        :param viewer_distance: zoom setting
        '''
        fov = 256
        final_vertices = []
        r_matrix = rotation_matrix(angle_x, angle_y, angle_z)  # Find the rotation matrix for the given angle
        
        # Apply rotation and projection to each vertex
        for vertex in self.vertices:
            aug_vertex = apply_rotation(vertex, r_matrix)
            proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
            final_vertices.append(proj_vertex)
        
        edges = self._generate_cylinder_edges(len(self.vertices) // 2)  # Calculate edges based on vertices count
        faces = self._generate_cylinder_faces(len(self.vertices) // 2)

        # Draw the faces of the cylinder
        for face in faces:
            polygon_points = [final_vertices[i] for i in face]
            pygame.draw.polygon(screen, self.face_color, polygon_points)  # Draw filled face
            
            #pygame.draw.polygon(screen, COLORS['BLACK'], polygon_points, 1)  # Draw outline

        # Draw the edges of the cylinder
        for edge in edges:
            pygame.draw.line(screen, self.edge_color, final_vertices[edge[0]], final_vertices[edge[1]], 2)

class Cube:
    '''
    defines the atrributes for a cube

    attributes:
        __init__: Initialises the key dimensions of a cube
        _generate_cube_vertices 
        _generate_cube_edges
        _generate_cube_faces
        draw_cube
    '''
    def __init__(self, center=[0,0,0], side_length=4, edge_color=COLORS['BLACK'], face_color=COLORS['GREY']):
        '''
        Initialise the class

        :param center: defines the center of the cube in 3D
        :param side_length: defines the length if a side of the cube
        :param edge_color: defines the color of the edges
        :param face_color: defines the colors on the faces 
        '''
        self.vertices = self._generate_cube_vertices(center, side_length)
        self.edges = self._generate_cube_edges()
        self.faces = self._generate_cube_faces()
        self.edge_color = edge_color
        self.face_color = face_color

    def _generate_cube_vertices(self, center, side_length):
        '''
        Creates the vertices of the cube

        :param center: defines the center point of the bottom circle as a list
        :param side_length: defines the length of a side of the cube
        :return vertices: outputs list of defined vertices of the cube
        '''
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
    
    def _generate_cube_edges(self):
        '''
        Creates the edges of the cube

        :return edges: outputs list of edges
        '''
        return [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
        (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]

    def _generate_cube_faces(self):
        '''
        Creates the faces of the cylinder defined through vertices

        :return faces: outputs list of defined faces
        '''
        return [
            (0, 1, 2, 3),  # Front face
            (4, 5, 6, 7),  # Back face
            (0, 1, 5, 4),  # Bottom face
            (2, 3, 7, 6),  # Top face
            (0, 3, 7, 4),  # Left face
            (1, 2, 6, 5),  # Right face
        ]

    def draw_cube(self, angle_x, angle_y, angle_z, viewer_distance):
        '''
        Draws the cube using the defines vertices, edges and faces. Also applies transformations

        :param angle_x: angle about x axis
        :param angle_y: angle about y axis
        :param angle_z: angle about z axis
        :param viewer_distance: zoom setting
        '''
        fov = 256
        final_vertices = []
        r_matrix = rotation_matrix(angle_x, angle_y, angle_z) # find the rotation matrix for the given angle
        for vertex in self.vertices:
            aug_vertex = apply_rotation(vertex, r_matrix)
            proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
            final_vertices.append(proj_vertex)
        

        for face in self.faces:
            polygon_points = [final_vertices[i] for i in face]
            pygame.draw.polygon(screen, self.face_color, polygon_points)  # Draw filled face
        
        for edge in self.edges:
            pygame.draw.line(screen, self.edge_color, final_vertices[edge[0]], final_vertices[edge[1]], 2)

class Torus:

    def __init__(self, center=[0,0,0], R=5, r=2, segments_u=30, segments_v=15, edge_color=COLORS['BLACK']):
        '''
        Initialise the class

        :param center: defines the center of the cube in 3D (default=[0,0,0])
        :param R: Outer radius of the torus (default=5)
        :param r: Inner radius of the torus (default=2)
        :param segments_u: Inner segments
        :param segments_v: Outer segments
        :param edge_color: defines the color of the edges (default=BLACK)
        '''
        self.vertices = self._generate_torus_vertices(center, R, r, segments_u, segments_v)
        self.edges = self._generate_torus_edges(segments_u, segments_v)
        self.edge_color = edge_color

    def _generate_torus_vertices(self, center, R, r, segments_u, segments_v):
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

    def _generate_torus_edges(self, segments_u, segments_v):
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

    def draw_torus(self, angle_x, angle_y, angle_z, viewer_distance):
        '''
        Draws the torus using the defines vertices and edges. Also applies transformations

        :param angle_x: angle about x axis
        :param angle_y: angle about y axis
        :param angle_z: angle about z axis
        :param viewer_distance: zoom setting
        '''
        fov = 256
        final_vertices = []
        r_matrix = rotation_matrix(angle_x, angle_y, angle_z)  # Find the rotation matrix for the given angle
        
        # Apply rotation and projection to each vertex
        for vertex in self.vertices:
            aug_vertex = apply_rotation(vertex, r_matrix)
            proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
            final_vertices.append(proj_vertex)

        # Draw the edges of the cylinder
        for edge in self.edges:
            pygame.draw.line(screen, self.edge_color, final_vertices[edge[0]], final_vertices[edge[1]], 2)

class Sphere:
    '''
    Defines the attributes for a sphere with shading based on light source

    Attributes:
        __init__: Class initialiser
        _generate_sphere_vertices: Function to calculate the vertices for displaying the sphere
        _generate_sphere_faces: Function to calculate the faces for displaying the sphere
        _calculate_face_normal: Calculate the normals from faces
        _calculate_lighting: Calculate the shading from the normals and the direction of the light source
    '''
    def __init__(self, center=[0,0,0], radius=5, segments_lat=30, segments_lon=30, gravity = 0.01, damping = 0.9, face_color=COLORS['GREY'], light_pos=[-50,50,50]):
        '''
        Initialise the class

        :param center: defines the center of the sphere in 3D (default=[0,0,0])
        :param radius: defines the radius of the sphere (default=5)
        :param segments_lat: number of segments for latitude (default=20)
        :param segments_lon: number of segments for longitude (default=20)
        :param face_color: base color of the faces (default=GREY)
        :param light_pos: position of the light source in 3D space (default=[1, 1, 1])
        '''
        # sphere definition
        self.center = center
        self.radius = radius
        self.velocity = [0,0,0] # velocities in the x, y & z directions

        self.gravity = gravity # gravity in the environment
        self.damping = damping # damping factor

        # define the lat and long
        self.segments_lat = segments_lat
        self.segments_lon = segments_lon

        self.vertices = None
        self.faces = None
        self.face_color = face_color
        self.light_pos = light_pos
    
    def _generate_sphere_vertices(self, center, radius, segments_lat, segments_lon):
        '''
        Creates the vertices of the sphere

        :param center: defines the center point of the sphere as a list
        :param radius: defines the radius of the sphere
        :param segments_lat: defines the segments for latitude
        :param segments_lon: defines the segments for longitude
        :return vertices: outputs list of defined vertices
        '''
        cx, cy, cz = center
        vertices = []
        
        for i in range(segments_lat + 1):  # Latitude lines
            theta = math.pi * i / segments_lat  # Polar angle
            for j in range(segments_lon):  # Longitude lines
                phi = 2 * math.pi * j / segments_lon  # Azimuthal angle
                
                # Calculate the vertex coordinates in 3D space
                x = cx + radius * math.sin(theta) * math.cos(phi)
                y = cy + radius * math.sin(theta) * math.sin(phi)
                z = cz + radius * math.cos(theta)
                
                vertices.append([x, y, z])
        
        return vertices

    def _generate_sphere_faces(self, segments_lat, segments_lon):
        '''
        Creates the faces of the sphere as quads

        :param segments_lat: defines the segments for latitude
        :param segments_lon: defines the segments for longitude
        :return faces: outputs list of faces defined by vertex indices
        '''
        faces = []
        
        for i in range(segments_lat):
            for j in range(segments_lon):
                # Current vertex index
                current = i * segments_lon + j
                next_lon = (j + 1) % segments_lon  # Wrap longitude

                # Define the four corners of the quad face
                top_left = current
                top_right = i * segments_lon + next_lon
                bottom_left = (i + 1) * segments_lon + j
                bottom_right = (i + 1) * segments_lon + next_lon

                # Add the face as a quad (polygon with 4 vertices)
                faces.append([top_left, top_right, bottom_right, bottom_left])
        
        return faces
    
    def _calculate_face_normal(self, face):
        '''
        Calculates the normal vector of a face (quad) defined by 4 vertices

        :param face: list of 4 vertex indices that define the face
        :return normal: normal vector of the face
        '''
        v0 = self.vertices[face[0]]
        v1 = self.vertices[face[1]]
        v2 = self.vertices[face[2]]

        # Calculate vectors for two edges of the quad
        edge1 = [v1[i] - v0[i] for i in range(3)]
        edge2 = [v2[i] - v0[i] for i in range(3)]
        
        # Cross product of edge1 and edge2 gives the face normal
        normal = [edge1[1] * edge2[2] - edge1[2] * edge2[1],
                  edge1[2] * edge2[0] - edge1[0] * edge2[2],
                  edge1[0] * edge2[1] - edge1[1] * edge2[0]]
        
        # Normalize the normal
        length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        if length != 0:
            normal = [n / length for n in normal]
        
        return normal

    def _calculate_lighting(self, normal):
        '''
        Calculates the shading value based on the normal and the light source

        :param normal: normal vector of the face
        :return brightness: brightness factor for shading (between 0 and 1)
        '''
        # Light direction (can be normalized)
        light_dir = self.light_pos
        light_length = math.sqrt(light_dir[0]**2 + light_dir[1]**2 + light_dir[2]**2)
        light_dir = [l / light_length for l in light_dir]

        # Dot product between the normal and light direction
        dot_product = max(0, normal[0] * light_dir[0] + normal[1] * light_dir[1] + normal[2] * light_dir[2])
        return dot_product

    def draw_sphere(self, angle_x, angle_y, angle_z, viewer_distance):
        '''
        Draws the sphere using the defined vertices, faces and applies lighting and shading

        :param angle_x: angle about x axis
        :param angle_y: angle about y axis
        :param angle_z: angle about z axis
        :param viewer_distance: zoom setting
        '''
        fov = 256 # field of view
        final_vertices = [] # store the projected vertices
        self.vertices = self._generate_sphere_vertices(self.center,
                                                       self.radius,
                                                       self.segments_lat,
                                                       self.segments_lon) # generate vertices for sphere 
        
        r_matrix = rotation_matrix(angle_x, angle_y, angle_z)  # Find the rotation matrix for the given angle
        
        # Apply rotation and projection to each vertex
        for vertex in self.vertices:
            aug_vertex = apply_rotation(vertex, r_matrix)
            proj_vertex = project_3d_to_2d(aug_vertex, fov, viewer_distance)
            final_vertices.append(proj_vertex)

        self.faces = self._generate_sphere_faces(self.segments_lat,self.segments_lon) # generate faces

        # Draw the faces of the sphere
        for face in self.faces:
            polygon_points = [final_vertices[i] for i in face]
            
            # Calculate the normal of the face
            normal = self._calculate_face_normal(face)
            normal_rotated = apply_rotation(normal, r_matrix)
            
            # Determine lighting for the face
            brightness = self._calculate_lighting(normal_rotated)
            
            # Shade the face based on lighting (darker color with less brightness)
            shaded_color = [min(255, max(0, int(c * brightness))) for c in self.face_color]  # Assuming GREY is a tuple like (r, g, b)
            
            # Draw the shaded face
            pygame.draw.polygon(screen, shaded_color, polygon_points)
    
    def _apply_gravity(self):
        self.velocity[1] += -self.gravity # Increase the velocity downwards
    
    def _floor_collisions(self):
        # Handle floor collision
        if self.center[1] - self.radius < 0:
            self.center[1] = self.radius
            self.velocity[1] = -self.velocity[1] * self.damping  # Bounce with damping

    def update_ball_position(self, angle_x, angle_y, angle_z, viewer_distance):
        self._apply_gravity() # add acceleration downwards
        # Update ball position in 3D
        self.center[1] += self.velocity[1]  # Update y (vertical movement)
        self._floor_collisions() # check for floor collisions
        self.draw_sphere(angle_x, angle_y, angle_z, viewer_distance) # draw the sphere at the new sphere
