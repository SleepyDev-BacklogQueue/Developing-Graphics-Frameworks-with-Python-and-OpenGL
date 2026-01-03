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
        in vec3 vertexColor;
        out vec3 color;
        void main() {
            gl_Position = vec4(position, 1.0);
            color = vertexColor;
        }
        """

        fragmentShaderCode = """
        in vec3 color;
        out vec4 fragColor;
        void main() {
            fragColor = vec4(color, 1.0);
        }
        """

        self.programRef = OpenGLUtils.initialiseProgram(vertexShaderCode, fragmentShaderCode)

        ## Setup VAO ##
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        ## Setup attributes ##
        positionData = [
            [ 0.8,  0.0,  0.0],
            [ 0.4,  0.6,  0.0],
            [-0.4,  0.6,  0.0],
            [-0.8,  0.0,  0.0],
            [-0.4, -0.6,  0.0],
            [ 0.4, -0.6,  0.0]
        ]
        self.vertexCount = len(positionData)
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")


        colorData = [
            [ 1.0,  0.0,  0.0],
            [ 1.0,  0.5,  0.0],
            [ 1.0,  1.0,  0.0],
            [ 0.0,  1.0,  0.0],
            [ 0.0,  0.0,  1.0],
            [ 1.0,  0.0,  1.0]
        ]
        colorAttribute = Attribute("vec3", colorData)
        colorAttribute.associateVariable(self.programRef, "vertexColor")


        ## Render settings (optional) ##
        glPointSize(10)
        glLineWidth(4)
    
    def update(self):
        glUseProgram(self.programRef)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount)

# Launch application
Test().run()