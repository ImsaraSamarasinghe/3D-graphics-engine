# 3D Graphics engine

## Overview
PyGame does not have the ability to process 3D projects. It has the functionality to display 2D objects. This python code contains a set of mathematical transforms that process rotations of 3D axes and project 3D vertices onto a 2D plane (computer screen). The program also has some predefined 3D shapes that can be defined and displayed in the window.

## Features
- Rotates vertices around axes using `rotation_matrix()`
- Projects 3D coordinates to 2D `project_3d_to_2d()`
- Uses `pygame.draw()` functions to draw projected vertices
- Zoom with scrollwheel
- Rotate using left-click
- Press `i` key for isometric view
- Press `r` key for front view

![Video](https://github.com/ImsaraSamarasinghe/3D-graphics-engine/blob/main/2024-10-14%2020-13-26%20-%20Trim%20(2).gif)

## Requirements
- **Python** - 3.x
- **Install PyGame**
'''bash
pip install pygame
'''
