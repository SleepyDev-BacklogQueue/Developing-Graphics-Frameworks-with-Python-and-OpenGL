#!/usr/bin/env python3

from core.base import Base
from core.openGLUtils import OpenGLUtils
from OpenGL.GL import *

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        ## Build program ##
        vertexShaderCode = """
        void main() {
            gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
        }
        """

        fragmentShaderCode = """
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """

        self.programRef = OpenGLUtils.initialiseProgram(vertexShaderCode, fragmentShaderCode)

        ## Setup VAO ##
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        ## Render settings (optional) ##
        glPointSize(10)
    
    def update(self):
        glUseProgram(self.programRef)
        glDrawArrays(GL_POINTS, 0, 1)

# Launch application
Test().run()