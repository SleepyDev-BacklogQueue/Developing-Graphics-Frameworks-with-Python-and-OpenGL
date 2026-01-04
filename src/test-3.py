#!/usr/bin/env python3

from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from OpenGL.GL import *
from math import pi

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        ## Build program ##
        vertexShaderCode = """
        in vec3 position;
        uniform mat4 projectionMatrix;
        uniform mat4 modelMatrix;
        void main() {
            gl_Position = projectionMatrix * modelMatrix * vec4(position, 1.0);
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

        ## Setup attributes ##
        positionData = [
            [ 0.0,  0.2, 0.0],
            [ 0.1, -0.2, 0.0],
            [-0.1, -0.2, 0.0]
        ]
        self.vertexCount = len(positionData)
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")

        # ## Setup uniforms ##
        mMatrix = Matrix.makeTranslation(0, 0, -1)
        self.modelMatrix = Uniform("mat4", mMatrix)
        self.modelMatrix.locateVariable(self.programRef, "modelMatrix")

        pMatrix = Matrix.makePerspective()
        self.projectionMatrix = Uniform("mat4", pMatrix)
        self.projectionMatrix.locateVariable(self.programRef, "projectionMatrix")

        # ## Render settings ##
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        ## Animation settings ##
        self.moveSpeed = 0.5
        self.turnSpeed = 90 * pi / 180

    def update(self):
        ## Update data ##
        moveAmount = self.moveSpeed * self.deltaTime
        turnAmount = self.turnSpeed * self.deltaTime

        # Global translation
        if self.input.isKeyPressed("w"):
            m = Matrix.makeTranslation(0, moveAmount, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed("s"):
            m = Matrix.makeTranslation(0, -moveAmount, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed("a"):
            m = Matrix.makeTranslation(-moveAmount, 0, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed("d"):
            m = Matrix.makeTranslation(moveAmount, 0, 0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed("z"):
            m = Matrix.makeTranslation(0, 0, moveAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed("x"):
            m = Matrix.makeTranslation(0, 0, -moveAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data

        # Global rotation
        if self.input.isKeyPressed("q"):
            m = Matrix.makeRotationZ(turnAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed("e"):
            m = Matrix.makeRotationZ(-turnAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data

        # Local translation
        if self.input.isKeyPressed("i"):
            m = Matrix.makeTranslation(0, moveAmount, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed("k"):
            m = Matrix.makeTranslation(0, -moveAmount, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed("j"):
            m = Matrix.makeTranslation(-moveAmount, 0, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed("l"):
            m = Matrix.makeTranslation(moveAmount, 0, 0)
            self.modelMatrix.data = self.modelMatrix.data @ m

        # Local rotation
        if self.input.isKeyPressed("u"):
            m = Matrix.makeRotationZ(turnAmount)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed("o"):
            m = Matrix.makeRotationZ(-turnAmount)
            self.modelMatrix.data = self.modelMatrix.data @ m
        

        ## Render ##
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.programRef)
        self.modelMatrix.uploadData()
        self.projectionMatrix.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

# Launch application
Test().run()