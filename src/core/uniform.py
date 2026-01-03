from OpenGL.GL import *

class Uniform(object):
    def __init__(self, dataType, data):
        # dataType is expected to have values
        #   int | bool | float | vec2 | vec3 | vec4
        self.dataType = dataType
        self.data = data

        # Manage OpenGL data
        self.variableRef = -1
    
    def locateVariable(self, programRef, variableName):
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
            glUniform2f(self.variableRef, self.data[0], self.data[1])
        elif self.dataType == "vec3":
            glUniform3f(self.variableRef, self.data[0], self.data[1], self.data[2])
        elif self.dataType == "vec4":
            glUniform4f(self.variableRef, self.data[0], self.data[1], self.data[2], self.data[3])
        else:
            raise Exception(f"Uniform has unknown type {self.dataType}")