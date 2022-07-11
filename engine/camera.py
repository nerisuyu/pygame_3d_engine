import math

from numpy import array

from globals import *


class Camera:
    def __init__(self, x_, y_, z_, pitch_,yaw_):
        self.__position = array([x_, y_, z_])
        self.__yaw = yaw_
        self.__pitch = pitch_
        self.__fovx = math.pi / 2
        self.__fovy = self.__fovx * SCREEN_HEIGHT/SCREEN_WIDTH

    def get_params(self):
        return self.__position,self.__yaw,self.__pitch,self.__fovx,self.__fovy
