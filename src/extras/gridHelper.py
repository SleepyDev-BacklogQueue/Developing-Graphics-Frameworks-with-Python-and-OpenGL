from core.mesh import Mesh
from geometry.geometry import Geometry
from material.lineMaterial import LineMaterial

class GridHelper(Mesh):
    def __init__(self, size=10, divisions=10, gridColor=[0, 0, 0], centerColor=[0.5,0.5,0.5], lineWidth=1):
        geo = Geometry()
        positionData = []
        colorData = []

        # Create interval values
        values = []
        deltaSize = size/divisions
        for n in range(divisions+1):
            values += [-size/2 + n*deltaSize]

        # Add vertical lines
        for x in values:
            positionData += [[x, -size/2, 0]]
            positionData += [[x,  size/2, 0]]
            if x == 0:
                colorData += [centerColor]
                colorData += [centerColor]
            else:
                colorData += [gridColor]
                colorData += [gridColor]

        # Add horizontal lines
        for y in values:
            positionData += [[-size/2, y, 0]]
            positionData += [[ size/2, y, 0]]
            if y == 0:
                colorData += [centerColor]
                colorData += [centerColor]
            else:
                colorData += [gridColor]
                colorData += [gridColor]

        geo.addAttribute("vec3", "vertexPosition", positionData)
        geo.addAttribute("vec3", "vertexColor",    colorData)
        geo.countVertices()

        mat = LineMaterial({
            "useVertexColors": True,
            "lineWidth": lineWidth,
            "lineType": "segments"
        })

        super().__init__(geo, mat)