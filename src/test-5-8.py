#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from core.texture import Texture
from core.matrix import Matrix
from geometry.rectangleGeometry import RectangleGeometry
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.textTexture import TextTexture
from extras.movementRig import MovementRig
from math import pi

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)

        # Define scene
        self.scene = Scene()

        labelGeometry = RectangleGeometry(width=1, height=0.5)
        labelGeometry.applyMatrix(Matrix.makeRotationY(pi))
        labelTexture = TextTexture(
            text=" This is a Crate. ",
            systemFontName="Arial Bold",
            fontSize=40,
            fontColor=[0,0,200],
            imageWidth=256,
            imageHeight=128,
            alignHorizontal=0.5,
            alignVertical=0.5,
            imageBorderWidth=4,
            imageBorderColor=[255,0,0]
        )
        labelMaterial = TextureMaterial(labelTexture)
        self.label = Mesh(labelGeometry, labelMaterial)
        self.label.setPosition([0,1,0])
        self.scene.add(self.label)

        crateGeometry = BoxGeometry()
        crateTexture = Texture("../images/crate.png")
        crateMaterial = TextureMaterial(crateTexture)
        crate = Mesh(crateGeometry, crateMaterial)
        self.scene.add(crate)

        # Define input rig
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 1, 5])
        self.scene.add(self.rig)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.rig.update(self.input, self.deltaTime)
        self.label.lookAt(self.camera.getWorldPosition())
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()