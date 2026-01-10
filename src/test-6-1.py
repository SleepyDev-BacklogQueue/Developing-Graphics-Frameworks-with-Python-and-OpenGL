#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from core.texture import Texture
from geometry.boxGeometry import BoxGeometry
from geometry.sphereGeometry import SphereGeometry
from light.ambientLight import AmbientLight
from light.directionalLight import DirectionalLight
from light.pointLight import PointLight
from material.flatMaterial import FlatMaterial
from material.lambertMaterial import LambertMaterial
from material.phongMaterial import PhongMaterial
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.directionalLightHelper import DirectionalLightHelper
from extras.pointLightHelper import PointLightHelper
from math import sin

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 6])

        # Define scene
        self.scene = Scene()

        ambient = AmbientLight(color=[0.1, 0.1, 0.1])
        self.directional = DirectionalLight(color=[0.8,0.8,0.8], direction=[-1,-1,-2])
        self.point = PointLight(color=[0.9,0,0], position=[1,1,0.8])
        self.scene.add(ambient)
        self.scene.add(self.directional)
        self.scene.add(self.point)
        
        sphereGeometry = SphereGeometry()
        flatMaterial = FlatMaterial(
            properties={
                "baseColor": [0.6,0.2,0.2]
            }
        )
        grid = Texture("../images/grid.png")
        lambertMaterial = LambertMaterial(texture=grid)
        phongMaterial = PhongMaterial(
            properties={
                "baseColor": [0.5,0.5,1]
            }
        )

        sphere1 = Mesh(sphereGeometry, flatMaterial)
        sphere2 = Mesh(sphereGeometry, lambertMaterial)
        sphere3 = Mesh(sphereGeometry, phongMaterial)

        sphere1.setPosition([-2.2, 0,0])
        sphere2.setPosition([0, 0,0])
        sphere3.setPosition([2.2, 0,0])

        self.scene.add(sphere1)
        self.scene.add(sphere2)
        self.scene.add(sphere3)

        directHelper = DirectionalLightHelper(self.directional)
        self.directional.setPosition([3, 2, 0])
        self.directional.add(directHelper)
        pointHelper = PointLightHelper(self.point)
        self.point.add(pointHelper)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.directional.setDirection([-1, sin(0.7*self.time), -2])
        self.point.setPosition([1, sin(self.time), 0.8])
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()