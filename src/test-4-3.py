#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from geometry.geometry import Geometry
from material.pointMaterial import PointMaterial
from material.lineMaterial import LineMaterial
from numpy import arange
from math import sin

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 4])

        # Define scene
        self.scene = Scene()

        geometry = Geometry()
        posData = []
        for x in arange(-3.2, 3.2, 0.3):
            posData += [[x, sin(x), 0]]
        geometry.addAttribute("vec3", "vertexPosition", posData)
        geometry.countVertices()

        pointMaterial = PointMaterial({
            "baseColor": [1, 1, 0],
            "pointSize": 10
        })

        lineMaterial = LineMaterial({
            "baseColor": [1, 0, 1],
            "lineWidth": 4
        })

        self.pointMesh = Mesh(geometry, pointMaterial)
        self.lineMesh = Mesh(geometry, lineMaterial)
        self.scene.add(self.pointMesh)
        self.scene.add(self.lineMesh)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()