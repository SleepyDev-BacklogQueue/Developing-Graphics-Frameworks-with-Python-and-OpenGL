import numpy as np
from numpy import subtract, divide, cross
from numpy.linalg import norm
from math import sin, cos, tan, pi

class Matrix(object):
    @staticmethod
    def makeIdentity():
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makeTranslation(x, y, z):
        return np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makeRotationX(theta):
        c = cos(theta)
        s = sin(theta)
        return np.array([
            [ 1,  0,  0, 0],
            [ 0,  c, -s, 0],
            [ 0,  s,  c, 0],
            [ 0,  0,  0, 1]
        ]).astype(float)

    @staticmethod
    def makeRotationY(theta):
        c = cos(theta)
        s = sin(theta)
        return np.array([
            [ c,  0,  s, 0],
            [ 0,  1,  0, 0],
            [-s,  0,  c, 0],
            [ 0,  0,  0, 1]
        ]).astype(float)

    @staticmethod
    def makeRotationZ(theta):
        c = cos(theta)
        s = sin(theta)
        return np.array([
            [ c, -s,  0, 0],
            [ s,  c,  0, 0],
            [ 0,  0,  1, 0],
            [ 0,  0,  0, 1]
        ]).astype(float)

    @staticmethod
    def makeScale(s):
        return np.array([
            [s, 0, 0, 0],
            [0, s, 0, 0],
            [0, 0, s, 0],
            [0, 0, 0, 1]
        ]).astype(float)

    @staticmethod
    def makeOrtographic(left=-1, right=1, bottom=-1, top=-1, near=-1, far=-1):
        return np.array([
            [2/(right-left), 0, 0, -(right+left)/(right-left)],
            [0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)],
            [0, 0, -2/(far-near),  -(far+near)/(far-near)],
            [0, 0, 0, 1]
        ])
    
    @staticmethod
    def makePerspective(angleOfView=60, aspectRatio=1, near=0.1, far=1000):
        a = angleOfView * pi / 180.0
        d = 1.0 / tan(a/2)
        r = aspectRatio
        b = (near + far) / (near - far)
        c = 2 * far * near / (near - far)
        return np.array([
            [d/r, 0,  0, 0],
            [  0, d,  0, 0],
            [  0, 0,  b, c],
            [  0, 0, -1, 1]
        ]).astype(float)

    @staticmethod
    def makeLookAt(position, target):
        worldUp = [0,1,0]
        forward = subtract(target, position)
        right = cross(forward, worldUp)

        if norm(right) < 0.001:
            offset = np.array([0.001,0,0])
            right = cross(foward, worldUp + offset)
        
        up = cross(right, forward)

        # Normalise vectors
        forward = divide(forward, norm(forward))
        right = divide(right, norm(right))
        up = divide(up, norm(up))

        return np.array([
            [right[0], up[0], -forward[0], position[0]],
            [right[1], up[1], -forward[1], position[1]],
            [right[2], up[2], -forward[2], position[2]],
            [       0,     0,           0,           1]
        ])