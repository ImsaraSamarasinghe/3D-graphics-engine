'''
AUTHOR: Imsara Samarasinghe
EMAIL: imsara256@gmail.com
'''
# module imports
import pygame
import sys
import math

# self defined
from shapes import Cylinder, Cube, Torus, Sphere
from config import screen, COLORS # IMPORT params
from background import Axes, Floor # IMPORT Axes class
from text import print_angles, print_zoom

# initialise
pygame.init()

def main():
    clock = pygame.time.Clock() #set pygame clock 
    angle_x, angle_y, angle_z = 0, 0, 0 # Initialise angles
    run = True # variable for sim window
    rotating = False # variable for finding roation status
    last_mouse_pos = None # store last know mouse position
    viewer_distance = 20 # initialise zoom

    # background objects
    ax = Axes() # axes object
    ground = Floor() # floor object

    # shapes class
    cube1 = Cube(center=[0,10,0], face_color=COLORS['P_ORANGE'])
    cube2 = Cube(center=[0,6,0], face_color=COLORS['P_GREEN'])
    cube3 = Cube(center=[0,2,0], face_color=COLORS['P_RED'])
    cube4 = Cube(center=[4,2,0], face_color=COLORS['P_YELLOW'])
    cube5 = Cube(center=[-4,2,0], face_color=COLORS['P_PINK'])
    cube6 = Cube(center=[0,14,0], face_color=COLORS['LAVENDAR'])
    cube7 = Cube(center=[-4,14,0], face_color=COLORS['SALMON'])
    cube8 = Cube(center=[4,14,0], face_color=COLORS['SEAGREEN'])

    ball = Sphere(center=[20,0,0])

    while run:
        screen.fill(COLORS['BACKGROUND_COLOR_2']) # screen background
        print_zoom(viewer_distance)
        print_angles(angle_x, angle_y, angle_z)
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

            # reset all angles to zero - front view
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                angle_x = 0
                angle_y = 0
                angle_z = 0
        
        # Draw ground
        ground.draw_floor(angle_x, angle_y, angle_z, viewer_distance)

        # Draw using the defined vertices
        cube1.draw_cube(angle_x, angle_y, angle_z, viewer_distance)
        cube2.draw_cube(angle_x, angle_y, angle_z, viewer_distance)
        cube3.draw_cube(angle_x, angle_y, angle_z, viewer_distance)
        cube4.draw_cube(angle_x, angle_y, angle_z, viewer_distance)
        cube5.draw_cube(angle_x, angle_y, angle_z, viewer_distance)
        cube6.draw_cube(angle_x, angle_y, angle_z, viewer_distance)
        cube7.draw_cube(angle_x, angle_y, angle_z, viewer_distance)
        cube8.draw_cube(angle_x, angle_y, angle_z, viewer_distance)
        ball.draw_sphere(angle_x, angle_y, angle_z, viewer_distance)

        # draw axes
        ax.draw_axes(angle_x, angle_y, angle_z, viewer_distance)

        pygame.display.flip() # Update the screen
        clock.tick(60) # set refresh rate

    pygame.quit() # close the window
    sys.exit

if __name__ == '__main__':
    main()

