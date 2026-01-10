from material.material import Material
from OpenGL.GL import *

class FlatMaterial(Material):
    def __init__(self, texture=None, properties={}):
        vertexShaderCode = """
        struct Light {
            int lightType;
            vec3 color;
            vec3 direction;
            vec3 position;
            vec3 attenuation;
        };

        uniform Light light0;
        uniform Light light1;
        uniform Light light2;
        uniform Light light3;

        vec3 lightCalc(Light light, vec3 pointPosition, vec3 pointNormal) {
            float ambient = 0;
            float diffuse = 0;
            float specular = 0;
            float attenuation = 1;
            vec3 lightDirection = vec3(0,0,0);

            if (light.lightType == 1) {
                ambient = 1;
            } else if (light.lightType == 2) {
                lightDirection = normalize(light.direction);
            } else if (light.lightType == 3) {
                lightDirection = normalize(pointPosition - light.position);
                float distance = length(pointPosition - light.position);
                attenuation = 1.0 / (light.attenuation[0] + distance * light.attenuation[1] + distance*distance * light.attenuation[2]);
            }

            if (light.lightType > 1) {
                pointNormal = normalize(pointNormal);
                diffuse = max(dot(pointNormal, -lightDirection), 0.0);
                diffuse *= attenuation;
            }

            return light.color * (ambient + diffuse + specular);
        }

        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        in vec2 vertexUV;
        in vec3 faceNormal;
        out vec2 UV;
        out vec3 light;

        void main() {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            UV = vertexUV;
            vec3 position = vec3(modelMatrix * vec4(vertexPosition, 1.0));
            vec3 normal = normalize(mat3(modelMatrix) * faceNormal);
            light = vec3(0,0,0);
            light += lightCalc(light0, position, normal);
            light += lightCalc(light1, position, normal);
            light += lightCalc(light2, position, normal);
            light += lightCalc(light3, position, normal);
        }
        """

        fragmentShaderCode = """
        uniform vec3 baseColor;
        uniform bool useTexture;
        uniform sampler2D texture;
        in vec2 UV;
        in vec3 light;
        out vec4 fragColor;
        void main() {
            vec4 color = vec4(baseColor, 1.0);
            if (useTexture) {
                color *= texture2D(texture, UV);
            }
            color *= vec4(light, 1);
            fragColor = color;
        }
        """

        super().__init__(vertexShaderCode, fragmentShaderCode)

        self.addUniform("vec3", "baseColor", [1.0,1.0,1.0])
        self.addUniform("Light", "light0", None)
        self.addUniform("Light", "light1", None)
        self.addUniform("Light", "light2", None)
        self.addUniform("Light", "light3", None)
        self.addUniform("bool", "useTexture", texture != None)
        if texture != None:
            self.addUniform("sampler2D", "texture", [texture.textureRef, 1])
        self.locateUniforms()

        # Render settings
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