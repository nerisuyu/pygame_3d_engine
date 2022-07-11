import math
import pygame
import numpy as np
import pygame.key
import meshio
from operator import itemgetter
import time

global event
WIDTH = 1000
HEIGHT = 750
FPS = 30


def cos(a): return math.cos(a)


def sin(a): return math.sin(a)


def trig(angle): return cos(angle), sin(angle)


def TransformMatrix(dX, dY, dZ, a, b, c, scale):
    xC, xS = trig(a)
    yC, yS = trig(b)
    zC, zS = trig(c)
    Scale_matrix = np.array([[scale, 0, 0, 0],
                             [0, scale, 0, 0],
                             [0, 0, scale, 0],
                             [0, 0, 0, 1]])
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

    # return np.dot(Rotate_Z_matrix,np.dot(Rotate_Y_matrix,np.dot(Rotate_X_matrix,Translate_matrix)))
    return np.dot(Scale_matrix, np.dot(Translate_matrix, np.dot(Rotate_Z_matrix, np.dot(Rotate_Y_matrix, Rotate_X_matrix))))

def isInView(tri):
    if tri[4] < -1 or tri[4] > 1: return False;
    for i in range(0, 2):
        for k in range(0, 1):
            if -1.5 > tri[i][0] or tri[i][0] > 1.5:
                return False
    return True;


class Camera:
    def __init__(self, x_, y_, z_, yaw_, pitch_):
        self.position = np.array([x_, y_, z_])
        self.yaw = yaw_
        self.pitch = pitch_


class Object:
    def __init__(self, x_, y_, z_, rx_, ry_, rz_, vertices_, triangles_, scale):
        self.position = np.array([x_, y_, z_])
        self.rotation = [rx_, ry_, rz_]
        self.__vertices = vertices_
        self.triangles = triangles_
        self.scale = scale
        self.__worldSpaceVertices = [None] * len(self.__vertices)
        self.__cameraSpaceVertices = [None] * len(self.__vertices)
        self.screenSpaceVertices = [None] * len(self.__vertices)

    def loadMesh(self, filename):
        self.__vertices = []
        self.triangles = []
        mesh = meshio.read(filename, file_format="stl")
        for v in mesh.points:
            vert = [v[0], v[1], v[2], 1]
            self.__vertices.append(vert)
        self.triangles = mesh.cells_dict['triangle']
        self.__worldSpaceVertices = [None] * len(self.__vertices)
        self.__cameraSpaceVertices = [None] * len(self.__vertices)
        self.screenSpaceVertices = [None] * len(self.__vertices)

    def __setNormals(self, Vertices):
        length = len(self.triangles)
        triangles_ = []
        for i in range(0, length):
            A = Vertices[self.triangles[i][1]] - Vertices[self.triangles[i][0]]
            B = Vertices[self.triangles[i][2]] - Vertices[self.triangles[i][0]]
            normal = [A[1] * B[2] - A[2] * B[1], A[2] * B[0] - A[0] * B[2], A[0] * B[1] - A[1] * B[0], 1]
            normal = normal / np.linalg.norm(normal)
            triangles_.append([self.triangles[i][0], self.triangles[i][1], self.triangles[i][2], normal])
        self.triangles = triangles_

    def __worldSpaceTransformation(self):
        Matrix = TransformMatrix(self.position[0], self.position[1], self.position[2], self.rotation[0],
                                 self.rotation[1], self.rotation[2], self.scale)
        length = len(self.__vertices)
        for i in range(0, length):
            self.__worldSpaceVertices[i] = np.dot(Matrix, self.__vertices[i])

    def __cameraSpaceTransformation(self):
        Matrix = np.linalg.inv(
            TransformMatrix(mainCamera.position[0], mainCamera.position[1], mainCamera.position[2], 0, 0, 0, 1))
        Matrix2 = (TransformMatrix(0, 0, 0, 0, 0, mainCamera.yaw, 1))
        Matrix3 = (TransformMatrix(0, 0, 0, mainCamera.pitch, 0, 0, 1))
        length = len(self.__vertices)
        for i in range(0, length):
            self.__cameraSpaceVertices[i] = np.dot(Matrix3,
                                                   np.dot(Matrix2, (np.dot(Matrix, self.__worldSpaceVertices[i]))))

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
        length = len(self.__vertices)
        for i in range(0, length):
            Vn = np.dot(Matrix, self.__cameraSpaceVertices[i])
            Vn[0] = Vn[0] / Vn[3]
            Vn[1] = Vn[1] / Vn[3]
            Vn[2] = Vn[2] / Vn[3]
            Vn[3] = Vn[3] / Vn[3]
            self.screenSpaceVertices[i] = Vn

    def update(self):
        self.__worldSpaceTransformation()
        self.__cameraSpaceTransformation()
        self.__perspectiveProjection()
        self.__setNormals(self.__worldSpaceVertices)




