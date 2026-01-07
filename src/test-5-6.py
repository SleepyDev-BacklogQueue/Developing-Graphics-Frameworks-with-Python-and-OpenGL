#!/usr/bin/env python3

from core.base import Base
from core.renderer import Renderer
from core.camera import Camera
from core.scene import Scene
from core.mesh import Mesh
from core.texture import Texture
from geometry.rectangleGeometry import RectangleGeometry
from material.material import Material
from material.textureMaterial import TextureMaterial

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
        float random(vec2 UV) {
            return fract(235711.0 * sin(14.337*UV.x + 42.418*UV.y));
        }

        float boxRandom(vec2 UV, float scale) {
            vec2 iScaleUV = floor(scale * UV);
            return random(iScaleUV);
        }

        float smoothRandom(vec2 UV, float scale) {
            vec2 iScaleUV = floor(scale * UV);
            vec2 fScaleUV = fract(scale * UV);
            float a = random(iScaleUV);
            float b = random(round(iScaleUV + vec2(1,0)));
            float c = random(round(iScaleUV + vec2(0,1)));
            float d = random(round(iScaleUV + vec2(1,1)));
            return mix(
                mix(a, b, fScaleUV.x),
                mix(c, d, fScaleUV.x),
                fScaleUV.y
            );
        }

        float fractalRandom(vec2 UV, float scale) {
            float value = 0.0;
            float amplitude = 0.5;

            for (int i = 0; i < 6; i++) {
                value += amplitude * smoothRandom(UV, scale);
                scale *= 2.0;
                amplitude *= 0.5;
            }

            return value;
        }

        vec4 clouds(vec2 UV) {
            float r = fractalRandom(UV, 5);
            vec4 color1 = vec4(0.5 ,0.5 ,1, 1);
            vec4 color2 = vec4(1, 1, 1, 1);
            return mix(color1, color2, r);
        }
        vec4 lava(vec2 UV) {
            float r = fractalRandom(UV, 40);
            vec4 color1 = vec4(1 , 0.8, 0, 1);
            vec4 color2 = vec4(0.8, 0, 0, 1);
            return mix(color1, color2, r);
        }
        vec4 marble(vec2 UV) {
            float t = fractalRandom(UV, 4);
            float r = abs(sin(20*t));
            vec4 color1 = vec4(0, 0.2, 0, 1);
            vec4 color2 = vec4(1.0, 1.0, 1.0, 1);
            return mix(color1, color2, r);
        }
        vec4 wood(vec2 UV) {
            float t = 80*UV.y + 20 * fractalRandom(UV, 2);
            float r = clamp(2*abs(sin(t)), 0, 1);
            vec4 color1 = vec4(0.3, 0.2, 0, 1);
            vec4 color2 = vec4(0.6, 0.4, 0.2, 1);
            return mix(color1, color2, r);
        }

        in vec2 UV;
        out vec4 fragColor;
        void main() {
            // Choose between noise
            // random(UV) | boxRandom(UV, scale) | smoothRandom(UV, scale) | fractalRandom(UV, scale)
            // float r = random(UV);
            // fragColor = vec4(r,r,r,1);
            
            // Choose between textures
            // clouds(UV) | lava(UV) | marble(UV) | wood(UV)
            fragColor = wood(UV);


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