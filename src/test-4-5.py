#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from geometry.sphereGeometry import SphereGeometry
from material.material import Material
from material.surfaceMaterial import SurfaceMaterial

class Test(Base):
    def initialise(self):
        print("Initialising program...")

        self.renderer = Renderer()

        # Define camera
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 7])

        # Define scene
        self.scene = Scene()

        geometry = SphereGeometry(radius=3, radiusSegments=128, heightSegments=64)

        vertexShaderCode = """
            uniform mat4 modelMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 projectionMatrix;
            uniform float time;
            in vec3 vertexPosition;
            in vec3 vertexColor;
            out vec3 color;
            void main() {
                float offset = 0.2 * sin(8.0 * vertexPosition.x + time);
                vec3 pos = vertexPosition + vec3(0.0f, offset, 0.0);
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
                color = vertexColor;
            }
        """

        fragmentShaderCode = """
        uniform float time;
        in vec3 color;
        out vec4 fragColor;
        void main() {
            float r = abs(sin(time));
            vec4 c = vec4(r, -0.5*r, -0.5*r, 0.0);
            fragColor = vec4(color, 1.0) + c;
        }
        """
        material = Material(vertexShaderCode, fragmentShaderCode)
        material.addUniform("float", "time", 0)
        material.locateUniforms()

        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

        # Time data
        self.time = 0

    def update(self):
        # Update time
        self.time += 1/60
        self.mesh.material.uniforms["time"].data = self.time

        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()