# module imports
import pygame

# Screen dimensions
width, height = 1200, 800

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
          'BACKGROUND_COLOR': (232, 228, 240),
          'P_RED': (255,179,186),
          'P_ORANGE': (255,223,186),
          'P_YELLOW': (255,255,186),
          'P_GREEN': (186,255,201),
          'P_BLUE': (186,225,255)
          }
