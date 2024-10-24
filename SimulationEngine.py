'''
AUTHOR: Imsara Samarasinghe
E-MAIL: imsara256@gmail.com
'''
# Imports
import pygame
import sys
import math

# self defined
from config import screen, COLORS # IMPORT params
from background import Axes, Floor # IMPORT Axes class
from text import print_angles, print_zoom

class Engine:
    '''
    Class for defining the graphics engine that handles events and  
    manages shapes

    Attributes:
        __init__: Class initialiser
        _add_balls: Shape manager for spheres
        _add_shapes: Shape manager for other shapes
        _handle_events: Handle mouse, keyboards and other events
        runEngine: Simulation loop
    '''
    def __init__(self, angle_x=0, angle_y=0, angle_z=0, viewer_distance=60):
        '''
        Class initialiser - initialise pygame and other essential variables 
                            as well as background classes

        :param angle_x: Initial angle about the x-axis
        :param angle_y: Intital angle about the y-axis
        :param angle_z: Initial angle about the z-axis
        :param viewer_distance: Zoom setting
        '''
        pygame.init() # initiliase pygame
        self.clock = pygame.time.Clock() # set pygame clock
        self.angle_x, self.angle_y, self.angle_z = angle_x, angle_y, angle_z # Initialise angles
        self.run = True # variable for running the simulation loop
        self.rotating = False # variable for finding roation status
        self.last_mouse_pos = None # store last know mouse position
        self.viewer_distance = viewer_distance # initialise zoom

        # background objects
        self.ax = Axes(side_length=5) # axes object
        self.ground = Floor(side_length=50) # floor object

        # list for storing objects
        self.balls = []
        self.shapes = []

    def _add_balls(self, shape):
        '''
        shape manager for spherical objects

        :param shape: Accepts Sphere class object
        '''
        self.balls.append(shape)
    
    def _add_shapes(self, shape):
        '''
        shape manager for all other shapes

        :param shape: Accepts other defined shape classes
        '''
        self.shapes.append(shape)

    def _handle_events(self):
        '''
        Handles all in game events and user inputs. Uses pygame event handlers.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # close simulation
                self.run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # find left mouse click position
                self.rotating = True
                self.last_mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # find the left mouse button up
               self.rotating = False

            if event.type == pygame.MOUSEMOTION and self.rotating: # calculate the angles based on mouse positions
                current_mouse_pos = pygame.mouse.get_pos()
                dx = current_mouse_pos[0] - self.last_mouse_pos[0]
                dy = current_mouse_pos[1] - self.last_mouse_pos[1]

                # create angles
                self.angle_x += dy * 0.01
                self.angle_y += dx * 0.01

                self.last_mouse_pos = current_mouse_pos

            if event.type == pygame.MOUSEWHEEL: # change the zoom based on the scrollwheel
                self.viewer_distance += event.y

            # Check for the fullscreen toggle event
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                # Toggle fullscreen mode
                pygame.display.toggle_fullscreen()
            
            # Isometric screen format
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.viewer_distance = 60
                self.angle_x = math.radians(-35.26)
                self.angle_y = math.radians(45)
                self.angle_z = 0

            # reset all angles to zero - front view
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.angle_x = 0
                self.angle_y = 0
                self.angle_z = 0
    
    def runEngine(self):
        '''
        Runs the main simulation loop. Uses shape managers for drawing.
        '''
        while self.run:
            screen.fill(COLORS['GREY']) # screen background
            print_zoom(self.viewer_distance)
            print_angles(self.angle_x, self.angle_y, self.angle_z)
            # event loop for pygame events
            self._handle_events()
            # Draw ground
            self.ground.draw_floor(self.angle_x, self.angle_y, self.angle_z, self.viewer_distance)
            
            # deploy sphere
            for ball in self.balls:
                ball.update_ball_position(self.angle_x, self.angle_y, self.angle_z, self.viewer_distance)

            # deploy other shapes
            for shape in self.shapes:
                shape.draw_shape(self.angle_x, self.angle_y, self.angle_z, self.viewer_distance)

            # draw axes
            self.ax.draw_axes(self.angle_x, self.angle_y, self.angle_z, self.viewer_distance)

            pygame.display.flip() # Update the screen
            self.clock.tick(60) # set refresh rate

        pygame.quit() # close the window
        sys.exit

