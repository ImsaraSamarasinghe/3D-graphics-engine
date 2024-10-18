'''
AUTHOR: Imsara Samarasinghe
EMAIL: imsara256@gmail.com
'''
import pygame
import math
from config import COLORS, screen

# zoom level text
def print_zoom(viewer_distance):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(f'Zoom: {100-viewer_distance}', True, COLORS['BLACK'], COLORS['BACKGROUND_COLOR'])
    textRect = text.get_rect()
    textRect.center = (50,10)
    screen.blit(text, textRect)

# angles text
def print_angles(angle_x, angle_y, angle_z):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(f'angle_x : {math.degrees(angle_x):.2f}° | angle_y : {math.degrees(angle_y):.2f}° | angle_z : {math.degrees(angle_z):.2f}°', True, COLORS['BLACK'], COLORS['BACKGROUND_COLOR'])
    textRect = text.get_rect()
    textRect.center = (200,50)
    screen.blit(text, textRect)