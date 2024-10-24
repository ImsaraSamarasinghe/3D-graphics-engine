'''
AUTHOR: Imsara Samarasinghe
E-MAIL: imsara256@gmail.com
'''

from SimulationEngine import Engine
from shapes import Sphere, Cube, Torus
from config import COLORS

sim = Engine() # Initialise the engine

sim._add_balls(Sphere(center=[0,30,0])) # add a ball to the engine @ x, y, z = 0, 30, 0
sim._add_balls(Sphere(center=[10,20,0], radius=2 , face_color=COLORS['RED'])) # add a ball to the engine @ x, y, z = 10, 20, 0
sim._add_shapes(Cube(center=[10,4,10])) # add a cube 
sim._add_shapes(Torus(center=[20,30,4])) # add a torus

sim.runEngine() # run the engine