#!/usr/bin/env python3

from core.base import Base
from core.openGLUtils import OpenGLUtils
from OpenGL.GL import *

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        # Build program
        vertexShaderCode = """
        void main() {
            gl_Position = vec4(0.0f, 0.0f, 0.0f, 1.0f);
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

        # Set render settings
        glPointSize(10)
    
    def update(self):
        # Render
        glUseProgram(self.programRef)
        glDrawArrays(GL_POINTS, 0, 1)

# Launch application
Test().run()