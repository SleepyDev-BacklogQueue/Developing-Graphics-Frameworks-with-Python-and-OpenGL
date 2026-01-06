#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from geometry.geometry import Geometry
from material.surfaceMaterial import SurfaceMaterial

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)

        # Define scene
        self.scene = Scene()

        # Define custom geometry
        geometry = Geometry()
        P = [
            [-0.1,  0.1,  0.0],
            [ 0.0,  0.0,  0.0],
            [ 0.1,  0.1,  0.0],
            [-0.2, -0.2,  0.0],
            [ 0.2, -0.2,  0.0]
        ]
        posData = [
            P[0], P[3], P[1],
            P[1], P[3], P[4],
            P[1], P[4], P[2]
        ]

        R = [1, 0, 0]
        Y = [1, 1, 0]
        G = [0, 0.25, 0]
        colData = [
            R, G, Y,
            Y, G, G,
            Y, G, R
        ]

        geometry.addAttribute("vec3", "vertexPosition", posData)
        geometry.addAttribute("vec3", "vertexColor", colData)
        geometry.countVertices()

        material = SurfaceMaterial({
            "useVertexColors": True
        })
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()