from core.object3D import Object3D
from OpenGL.GL import *

class Mesh(Object3D):
    def __init__(self, geometry, material):
        super().__init__()

        # Set visibility
        self.visible = True

        # Mesh components
        self.geometry = geometry
        self.material = material
        self.vaoRef = glGenVertexArrays(1)

        # Bind attributes
        glBindVertexArray(self.vaoRef)
        for variableName, attributeObject in geometry.attributes.items():
            attributeObject.associateVariable(material.programRef, variableName)
        glBindVertexArray(0)