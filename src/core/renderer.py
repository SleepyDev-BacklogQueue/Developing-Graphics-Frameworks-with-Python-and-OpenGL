from core.mesh import Mesh
from light.light import Light
from light.shadow import Shadow
from OpenGL.GL import *
import pygame

class Renderer(object):
    def __init__(self, clearColor=[0.0, 0.0, 0.0]):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(*clearColor, 1)

        self.windowSize = pygame.display.get_surface().get_size()
        self.shadowsEnabled = False

    def enableShadows(self, shadowLight, strength=0.5, resolution=[512,512]):
        self.shadowsEnabled = True
        self.shadowObject = Shadow(shadowLight, strength=strength, resolution=resolution)

    def render(self, scene, camera, clearColor=True, clearDepth=True, renderTarget=None):
        # Extract meshes and lights
        descendantList = scene.getDescendantList()
        meshFilter = lambda x : isinstance(x, Mesh)
        lightFilter = lambda x : isinstance(x, Light)
        meshList = list(filter(meshFilter, descendantList))
        lightList = list(filter(lightFilter, descendantList))

        # Initialise all lights
        while len(lightList) < 4:
            lightList += [Light()]

        # Perform shadow pass
        if self.shadowsEnabled:
            glBindFramebuffer(GL_FRAMEBUFFER, self.shadowObject.renderTarget.framebufferRef)
            glViewport(0,0,self.shadowObject.renderTarget.width, self.shadowObject.renderTarget.height)

            # Clear screen
            glClearColor(1,1,1,1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Bind program
            glUseProgram(self.shadowObject.material.programRef)
            self.shadowObject.updateInternal()

            for mesh in meshList:
                # No rendering
                if not mesh.visible: continue
                if mesh.material.settings["drawStyle"] != GL_TRIANGLES: continue

                # Bind VAO
                glBindVertexArray(mesh.vaoRef)
                self.shadowObject.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix()

                for varName, unifObj in self.shadowObject.material.uniforms.items():
                    unifObj.uploadData()
                glDrawArrays(GL_TRIANGLES, 0, mesh.geometry.vertexCount)

        # Activate render target
        if renderTarget is None:
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glViewport(0, 0, *self.windowSize)
        else:
            glBindFramebuffer(GL_FRAMEBUFFER, renderTarget.framebufferRef)
            glViewport(0, 0, renderTarget.width, renderTarget.height)

        # Clear GL buffers
        if clearColor: glClear(GL_COLOR_BUFFER_BIT)
        if clearDepth: glClear(GL_DEPTH_BUFFER_BIT)

        # Enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Update camera
        camera.updateViewMatrix()

        # Main render pass
        for mesh in meshList:
            # No rendering
            if not mesh.visible: continue

            # Bind program + VAO
            glUseProgram(mesh.material.programRef)
            glBindVertexArray(mesh.vaoRef)

            # Connect camera
            mesh.material.uniforms["modelMatrix"].data = mesh.getWorldMatrix()
            mesh.material.uniforms["viewMatrix"].data = camera.viewMatrix
            mesh.material.uniforms["projectionMatrix"].data = camera.projectionMatrix

            # Check for light uniforms
            if "light0" in mesh.material.uniforms.keys():
                for lightNumber in range(4):
                    lightName = "light" + str(lightNumber)
                    lightObject = lightList[lightNumber]
                    mesh.material.uniforms[lightName].data = lightObject
            if "viewPosition" in mesh.material.uniforms.keys():
                mesh.material.uniforms["viewPosition"].data = camera.getWorldPosition()

            # Include shadow uniform
            if self.shadowsEnabled and "shadow0" in mesh.material.uniforms.keys():
                mesh.material.uniforms["shadow0"].data = self.shadowObject

            # Upload uniforms
            for _, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()
            
            # Update render settings
            mesh.material.updateRenderSettings()

            # Draw
            glDrawArrays(mesh.material.settings["drawStyle"], 0, mesh.geometry.vertexCount)