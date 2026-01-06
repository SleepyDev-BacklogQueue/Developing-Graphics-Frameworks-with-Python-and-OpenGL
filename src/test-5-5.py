#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from core.texture import Texture
from geometry.rectangleGeometry import RectangleGeometry
from material.material import Material

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 1.5])

        # Define scene
        self.scene = Scene()

        geometry = RectangleGeometry()
        vertexShaderCode = """
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        out vec2 UV;

        void main() {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV;
        }
        """

        fragmentShaderCode = """
        uniform sampler2D noise;
        uniform sampler2D image;
        in vec2 UV;
        uniform float time;
        out vec4 fragColor;

        void main() {
            vec2 uvShift = UV + vec2(-0.033, 0.07) * time;
            vec4 noiseValues = texture2D(noise, uvShift);
            vec2 uvNoise = UV + 0.4 * noiseValues.rg;
            fragColor = texture2D(image, uvNoise);
        }
        """
        self.distortMaterial = Material(vertexShaderCode, fragmentShaderCode)
        
        noiseTexture = Texture("../images/noise.png")
        gridTexture = Texture("../images/grid.png")
        self.distortMaterial.addUniform("sampler2D", "noise", [noiseTexture.textureRef, 1])
        self.distortMaterial.addUniform("sampler2D", "image", [gridTexture.textureRef, 2])
        self.distortMaterial.addUniform("float", "time", 0.0)
        self.distortMaterial.locateUniforms()
        self.mesh = Mesh(geometry, self.distortMaterial)
        self.scene.add(self.mesh)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.distortMaterial.uniforms["time"].data += self.deltaTime
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()