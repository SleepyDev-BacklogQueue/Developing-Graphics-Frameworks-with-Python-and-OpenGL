#!/usr/bin/env python3

from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        ## Build program ##
        vertexShaderCode = """
        in vec3 position;
        uniform vec3 translation;
        void main() {
            vec3 pos = position + translation;
            gl_Position = vec4(pos, 1.0);
        }
        """

        fragmentShaderCode = """
        uniform vec3 baseColor;
        out vec4 fragColor;
        void main() {
            fragColor = vec4(baseColor, 1.0);
        }
        """

        self.programRef = OpenGLUtils.initialiseProgram(vertexShaderCode, fragmentShaderCode)

        ## Setup VAO ##
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        ## Setup attributes ##
        positionData = [
            [ 0.0,  0.2,  0.0],
            [ 0.2, -0.2,  0.0],
            [-0.2, -0.2,  0.0]
        ]
        self.vertexCount = len(positionData)
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")

        ## Setup uniforms ##
        self.translation = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.translation.locateVariable(self.programRef, "translation")

        self.baseColor = Uniform("vec3", [1.0, 0.0, 0.0])
        self.baseColor.locateVariable(self.programRef, "baseColor")

        ## Render settings (optional) ##
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def update(self):
        ## Update ##
        self.translation.data[0] += 0.01
        if self.translation.data[0] > 1.2:
            self.translation.data[0] = -1.2

        ## Render ##
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.programRef)
        self.translation.uploadData()
        self.baseColor.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)


# Launch application
Test().run()