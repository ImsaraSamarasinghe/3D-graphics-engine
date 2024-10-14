# module imports
import pygame
import sys
import math

# self defined
from shapes import Cylinder, Cube, Torus
from config import screen, COLORS # IMPORT params
from background import Axes, Floor # IMPORT Axes class

# initialise
pygame.init()

def main():
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0 # Initialise angles
    run = True # variable for sim window
    rotating = False # variable for finding roation status
    last_mouse_pos = None # store last know mouse position
    viewer_distance = 20 # initialise zoom

    # background objects
    ax = Axes()
    ground = Floor()

    # shapes class
    cylinder = Cylinder(center=[0,0,-10], edge_color=(10,128,95))
    cube = Cube(center=[0,10,0], face_color=COLORS['P_ORANGE'])
    torus = Torus(center=[0,0,10], edge_color=COLORS['P_RED'])

    while run:
        screen.fill(COLORS['BACKGROUND_COLOR']) # screen background

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
            
            # Isometric screen format
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                viewer_distance = 60
                angle_x = math.radians(-35.26)
                angle_y = math.radians(45)
                angle_z = 0

            # reset all angles to zero 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                angle_x = 0
                angle_y = 0
                angle_z = 0
        
        # Draw ground
        ground.draw_floor(angle_x, angle_y, angle_z, viewer_distance)


        # Draw using the defined vertices
        torus.draw_torus(angle_x, angle_y, angle_z, viewer_distance)
        cylinder.draw_cylinder(angle_x, angle_y, angle_z, viewer_distance)
        cube.draw_cube(angle_x, angle_y, angle_z, viewer_distance)
        
        # draw axes
        ax.draw_axes(angle_x, angle_y, angle_z, viewer_distance)

        pygame.display.flip() # Update the screen
        clock.tick(60) # set refresh rate

    pygame.quit()
    sys.exit

if __name__ == '__main__':
    main()

