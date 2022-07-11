from math import sin, cos

from numpy import array


def trig(angle): return cos(angle), sin(angle)


def transform_matrix(pos, rot, scale, campos):
    dX, dY, dZ = pos[0], pos[1], pos[2]
    a, b, c = rot[0], rot[1], rot[2]
    scx, scy, scz = scale[0], scale[1], scale[2]
    camx, camy, camz = campos[0], campos[1], campos[2]
    cx, sx = trig(a)
    cy, sy = trig(b)
    cz, sz = trig(c)
    # Transform.ZXYRotation.Scale
    return array([[scx * (cy * cz - sx * sy * sz), scy * (-cx * sz), scz * (sx * cy * sz + sy * cz), dX - camx],
                  [scx * (sx * sy * cz + cy * sz), scy * (cx * cz), scz * (sy * sz - sx * cy * cz), dY - camy],
                  [scx * (-cx * sy), scy * sx, scz * (cx * cy), dZ - camz],
                  [0, 0, 0, 1]])



'''
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
'''
