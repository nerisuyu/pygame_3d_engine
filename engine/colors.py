import pygame
from math import cos,sin,pi
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FROG_GREEN=(94,221,95)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173,216,230)
SKY_BLUE = (135,206,235)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

def CHAOS():
    t=pygame.time.get_ticks()/300
    return ((0.5+0.5*cos(t))*250,(0.5+0.5*cos(t+2*pi/3))*250,(0.5+0.5*cos(t+4*pi/3))*250)