mainCamera = Camera(10, 40, 1, 0, math.pi / 2)
verts = [[5, 5, -5, 1], [-5, 5, 5, 1], [5, -5, 5, 1], [-5, -5, -5, 1]]
tris = [[0, 1, 3, 0], [0, 3, 2, 0], [0, 1, 2, 0], [1, 3, 2, 0]]
tetraedr = Object(0., 10., -3., 0., 0., math.pi, verts, tris, 1)
tetraedr2 = Object(0., 10., -3., 0., 0., math.pi, verts, tris, 2)
tetraedr.loadMesh('.\\stl\\frog.stl')
tetraedr2.loadMesh('.\\stl\\socrat.stl')
Objects = [tetraedr]
tetraedr.update()


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rasterizer")
    clock = pygame.time.Clock()
    running = True
    YawMovement = 0
    YawSpeed = 0.1
    PitchMovement = 0
    PitchSpeed = 0.1
    t=0
    while running:
        t=t+1
        clock.tick(FPS)
        screen.fill((255, 255, 255))

        tetraedr.rotation[2] = tetraedr.rotation[2]+0.1

        #tetraedr.rotation[1] = tetraedr.rotation[1] + 0.01
        #tetraedr.position[1] = tetraedr.position[1] + 0.2
        mainCamera.yaw = mainCamera.yaw + YawMovement
        mainCamera.pitch= mainCamera.pitch+PitchMovement
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    YawMovement = YawMovement + YawSpeed
                    print(mainCamera.yaw)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    YawMovement = YawMovement - YawSpeed
                    print(mainCamera.yaw)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    PitchMovement=PitchMovement +PitchSpeed
                    print('up')
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    print('down')
                    PitchMovement=PitchMovement -PitchSpeed
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    YawMovement = YawMovement - YawSpeed
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    YawMovement = YawMovement + YawSpeed
                if event.key == pygame.K_UP or event.key == ord('w'):
                    PitchMovement=PitchMovement -PitchSpeed

                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    PitchMovement=PitchMovement +PitchSpeed

        SceneTriangles = []
        for Obj in Objects:
            timing=time.time()
            Obj.update()
            print(f"update: {time.time()-timing}")
            for tri in Obj.triangles:
                depth = (Obj.screenSpaceVertices[tri[0]][2] + Obj.screenSpaceVertices[tri[1]][2] +
                         Obj.screenSpaceVertices[tri[2]][2]) / 3
                SceneTriangles.append([[Obj.screenSpaceVertices[tri[0]][0], Obj.screenSpaceVertices[tri[0]][1]],
                                       [Obj.screenSpaceVertices[tri[1]][0], Obj.screenSpaceVertices[tri[1]][1]],
                                       [Obj.screenSpaceVertices[tri[2]][0], Obj.screenSpaceVertices[tri[2]][1]],
                                       tri[3],
                                       depth])

        timing = time.time()
        SceneTriangles = sorted(SceneTriangles, key=itemgetter(4), reverse=True)
        print(f"sorting: {time.time() - timing}")

        light = [0, 0, 0.5, 0.5]
        for tri in SceneTriangles:
            l = np.dot(light, tri[3])+1
            if isInView(tri):
                #(102,102,102)
                #(l/3, l+50 , l/3)
                pygame.draw.polygon(screen, (255, 255 , 255), [
                    (tri[0][0] * WIDTH / 2 + WIDTH / 2,
                     tri[0][1] * HEIGHT / 2 + HEIGHT / 2),
                    (tri[1][0] * WIDTH / 2 + WIDTH / 2,
                     tri[1][1] * HEIGHT / 2 + HEIGHT / 2),
                    (tri[2][0] * WIDTH / 2 + WIDTH / 2,
                     tri[2][1] * HEIGHT / 2 + HEIGHT / 2)],
                                    2)
                pygame.draw.polygon(screen, (l*40, l*0 , l*30), [
                    (tri[0][0] * WIDTH / 2 + WIDTH / 2,
                     tri[0][1] * HEIGHT / 2 + HEIGHT / 2),
                    (tri[1][0] * WIDTH / 2 + WIDTH / 2,
                     tri[1][1] * HEIGHT / 2 + HEIGHT / 2),
                    (tri[2][0] * WIDTH / 2 + WIDTH / 2,
                     tri[2][1] * HEIGHT / 2 + HEIGHT / 2)],
                                    0)
        pygame.display.flip()
        # gives a single float value
        #print(f'cpu:{psutil.cpu_percent()},ram:{psutil.virtual_memory().percent}')

    pygame.quit()




if __name__ == '__main__':
    main()
