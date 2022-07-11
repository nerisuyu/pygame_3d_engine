import pygame
import pygame.key
from engine.scene import Scene
from engine.renderer.renderers import render
from globals import SCREEN_HEIGHT, SCREEN_WIDTH, FPS
from engine.colors import *
import time

global event


class Game:
    def __init__(self, name_="My Game"):
        self.__name = name_
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__clock = pygame.time.Clock()
        self.__running = False
        self.__currentScene = None

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(self.__name)

    def run(self):
        self.__running = True
        YawMovement = 0
        YawSpeed = 0.1
        PitchMovement = 0
        PitchSpeed = 0.1
        while self.__running:
            self.__clock.tick(FPS)

            # print("fps is",float(self.__clock.get_fps()))
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        self.stop()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        YawMovement = YawMovement + YawSpeed
                        print(currentCamera[0].yaw)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        YawMovement = YawMovement - YawSpeed
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                print("left")
            if keys[pygame.K_RIGHT]:
                print("right")
            if keys[pygame.K_UP]:
                print("up")
            if keys[pygame.K_DOWN]:
                print("down")

            if keys[ord('c')]:
                print("c")
            if keys[ord('v')]:
                print("v")

            self.__currentScene.update()
            self.__currentScene.draw(self.__screen, SKY_BLUE)
            # todo second and third buffers for ui
            # set to current scene bg

    # TODO create game pause using threading
    # TODO deltaTime and pass it into functions

    def stop(self):
        self.__running = False

    def load_scene(self, newscene: Scene = None):
        self.__currentScene = newscene
