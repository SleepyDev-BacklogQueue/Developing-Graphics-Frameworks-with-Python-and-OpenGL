#!/usr/bin/env python3

from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        ## Build program ##
        vertexShaderCode = """
        in vec3 position;
        void main() {
            gl_Position = vec4(position, 1.0);
        }
        """

        fragmentShaderCode = """
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """

        self.programRef = OpenGLUtils.initialiseProgram(vertexShaderCode, fragmentShaderCode)

        ## Setup triangle ##
        self.vaoTri = glGenVertexArrays(1)
        glBindVertexArray(self.vaoTri)

        positionDataTri = [
            [-0.5,  0.8,  0.0],
            [-0.2,  0.2,  0.0],
            [-0.8,  0.2,  0.0]
        ]
        self.vertexCountTri = len(positionDataTri)
        positionAttributeTri = Attribute("vec3", positionDataTri)
        positionAttributeTri.associateVariable(self.programRef, "position")

        ## Setup square ##
        self.vaoSquare = glGenVertexArrays(1)
        glBindVertexArray(self.vaoSquare)

        positionDataSquare = [
            [ 0.8,  0.8,  0.0],
            [ 0.8,  0.2,  0.0],
            [ 0.2,  0.2,  0.0],
            [ 0.2,  0.8,  0.0]
        ]
        self.vertexCountSquare = len(positionDataSquare)
        positionAttributeSquare = Attribute("vec3", positionDataSquare)
        positionAttributeSquare.associateVariable(self.programRef, "position")


        ## Render settings (optional) ##
        glLineWidth(4)
    
    def update(self):
        # Draw triangle
        glUseProgram(self.programRef)
        glBindVertexArray(self.vaoTri)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCountTri)

        # Draw square
        glUseProgram(self.programRef)
        glBindVertexArray(self.vaoSquare)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCountSquare)


# Launch application
Test().run()