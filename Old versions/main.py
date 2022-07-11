import math
import pygame
import numpy as np
import pygame.key

global event
WIDTH = 1000
HEIGHT = 750
FPS = 30


def Vertex(a):
    return np.array([a[0], a[1], a[2], 1], dtype=object)


def cos(a): return math.cos(a)


def sin(a): return math.sin(a)


def trig(angle): return cos(angle), sin(angle)


def TransformMatrix(dX, dY, dZ, a, b, c):
    xC, xS = trig(a)
    yC, yS = trig(b)
    zC, zS = trig(c)
    Translate_matrix = np.array([[1, 0, 0, dX],
                                 [0, 1, 0, dY],
                                 [0, 0, 1, dZ],
                                 [0, 0, 0, 1]])
    Rotate_Z_matrix = np.array([[zC, -zS, 0, 0],
                                [zS, zC, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
    Rotate_Y_matrix = np.array([[yC, 0, yS, 0],
                                [0, 1, 0, 0],
                                [-yS, 0, yC, 0],
                                [0, 0, 0, 1]])
    Rotate_X_matrix = np.array([[1, 0, 0, 0],
                                [0, xC, -xS, 0],
                                [0, xS, xC, 0],
                                [0, 0, 0, 1]])

    return np.dot(Rotate_X_matrix, np.dot(Rotate_Y_matrix, np.dot(Rotate_Z_matrix, Translate_matrix)))


class Triangle:
    def __init__(self, vert1, vert2, vert3, color):
        self.vertices = [vert1, vert2, vert3]
        A = self.vertices[1] - self.vertices[0]
        B = self.vertices[2] - self.vertices[0]
        self.color = color
        self.normal = np.array([[A[1] * B[2] - A[2] * B[1]],
                                [A[2] * B[0] - A[0] * B[2]],
                                [A[0] * B[1] - A[1] * B[0]]])


class Camera:
    def __init__(self, x_, y_, z_, yaw_, pitch_):
        self.position = np.array([x_, y_, z_])
        self.yaw = yaw_
        self.pitch = pitch_


class Object:
    def __init__(self, x_, y_, z_, rx_, ry_, rz_, triangles_):
        self.position = np.array([x_, y_, z_])
        self.rotation = [rx_, ry_, rz_]

        self.__triangles = triangles_
        self.__worldSpaceTriangles = [None] * len(self.__triangles)
        self.__cameraSpaceTriangles = [None] * len(self.__triangles)
        self.screenSpaceTriangles = [None] * len(self.__triangles)

    def __worldSpaceTransformation(self):
        Matrix = TransformMatrix(self.position[0], self.position[1], self.position[2], self.rotation[0],
                                 self.rotation[1], self.rotation[2])
        length = len(self.__triangles)
        for i in range(0, length):
            V = []
            for v in self.__triangles[i].vertices:
                V.append(np.dot(Matrix, v))
            self.__worldSpaceTriangles[i] = Triangle(V[0], V[1], V[2], self.__triangles[i].color)

    def __cameraSpaceTransformation(self):
        Matrix = np.linalg.inv(
            TransformMatrix(mainCamera.position[0], mainCamera.position[1], mainCamera.position[2], 0, 0, 0))
        Matrix2 = (TransformMatrix(0, 0, 0, 0, 0, mainCamera.yaw))
        Matrix3 = (TransformMatrix(0, 0, 0, mainCamera.pitch, 0, 0))
        length = len(self.__triangles)
        for i in range(0, length):
            V = []
            for v in self.__worldSpaceTriangles[i].vertices:
                V.append(np.dot(Matrix3, np.dot(Matrix2, (np.dot(Matrix, v)))))
            self.__cameraSpaceTriangles[i] = Triangle(V[0], V[1], V[2], self.__triangles[i].color)

    def __perspectiveProjection(self):
        n = 10
        f = 50
        t = 8
        b = -t
        r = t * WIDTH / HEIGHT
        l = -r
        Matrix = np.array([[2 * n / (r - l), 0, (r + l) / (r - l), 0],
                           [0, 2 * n / (t - b), (t + b) / (t - b), 0],
                           [0, 0, (f + n) / (n - f), 2 * f * n / (n - f)],
                           [0, 0, -1, 0]])
        length = len(self.__triangles)
        for i in range(0, length):
            V = []
            for v in self.__cameraSpaceTriangles[i].vertices:
                Vn = np.dot(Matrix, v)
                Vn[0] = Vn[0] / Vn[3]
                Vn[1] = Vn[1] / Vn[3]
                Vn[2] = Vn[2] / Vn[3]
                Vn[3] = Vn[3] / Vn[3]
                V.append(Vn)
            self.screenSpaceTriangles[i] = Triangle(V[0], V[1], V[2], self.__triangles[i].color)

    def update(self):
        self.__worldSpaceTransformation()
        self.__cameraSpaceTransformation()
        self.__perspectiveProjection()


mainCamera = Camera(10, 40, 1, 0, math.pi / 2)

tris = [Triangle(Vertex([5, 0, 0]), Vertex([0, 5, 0]), Vertex([0, 0, 5]), (200, 200, 200)),
        Triangle(Vertex([-5, 0, 0]), Vertex([0, 5, 0]), Vertex([0, 0, 5]), (200, 200, 200)),
        Triangle(Vertex([5, 0, 0]), Vertex([0, -5, 0]), Vertex([0, 0, 5]), (200, 200, 200)),
        Triangle(Vertex([5, 0, 0]), Vertex([0, 5, 0]), Vertex([0, 0, -5]), (200, 200, 200)),
        Triangle(Vertex([5, 0, 0]), Vertex([0, -5, 0]), Vertex([0, 0, -5]), (200, 200, 200)),
        Triangle(Vertex([-5, 0, 0]), Vertex([0, -5, 0]), Vertex([0, 0, -5]), (200, 200, 200)),
        Triangle(Vertex([-5, 0, 0]), Vertex([0, -5, 0]), Vertex([0, 0, 5]), (200, 200, 200)),
        Triangle(Vertex([-5, 0, 0]), Vertex([0, 5, 0]), Vertex([0, 0, -5]), (255, 200, 200))]
Obj = Object(0, 0, 0, 0, 0, math.pi / 4, tris)
Obj2 = Object(40, 0, 0, 0, 0, math.pi / 4, tris)
Objects = [Obj, Obj2]


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        Obj.rotation[2] = Obj.rotation[2] + 0.1
        Obj.rotation[1] = Obj.rotation[1] + 0.01

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    mainCamera.yaw = mainCamera.yaw + 0.1
                    print('left')
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    mainCamera.yaw = mainCamera.yaw - 0.1
                    print('right')
                if event.key == pygame.K_UP or event.key == ord('w'):
                    mainCamera.pitch = mainCamera.pitch + 0.1
                    print('up')
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    print('down')
                    mainCamera.pitch = mainCamera.pitch - 0.1
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    print('left stop')
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    print('right stop')

        for obj in Objects:
            obj.update()
            for tri in obj.screenSpaceTriangles:
                if tri.vertices[0][3] > 0:
                    pygame.draw.polygon(screen, tri.color, [
                        (tri.vertices[0][0] * WIDTH / 2 + WIDTH / 2, tri.vertices[0][1] * HEIGHT / 2 + HEIGHT / 2),
                        (tri.vertices[1][0] * WIDTH / 2 + WIDTH / 2, tri.vertices[1][1] * HEIGHT / 2 + HEIGHT / 2),
                        (tri.vertices[2][0] * WIDTH / 2 + WIDTH / 2, tri.vertices[2][1] * HEIGHT / 2 + HEIGHT / 2)],
                                        True)

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
