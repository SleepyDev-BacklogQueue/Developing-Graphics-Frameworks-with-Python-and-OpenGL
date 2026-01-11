#!/usr/bin/env python3

from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *

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
        self.translation1 = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.baseColor1 = Uniform("vec3", [1.0, 0.0, 0.0])
        self.translation1.locateVariable(self.programRef, "translation")
        self.baseColor1.locateVariable(self.programRef, "baseColor")

        self.translation2 = Uniform("vec3", [ 0.5, 0.0, 0.0])
        self.baseColor2 = Uniform("vec3", [0.0, 0.0, 1.0])
        self.translation2.locateVariable(self.programRef, "translation")
        self.baseColor2.locateVariable(self.programRef, "baseColor")

    def update(self):
        # Draw 1st object
        glUseProgram(self.programRef)
        self.translation1.uploadData()
        self.baseColor1.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

        # Draw 2nd object
        glUseProgram(self.programRef)
        self.translation2.uploadData()
        self.baseColor2.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

# Launch application
Test().run()