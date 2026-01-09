from core.mesh import Mesh
from OpenGL.GL import *
import pygame

class Renderer(object):
    def __init__(self, clearColor=[0.0, 0.0, 0.0]):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(clearColor[0], clearColor[1], clearColor[2], 1)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.windowSize = pygame.display.get_surface().get_size()

    def render(self, scene, camera, clearColor=True, clearDepth=True, renderTarget=None):
        # Activate render target
        if (renderTarget == None):
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glViewport(0, 0, self.windowSize[0], self.windowSize[1])
        else:
            glBindFramebuffer(GL_FRAMEBUFFER, renderTarget.framebufferRef)
            glViewport(0, 0, renderTarget.width, renderTarget.height)

        if clearColor:
            glClear(GL_COLOR_BUFFER_BIT)
        if clearDepth:
            glClear(GL_DEPTH_BUFFER_BIT)

        camera.updateViewMatrix()

        # Extract meshes
        descendantList = scene.getDescendantList()
        meshFilter = lambda x : isinstance(x, Mesh)
        meshList = list(filter(meshFilter, descendantList))

        for mesh in meshList:
            if not mesh.visible: continue

            glUseProgram(mesh.material.programRef)
            glBindVertexArray(mesh.vaoRef)
            mesh.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix()
            mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix

            for _, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()
            
            mesh.material.updateRenderSettings()

            glDrawArrays(mesh.material.settings["drawStyle"], 0, mesh.geometry.vertexCount)