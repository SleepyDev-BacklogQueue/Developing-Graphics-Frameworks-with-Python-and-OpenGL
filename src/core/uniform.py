from OpenGL.GL import *

class Uniform(object):
    def __init__(self, dataType, data):
        # dataType is expected to have values:
        #   int | bool | float | vec2 | vec3 | vec4 | mat4 | sampler2D | Light | Shadow
        self.dataType = dataType
        self.data = data

        # Manage OpenGL data
        self.variableRef = -1
    
    def locateVariable(self, programRef, variableName):
        # Locate all variables for struct Light
        if self.dataType == "Light":
            self.variableRef = {}
            self.variableRef["lightType"]   = glGetUniformLocation(programRef, variableName + ".lightType")
            self.variableRef["color"]       = glGetUniformLocation(programRef, variableName + ".color")
            self.variableRef["direction"]   = glGetUniformLocation(programRef, variableName + ".direction")
            self.variableRef["position"]    = glGetUniformLocation(programRef, variableName + ".position")
            self.variableRef["attenuation"] = glGetUniformLocation(programRef, variableName + ".attenuation")
        # Locate all variables for struct Shadow
        elif self.dataType == "Shadow":
            self.variableRef = {}
            self.variableRef["lightDirection"]   = glGetUniformLocation(programRef, variableName + ".lightDirection")
            self.variableRef["projectionMatrix"] = glGetUniformLocation(programRef, variableName + ".projectionMatrix")
            self.variableRef["viewMatrix"]       = glGetUniformLocation(programRef, variableName + ".viewMatrix")
            self.variableRef["depthTexture"]     = glGetUniformLocation(programRef, variableName + ".depthTexture")
            self.variableRef["strength"]         = glGetUniformLocation(programRef, variableName + ".strength")
            self.variableRef["bias"]             = glGetUniformLocation(programRef, variableName + ".bias")
        # Locate uniform variable
        else:
            self.variableRef = glGetUniformLocation(programRef, variableName)
    
    def uploadData(self):
        # Assert location
        if self.variableRef == -1: return
        
        # Upload data
        if self.dataType == "int":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "bool":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "float":
            glUniform1f(self.variableRef, self.data)
        elif self.dataType == "vec2":
            glUniform2f(self.variableRef, *self.data)
        elif self.dataType == "vec3":
            glUniform3f(self.variableRef, *self.data)
        elif self.dataType == "vec4":
            glUniform4f(self.variableRef, *self.data)
        elif self.dataType == "mat4":
            glUniformMatrix4fv(self.variableRef, 1, GL_TRUE, self.data)
        elif self.dataType == "sampler2D":
            # Fetch intermediate data
            textureObjectRef, textureUnitRef = self.data

            # Upload texture data
            glActiveTexture(GL_TEXTURE0 + textureUnitRef)
            glBindTexture(GL_TEXTURE_2D, textureObjectRef)
            glUniform1i(self.variableRef, textureUnitRef)
        elif self.dataType == "Light":
            # Fetch intermediate data
            direction = self.data.getDirection()
            position = self.data.getPosition()

            # Upload all data to struct Light
            glUniform1i(self.variableRef["lightType"], self.data.lightType)
            glUniform3f(self.variableRef["color"], *self.data.color)
            glUniform3f(self.variableRef["direction"], *direction)
            glUniform3f(self.variableRef["position"], *position)
            glUniform3f(self.variableRef["attenuation"], *self.data.attenuation)
        elif self.dataType == "Shadow":
            # Fetch intermediate data
            direction = self.data.lightSource.getDirection()
            textureObjectRef = self.data.renderTarget.texture.textureRef
            textureUnitRef = 15

            # Upload all data to struct Shadow
            glUniform3f(self.variableRef["lightDirection"], *direction)
            glUniformMatrix4fv(self.variableRef["projectionMatrix"], 1, GL_TRUE, self.data.camera.projectionMatrix)
            glUniformMatrix4fv(self.variableRef["viewMatrix"], 1, GL_TRUE, self.data.camera.viewMatrix)
            glActiveTexture(GL_TEXTURE0 + textureUnitRef)
            glBindTexture(GL_TEXTURE_2D, textureObjectRef)
            glUniform1i(self.variableRef["depthTexture"], textureUnitRef)
            glUniform1f(self.variableRef["strength"], self.data.strength)
            glUniform1f(self.variableRef["bias"], self.data.bias)
        else:
            raise Exception(f"Uniform has unknown type {self.dataType}")