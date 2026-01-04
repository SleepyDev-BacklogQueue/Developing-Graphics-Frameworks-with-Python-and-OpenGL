import numpy as np
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