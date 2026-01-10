#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from core.texture import Texture
from geometry.rectangleGeometry import RectangleGeometry
from geometry.sphereGeometry import SphereGeometry
from light.ambientLight import AmbientLight
from light.directionalLight import DirectionalLight
from light.pointLight import PointLight
from material.flatMaterial import FlatMaterial
from material.lambertMaterial import LambertMaterial
from material.phongMaterial import PhongMaterial
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.movementRig import MovementRig

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 2.5])

        # Define scene
        self.scene = Scene()

        # Define input
        self.rig = MovementRig(unitsPerSecond=5)
        self.scene.add(self.rig)

        ambientLight = AmbientLight(color=[0.1,0.1,0.1])
        pointLight   = PointLight(color=[1,1,1], position=[1.2,1.2,0.3])
        self.scene.add(ambientLight)
        self.scene.add(pointLight)

        geometry = RectangleGeometry()
        colorTex = Texture("../images/brick-color.jpg")
        bumpTex = Texture("../images/brick-bump.jpg")
        bumpMaterial = LambertMaterial(
            texture = colorTex,
            bumpTexture=bumpTex,
            properties={
                "bumpStrength": 1
            }
        )
        self.mesh = Mesh(geometry, bumpMaterial)
        self.rig.add(self.mesh)
        # self.scene.add(self.mesh)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()