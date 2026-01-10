from core.matrix import Matrix
import numpy as np

class Object3D(object):
    def __init__(self):
        self.transform = Matrix.makeIdentity()
        self.parent = None
        self.children = []
    
    # Populate Object3D tree
    def add(self, child):
        self.children += [child]
        child.parent = self

    def remove(self, child):
        self.children.remove(child)
        child.parent = None

    # Get absolute world space
    def getWorldMatrix(self):
        if self.parent == None:
            return self.transform
        
        return self.parent.getWorldMatrix() @ self.transform

    # Get all children
    def getDescendantList(self):
        descendant_l = []
        node_l = [self]
        while len(node_l) > 0:
            node = node_l.pop(0)
            descendant_l += [node]
            node_l = node.children + node_l

        return descendant_l

    # Quick apply matrix
    def applyMatrix(self, matrix, localCoord=True):
        if localCoord:
            self.transform = self.transform @ matrix
        else:
            self.transform = matrix @ self.transform
    
    def translate(self, x, y, z, localCoord=True):
        matrix = Matrix.makeTranslation(x, y, z)
        self.applyMatrix(matrix, localCoord)
            
    def rotateX(self, theta, localCoord=True):
        matrix = Matrix.makeRotationX(theta)
        self.applyMatrix(matrix, localCoord)
            
    def rotateY(self, theta, localCoord=True):
        matrix = Matrix.makeRotationY(theta)
        self.applyMatrix(matrix, localCoord)
            
    def rotateZ(self, theta, localCoord=True):
        matrix = Matrix.makeRotationZ(theta)
        self.applyMatrix(matrix, localCoord)
            
    def scale(self, s, localCoord=True):
        matrix = Matrix.makeScale(s)
        self.applyMatrix(matrix, localCoord)

    def lookAt(self, targetPoaition):
        self.transform = Matrix.makeLookAt(self.getWorldPosition(), targetPoaition)

    # Quick get/set position
    def getPosition(self):
        return [
            self.transform[0, 3],
            self.transform[1, 3],
            self.transform[2, 3]
        ]
    
    def setPosition(self, position):
        self.transform[0, 3] = position[0]
        self.transform[1, 3] = position[1]
        self.transform[2, 3] = position[2]

    def getWorldPosition(self):
        worldMatrix = self.getWorldMatrix()
        return [
            worldMatrix[0, 3],
            worldMatrix[1, 3],
            worldMatrix[2, 3]
        ]
    
    def getRotationMatrix(self):
        return np.array([
            self.transform[0][0:3],
            self.transform[1][0:3],
            self.transform[2][0:3]
        ])

    def getDirection(self):
        forward = np.array([0,0,-1])
        return list(self.getRotationMatrix() @ forward)

    def setDirection(self, direction):
        position = self.getPosition()
        targetPosition = [
            position[0] + direction[0],
            position[1] + direction[1],
            position[2] + direction[2]
        ]
        self.lookAt(targetPosition)