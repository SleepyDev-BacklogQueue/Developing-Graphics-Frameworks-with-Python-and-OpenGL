from core.attribute import Attribute

class Geometry(object):
    def __init__(self):
        self.attributes = {}
        self.vertexCount = 0

    def addAttribute(self, dataType, variableName, data):
        self.attributes[variableName] = Attribute(dataType, data)

    def countVertices(self):
        attribute = list(self.attributes.values())[0]
        self.vertexCount = len(attribute.data)

    # Modify attributes in place
    def applyMatrix(self, matrix, variableName="vertexPosition"):
        oldPositionData = self.attributes[variableName].data
        newPositionData = []

        # Apply matrix
        for oldPosition in oldPositionData:
            newPos = oldPosition.copy()
            newPos += [1]
            newPos = matrix @ newPos
            newPos = list(newPos[0:3])
            newPositionData += [newPos]
        
        # Update values
        self.attributes[variableName].data = newPositionData
        self.attributes[variableName].uploadData()

    def merge(self, otherGeometry):
        for variableName, attributeObject in self.attributes.items():
            attributeObject.data += otherGeometry.attributes[variableName].data
            attributeObject.uploadData()
        
        self.countVertices()