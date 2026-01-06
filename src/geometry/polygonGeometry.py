from geometry.geometry import Geometry
from math import sin, cos, pi

class PolygonGeometry(Geometry):
    def __init__(self, sides=3, radius=1):
        super().__init__()

        # Set attribute data
        positionData = []
        colorData = []
        uvData = []
        A = 2 * pi / sides
        for i in range(sides):
            positionData += [
                [0, 0, 0],
                [radius*cos(i*A), radius*sin(i*A), 0],
                [radius*cos((i+1)*A), radius*sin((i+1)*A), 0]
            ]

            colorData += [
                [1.0, 1.0, 1.0],
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0]
            ]

            uvData += [
                [0.5, 0.5]
                [0.5 + 0.5*cos(i*A),     0.5 + 0.5*sin(i*A)],
                [0.5 + 0.5*cos((i+1)*A), 0.5 + 0.5*sin((i+1)*A)]
            ]


        # Add attributes
        self.addAttribute("vertexPosition", "vec3", positionData)
        self.addAttribute("vertexColor", "vec3", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)
        self.countVertices()