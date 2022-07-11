from errors import *
from numpy.linalg import norm
from numpy import array,dot
from engine.matrices import transform_matrix

class Light:
    def __init__(self, name="BasicLightName", pos=[0, 0, 0, 0], color=(0, 0, 0), level=10):
        self.__name = name
        self.__position = pos / norm(pos)
        self.__color = color
        self.__level = level

    def get_pos(self):
        return self.__position
    def get_color(self):
        return self.__color()[0],self.__color()[1],self.__color()[2]
    def get_level(self):
        return self.__level

    def relative_transform(self, move=None, rotate=None, scale=None) -> None:
        if move:
            if not CheckIfInstance(self.__name, move, list):
                return
            else:
                self.__position = self.__position + array(move)
                self.__position = self.__position / norm(self.__position)

    def rotate(self,rotation):
        self.__position=dot(transform_matrix([0, 0, 0], rotation, [1, 1, 1], [0, 0, 0]),array(self.__position))


    def absolute_transform(self, move=None, rotate=None, scale=None):
        if move:
            if not CheckIfInstance(self.__name, move, list):
                return
            else:
                self.__position = move / norm(move)
