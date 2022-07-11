from numpy import array
from engine.visualizeable.visualizeable import Visualizeable
from engine.visualizeable.visualizeable_loader import load_visualizeable
from errors import *



class Object:
    def __init__(self, name_="BlankObjectName", x_=0, y_=0, z_=0, rx_=0, ry_=0, rz_=0, scale=1):
        self.__name = name_
        self.__location = array([x_, y_, z_])
        self.__rotation = array([rx_, ry_, rz_])
        self.__scale = array([scale, scale, scale])
        self.__Visualizeables = []
        self.Mover = None

    def get_lrs(self):
        return self.__location, self.__rotation, self.__scale

    def relative_transform(self, move=None, rotate=None, scale=None) -> None:
        if move:
            if not CheckIfInstance(self.__name, move, list):
                return
            else:
                self.__location = self.__location + array(move)
        if rotate:
            if not CheckIfInstance(self.__name, rotate, list):
                return
            else:
                self.__rotation = self.__rotation + array(rotate)
        if scale:
            if not isinstance(scale, list) and not isinstance(scale, float) and not isinstance(scale, int):
                WrongTypeErrorMessage(self.__name, scale, type(scale), "list or float")
                return
            else:
                self.__scale = self.__scale * scale

    def absolute_transform(self, move=None, rotate=None, scale=None):
        if move:
            if not CheckIfInstance(self.__name, move, list):
                return
            else:
                self.__location = array(move)
        if rotate:
            if not CheckIfInstance(self.__name, rotate, list):
                return
            else:
                self.__rotation = array(rotate)
        if scale:
            if not isinstance(scale, list) and not isinstance(scale, float) and not isinstance(scale, int):
                WrongTypeErrorMessage(self.__name, scale, type(scale), "list or float")
                return
            else:
                self.__scale = array(scale)

    def load_visualizeable(self,filename):
        v=load_visualizeable(filename)
        self.__Visualizeables.append(v)
        v.set_parent(self)

    def assign_visualizeable(self, v: Visualizeable):
        self.__Visualizeables.append(v)
        v.set_parent(self)

    def update(self):
        ...

    def draw(self, camera, renderBuffer, globalLight=None, localLights=None):
        if self.__Visualizeables:
            for v in self.__Visualizeables:
                v.draw(camera, renderBuffer, globalLight, localLights)
