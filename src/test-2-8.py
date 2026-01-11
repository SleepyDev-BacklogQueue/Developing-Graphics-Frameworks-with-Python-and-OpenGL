#!/usr/bin/env python3

from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *
from math import sin, cos

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        # Build program
        vertexShaderCode = """
        in vec3 position;
        uniform vec3 translation;
        void main() {
            vec3 pos = position + translation;
            gl_Position = vec4(pos, 1.0f);
        }
        """

        fragmentShaderCode = """
        uniform vec3 baseColor;
        out vec4 fragColor;
        void main() {
            fragColor = vec4(baseColor, 1.0f);
        }
        """

        self.programRef = OpenGLUtils.initialiseProgram(vertexShaderCode, fragmentShaderCode)

        # Setup VAO
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        # Setup vertex attributes
        positionData = [
            [ 0.0,  0.2,  0.0],
            [ 0.2, -0.2,  0.0],
            [-0.2, -0.2,  0.0]
        ]
        self.vertexCount = len(positionData)
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")

        # Setup uniforms
        self.translation = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.baseColor = Uniform("vec3", [1.0, 0.0, 0.0])
        self.translation.locateVariable(self.programRef, "translation")
        self.baseColor.locateVariable(self.programRef, "baseColor")

        # Render settings
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def update(self):
        # Update
        self.translation.data[0] = 0.75 * cos(self.time)
        self.translation.data[1] = 0.75 * sin(self.time)

        # Render
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.programRef)
        self.translation.uploadData()
        self.baseColor.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

# Launch application
Test().run()