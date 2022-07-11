import weakref
from math import cos, sin, tan
import meshio
import pyopencl
from numpy import array, dot
from numpy.linalg import norm
from engine.colors import *
from engine.matrices import transform_matrix
from engine.renderer.shapes import Polygon
from engine.visualizeable.visualizeable import Visualizeable
from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from engine.openCL.matrix_dot_vectors import matrix_dot_vector
import time


class Mesh(Visualizeable):
    def __init__(self, parent=None):
        self.__parent = weakref.ref(parent) if parent else parent
        self.__vertices = None
        self.__triangles = None
        self.__buffer = None
        self.__WorldSpaceVertices = None
        self.__screenSpaceVertices = None
        self.__buffer = None
        self.__mdv = matrix_dot_vector()

    def load_stl(self, filename):
        # todo try:
        #
        #
        # except:
        self.__vertices = []
        self.__triangles = []
        mesh = meshio.read(filename, file_format="stl")
        for v in mesh.points:
            self.__vertices.append(v[0])
            self.__vertices.append(v[1])
            self.__vertices.append(v[2])
            self.__vertices.append(1)
        self.__triangles = mesh.cells_dict['triangle']
        self.__screenSpaceVertices = [None] * len(self.__vertices)
        self.__WorldSpaceVertices = [None] * len(self.__vertices)
        self.__buffer = [None] * len(self.__vertices)
        return self

    def transform_triangles(self, camera):


        location, rotation, scale = self.parent.get_lrs()
        cam_position, yaw, pitch, fovx, fovy = camera.get_params()
        cyaw = cos(yaw)
        syaw = sin(yaw)
        cpitch = cos(pitch)
        spitch = sin(pitch)
        n = 10
        f = 50
        t = 8
        b = -t
        r = t * SCREEN_WIDTH / SCREEN_HEIGHT
        l = -r
        TMatrix = transform_matrix(location, rotation, scale, cam_position)

        WSMatrix = transform_matrix(location, rotation, scale, [0, 0, 0])

        CamMatrix = array([[cyaw, -syaw, 0, 0],
                           [cpitch * syaw, cpitch * cyaw, -spitch, 0],
                           [spitch * syaw, spitch * cyaw, cpitch, 0],
                           [0, 0, 0, 1]])
        PPMatrix = array([[2 * n / (r - l), 0, (r + l) / (r - l), 0],
                          [0, 2 * n / (t - b), (t + b) / (t - b), 0],
                          [0, 0, (f + n) / (n - f), 2 * f * n / (n - f)],
                          [0, 0, -1, 0]])
        FOVPMatrix = array([[1 / tan(fovx / 2), 0, 0, 0],
                            [0, 1 / tan(fovy / 2), 0, 0],
                            [0, 0, (f + n) / (n - f), 2 * f * n / (n - f)],
                            [0, 0, -1, 0]])

        length = len(self.__vertices)

        self.__screenSpaceVertices = self.__mdv.calculate(dot(FOVPMatrix, dot(CamMatrix, TMatrix)), self.__vertices)

        '''
        for i in range(0, length):
            Vn = dot(FOVPMatrix, dot(CamMatrix, dot(TMatrix, self.__vertices[i])))
            Vn = Vn / Vn[3]
            self.__screenSpaceVertices[i] = Vn
            # self.__WorldSpaceVertices[i] = dot(WSMatrix, self.__vertices[i])
        '''

    def draw(self, camera, renderBuffer, globalLight=None, localLights=None):

        self.transform_triangles(camera)


        '''
        if globalLight:
        light = globalLight.get_pos()
        r, g, b = globalLight.get_color()
        level = globalLight.get_level()
        r, g, b = 0, 0, 0
        level = 1
        light = [0, 0, 0, 0]
        for tri in self.__triangles:
            ##
            A = self.__WorldSpaceVertices[tri[1]] - self.__WorldSpaceVertices[tri[0]]
            B = self.__WorldSpaceVertices[tri[2]] - self.__WorldSpaceVertices[tri[0]]
            normal = [A[1] * B[2] - A[2] * B[1], A[2] * B[0] - A[0] * B[2], A[0] * B[1] - A[1] * B[0], 1]
            normal = normal / norm(normal)  ##
            l = (dot(light, normal) + 1) / 2  ##
            color = (min(l * r * level, 255), min(l * g * level, 255), min(l * b * level, 255))
                        ## performance drop here
            
            color=(0,0,0)
            
            depth = (self.__screenSpaceVertices[tri[0]][2] + self.__screenSpaceVertices[tri[1]][2] +
                     self.__screenSpaceVertices[tri[2]][2]) / 3
            
            color = (0, 0, 0)
            depth=0

            Triangle = Polygon(depth, 0, color,  # no
                               (self.__screenSpaceVertices[4*tri[0]] * SCREEN_WIDTH / 2 + SCREEN_WIDTH / 2,
                                self.__screenSpaceVertices[4*tri[0]+1] * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 2),
                               (self.__screenSpaceVertices[4*tri[1]] * SCREEN_WIDTH / 2 + SCREEN_WIDTH / 2,
                                self.__screenSpaceVertices[4*tri[1]+1] * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 2),
                               (self.__screenSpaceVertices[4*tri[2]] * SCREEN_WIDTH / 2 + SCREEN_WIDTH / 2,
                                self.__screenSpaceVertices[4*tri[2]+1] * SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 2))
            renderBuffer.append(Triangle)
            '''
        # setNormals
        # WS transform
        # CS transform
        # persp project
        # check if is in veiw with IsInView()
        # if yes then add into RenderBuffer
    # todo create sublcasses for textured mesh and non textured mesh with abstract function getcolor() or smth
