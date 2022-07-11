import pygame
from numpy import array
from engine.object import Object
from engine.camera import Camera
from math import pi
from engine.visualizeable.light import Light
from engine.renderer.renderers import render
import time

class Scene:
    def __init__(self, filename=None):
        self.loadfromfile()
        self.__objects = []
        self.__globalLight = None
        self.__localLights = []
        self.__camera = None
        self.__renderBuffer = []
        self.__background = None

    def set_global_light(self,light: Light):
        self.__globalLight = light

    def loadfromfile(self, filename=None):
        pass

    def init_camera(self, *args, **kwargs):
        self.__camera = Camera(*args, **kwargs)
        return self.__camera

    def add_object(self, obj: Object):
        self.__objects.append(obj)

    def remove_object(self, obj: Object):
        self.__objects.remove(obj)

    def update(self):
        keys = pygame.key.get_pressed()
        #for obj in self.__objects:
        #    obj.relative_transform([0,0,0],[0,0,0],[0,0,0])
        if keys[pygame.K_LEFT]:
            self.__globalLight.rotate([0.1,0,0])
        if keys[pygame.K_RIGHT]:
            self.__globalLight.rotate([-0.1,0,0])

    def draw(self, screen, bg):


        for Obj in self.__objects:

            Obj.draw(self.__camera, self.__renderBuffer, self.__globalLight, self.__localLights)


        render(screen, self.__renderBuffer, bg)

