from material.material import Material
from OpenGL.GL import *

class TextureMaterial(Material):
    def __init__(self, texture, properties={}):
        vertexShaderCode = """
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        uniform vec2 repeatUV;
        uniform vec2 offsetUV;
        out vec2 UV;

        void main() {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV * repeatUV + offsetUV;
        }
        """

        fragmentShaderCode = """
        in vec2 UV;

        uniform vec3 baseColor;
        uniform sampler2D texture;
        out vec4 fragColor;

        void main() {
            vec4 color = vec4(baseColor, 1.0) * texture2D(texture, UV);
            if (color.a < 0.1) discard;
            fragColor = color;
        }
        """

        super().__init__(vertexShaderCode, fragmentShaderCode)

        self.addUniform("vec3", "baseColor", [1,1,1])
        self.addUniform("sampler2D", "texture", [texture.textureRef, 1])
        self.addUniform("vec2", "repeatUV", [1,1])
        self.addUniform("vec2", "offsetUV", [0,0])
        self.locateUniforms()

        self.settings["doubleSide"] = True
        self.settings["wireframe"] = False
        self.settings["lineWidth"] = 1

        self.setProperties(properties)

    def updateRenderSettings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self.settings["lineWidth"])