#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from light.ambientLight import AmbientLight
from light.directionalLight import DirectionalLight
from material.phongMaterial import PhongMaterial
from material.textureMaterial import TextureMaterial
from geometry.rectangleGeometry import RectangleGeometry
from geometry.sphereGeometry import SphereGeometry
from extras.movementRig import MovementRig
from extras.directionalLightHelper import DirectionalLightHelper
from math import pi

class Test(Base):
    def initialise(self):
        self.renderer = Renderer([0.2, 0.2, 0.2])
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 2, 5])

        # Setup lignts
        ambLight = AmbientLight(color=[0.2, 0.2, 0.2])
        self.dirLight = DirectionalLight(color=[0.5, 0.5, 0.5], direction=[-1, -1, 0])
        self.dirLight.setPosition([2, 4, 0])
        self.scene.add(ambLight)
        self.scene.add(self.dirLight)

        directHelper = DirectionalLightHelper(self.dirLight)
        self.dirLight.add(directHelper)

        # Setup meshes
        sphereGeometry = SphereGeometry()
        phongMaterial = PhongMaterial(
            texture=Texture("../images/grid.png"),
            useShadow=True
        )

        sphere1 = Mesh(sphereGeometry, phongMaterial)
        sphere2 = Mesh(sphereGeometry, phongMaterial)
        sphere1.setPosition([-2, 1, 0])
        sphere2.setPosition([1, 2.2, -0.5])
        self.scene.add(sphere1)
        self.scene.add(sphere2)

        self.renderer.enableShadows(self.dirLight)

        # depthTexture = self.renderer.shadowObject.renderTarget.texture
        # shadowDisplay = Mesh(RectangleGeometry(), TextureMaterial(depthTexture))
        # shadowDisplay.setPosition([-1,3,0])
        # self.scene.add(shadowDisplay)

        floor = Mesh(RectangleGeometry(width=20, height=20), phongMaterial)
        floor.rotateX(-pi/2)
        self.scene.add(floor)

    def update(self):
        # View dynamic shadows
        self.dirLight.rotateY(0.01337, False)

        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.camera)

        # Render scene from shadow camera
        # shadowCam = self.renderer.shadowObject.camera
        # self.renderer.render(self.scene, shadowCam)

# Launch application
Test(screenSize=[800, 600]).run()