from OpenGL.GL import *
import numpy as np

class Attribute(object):
    def __init__(self, dataType, data):
        # dataType is expected to have values
        #   int | float | vec2 | vec3 | vec4
        self.dataType = dataType
        self.data = data

        # Manage OpenGL data
        self.bufferRef = glGenBuffers(1)
        self.uploadData()

    def uploadData(self):
        # Convert data to raw format
        if self.dataType == "int":
            data = np.array(self.data).astype(np.int32)
        else:
            data = np.array(self.data).astype(np.float32)
        
        # Upload data
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associateVariable(self, programRef, variableName):
        # Fetch location
        variableRef = glGetAttribLocation(programRef, variableName)
        if variableRef == -1: return

        # Associate variable
        if self.dataType == "int":
            glVertexAttribPointer(variableRef, 1, GL_INT, False, 0, None)
        elif self.dataType == "float":
            glVertexAttribPointer(variableRef, 1, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec2":
            glVertexAttribPointer(variableRef, 2, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec3":
            glVertexAttribPointer(variableRef, 3, GL_FLOAT, False, 0, None)
        elif self.dataType == "vec4":
            glVertexAttribPointer(variableRef, 4, GL_FLOAT, False, 0, None)
        else:
            raise Exception(f"Attribute {variableName}, has unknown type {self.dataType}")
        
        # Enable variable
        glEnableVertexAttribArray(variableRef)