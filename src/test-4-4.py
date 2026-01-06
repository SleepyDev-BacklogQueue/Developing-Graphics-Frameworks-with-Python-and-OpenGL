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

        geometry = SphereGeometry(radius=3)

        vertexShaderCode = """
            uniform mat4 modelMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 projectionMatrix;
            in vec3 vertexPosition;
            out vec3 position;
            void main() {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                position = vertexPosition;
            }
        """
        fragmentShaderCode = """
        in vec3 position;
        out vec4 fragColor;
        void main() {
            vec3 color = mod(position, 1.0);
            fragColor = vec4(color, 1.0);
        }
        """
        material = Material(vertexShaderCode, fragmentShaderCode)
        material.locateUniforms()

        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        # self.mesh.rotateY(0.0514)
        # self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)

# Launch application
Test(screenSize=[800,600]).run()