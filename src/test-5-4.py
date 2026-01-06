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
        uniform sampler2D texture1;
        uniform sampler2D texture2;
        in vec2 UV;
        uniform float time;
        out vec4 fragColor;

        void main() {
            vec4 color1 = texture2D(texture1, UV);
            vec4 color2 = texture2D(texture2, UV);
            float s = abs(sin(time));
            fragColor = s * color1 + (1.0 - s) * color2;
        }
        """
        self.blendMaterial = Material(vertexShaderCode, fragmentShaderCode)
        
        gridTexture = Texture("../images/grid.png")
        crateTexture = Texture("../images/crate.png")
        self.blendMaterial.addUniform("sampler2D", "texture1", [gridTexture.textureRef, 1])
        self.blendMaterial.addUniform("sampler2D", "texture2", [crateTexture.textureRef, 2])
        self.blendMaterial.addUniform("float", "time", 0.0)
        self.blendMaterial.locateUniforms()
        self.mesh = Mesh(geometry, self.blendMaterial)
        self.scene.add(self.mesh)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.blendMaterial.uniforms["time"].data += self.deltaTime
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()