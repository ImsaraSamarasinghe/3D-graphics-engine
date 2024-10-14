# module imports
import pygame

# Screen dimensions
width, height = 1400, 1000

# create PyGame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D CAD Visualization")

# colors
COLORS = {'WHITE':(255, 255, 255),
          'BLACK':(0, 0, 0),
          'BLUE':(0, 0, 255),
          'RED':(255, 0, 0),
          'GREEN':(0,255,0),
          'GREY':(128, 128, 128),
          'FLOOR_COLOR':(54, 179, 216),
          'BACKGROUND_COLOR': (232, 228, 240)
          }