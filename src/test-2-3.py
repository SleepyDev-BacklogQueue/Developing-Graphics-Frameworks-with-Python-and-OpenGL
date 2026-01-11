#!/usr/bin/env python3

from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        # Build program
        vertexShaderCode = """
        in vec3 position;
        void main() {
            gl_Position = vec4(position, 1.0f);
        }
        """

        fragmentShaderCode = """
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0f, 1.0f, 0.0f, 1.0f);
        }
        """

        self.programRef = OpenGLUtils.initialiseProgram(vertexShaderCode, fragmentShaderCode)

        # Setup VAO
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        # Setup vertex attributes
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

        # Set render settings
        glLineWidth(4)

        # Set drawStyle :
        #   GL_LINE_LOOP | GL_LINE_STRIP | GL_LINES | ...
        #   GL_TRIANGLES | GL_TRIANGLE_FAN
        self.drawStyle = GL_LINE_LOOP
    
    def update(self):
        # Render
        glUseProgram(self.programRef)
        glDrawArrays(self.drawStyle, 0, self.vertexCount)

# Launch application
Test().run()