#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
from extras.axesHelper import AxesHelper
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
from math import pi

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0.5, 1, 0.5])

        # Define scene
        self.scene = Scene()

        axes = AxesHelper(axisLength=2)
        self.scene.add(axes)

        grid = GridHelper(size=20, gridColor=[1,1,1], centerColor=[1,1,0])
        grid.rotateX(-pi/2)
        self.scene.add(grid)

        # Define input rig
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0.5, 1, 5])
        self.scene.add(self.rig)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()