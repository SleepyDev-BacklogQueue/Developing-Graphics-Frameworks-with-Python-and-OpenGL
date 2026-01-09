#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from core.texture import Texture
from geometry.rectangleGeometry import RectangleGeometry
from geometry.sphereGeometry import SphereGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.movementRig import MovementRig
from extras.postprocessor import Postprocessor
from effect.tintEffect import TintEffect
from effect.invertEffect import InvertEffect
from effect.pixelateEffect import PixelateEffect
from effect.vignetteEffect import VignetteEffect
from effect.colorReduceEffect import ColorReduceEffect
from math import pi

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)

        # Define scene
        self.scene = Scene()

        skyGeometry = SphereGeometry(radius=50)
        skyMaterial = TextureMaterial(
            Texture("../images/sky-earth.jpg")
        )
        sky = Mesh(skyGeometry, skyMaterial)
        self.scene.add(sky)

        grassGeometry = RectangleGeometry(width=100, height=100)
        grassMaterial = TextureMaterial(
            Texture("../images/grass.jpg"),
            {"repeatUV": [50,50]}
        )
        grass = Mesh(grassGeometry, grassMaterial)
        grass.rotateX(-pi/2)
        self.scene.add(grass)

        sphereGeometry = SphereGeometry()
        sphereMaterial = TextureMaterial(Texture("../images/grid.png"))
        self.sphere = Mesh(sphereGeometry, sphereMaterial)
        self.sphere.setPosition([0,1,0])
        self.scene.add(self.sphere)

        # Define input rig
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 1, 4])
        self.scene.add(self.rig)

        self.postprocessor = Postprocessor(self.renderer, self.scene, self.camera)
        self.postprocessor.addEffect(TintEffect(tintColor=[0,1,0]))
        self.postprocessor.addEffect(ColorReduceEffect(levels=5))
        self.postprocessor.addEffect(PixelateEffect(resolution=[800,600]))
        # self.postprocessor.addEffect(VignetteEffect())
        # self.postprocessor.addEffect(InvertEffect())


    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.rig.update(self.input, self.deltaTime)
        # self.renderer.render(self.scene, self.camera)
        self.postprocessor.render()

# Launch application
Test(screenSize=[800,600]).run()