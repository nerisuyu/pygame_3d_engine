from engine.colors import *
from game import Game
from engine.scene import Scene
from engine.object import Object

import globals
from engine.renderer.shapes import Rect, Polygon, Circle
from engine.visualizeable.visualizeable_loader import load_visualizeable
from math import pi
from engine.visualizeable.light import Light


def main_menu():
    ...


def game_loop():
    ...


def main():
    sun = Light("sun", [0, -1, 0, 0], CHAOS, 1)
    ObjFrog = Object("MyObject", -20, -20, 0, 0, 0, pi / 4, 1)
    ObjFrog2 = Object("MyObject", 10, 0, 0, 0, 0, 0, 0.2)
    ObjFrog3 = Object("MyObject", 10, 0, 0, 0, 0, 0, 0.7)
    ObjFrog4 = Object("MyObject", 0, 0, 0, 0, 0, pi / 4, 0.1)
    ObjFrog5 = Object("MyObject", 10, 0, 0, 0, 0, 0, 0.7)
    ObjFrog6 = Object("MyObject", 10, 0, 0, 0, 0, 0, 0.7)
    ObjFrog7 = Object("MyObject", 10, 0, 0, 0, 0, 0, 0.7)
    ObjFrog8 = Object("MyObject", 10, 0, 0, 0, 0, 0, 0.7)

    v = load_visualizeable("./engine/visualizeable/stl/frog.stl")
    ObjFrog.load_visualizeable("./engine/visualizeable/stl/frog.stl")
    ObjFrog3.assign_visualizeable(v)
    ObjFrog4.assign_visualizeable(v)
    ObjFrog5.assign_visualizeable(v)
    #ObjFrog6.assign_visualizeable(v)
    #ObjFrog7.assign_visualizeable(v)
    #ObjFrog8.assign_visualizeable(v)
    # TODO deltaTime

    MyScene = Scene()
    MyScene.init_camera(-20, 20, 5, -pi / 2, 0)
    MyScene.add_object(ObjFrog)
    MyScene.add_object(ObjFrog2)
    MyScene.add_object(ObjFrog3)
    #MyScene.add_object(ObjFrog4)
    #MyScene.add_object(ObjFrog5)
    #MyScene.add_object(ObjFrog6)
    #MyScene.add_object(ObjFrog7)
    #MyScene.add_object(ObjFrog8)
    MyScene.set_global_light(sun)

    MyGame = Game()
    MyGame.load_scene(MyScene)
    MyGame.run()

    '''        start = time.time()
        end = time.time()
        print("time= ", end - start)'''


if __name__ == '__main__':
    main()

# todo function creator for jumps and stuff
# todo maybe do curve motion
