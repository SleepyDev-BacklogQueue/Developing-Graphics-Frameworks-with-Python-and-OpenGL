#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 4])

        # Define scene
        self.scene = Scene()

        geometry = BoxGeometry()
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