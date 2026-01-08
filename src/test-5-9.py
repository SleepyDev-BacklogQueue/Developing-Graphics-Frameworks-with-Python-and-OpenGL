#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from core.texture import Texture
from geometry.rectangleGeometry import RectangleGeometry
from geometry.boxGeometry import BoxGeometry
from material.spriteMaterial import SpriteMaterial
from material.textureMaterial import TextureMaterial
from extras.movementRig import MovementRig
from extras.gridHelper import GridHelper
from math import floor, pi

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)

        # Define scene
        self.scene = Scene()

        geometry = RectangleGeometry()
        tileSet = Texture("../images/rolling-ball.png")
        spriteMaterial = SpriteMaterial(
            tileSet, {
                "billboard" : True,
                "tileCount" : [4,4],
                "tileNumber" : 0
            }
        )
        self.tilesPerSecond = 8
        self.sprite = Mesh(geometry, spriteMaterial)
        self.scene.add(self.sprite)

        grid = GridHelper()
        grid.rotateX(-pi/2)
        self.scene.add(grid)

        # Define input rig
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 0.5, 3])
        self.scene.add(self.rig)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        tileNumber = floor(self.time * self.tilesPerSecond)
        self.sprite.material.uniforms["tileNumber"].data = tileNumber
        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()