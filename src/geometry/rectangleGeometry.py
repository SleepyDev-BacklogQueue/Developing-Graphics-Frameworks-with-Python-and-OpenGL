from geometry.geometry import Geometry

class RectangleGeometry(Geometry):
    def __init__(self, width=1, height=1, position=[0,0], alignment=[0.5, 0.5]):
        super().__init__()

        # Set position data
        x, y = position
        a, b = alignment
        P = [
            [x + ( -a)*width, y + ( -b)*height,  0.0],
            [x + (1-a)*width, y + ( -b)*height,  0.0],
            [x + ( -a)*width, y + (1-b)*height,  0.0],
            [x + (1-a)*width, y + (1-b)*height,  0.0]
        ]

        positionData = [
            P[0], P[1], P[3],
            P[0], P[3], P[2]
        ]

        # Set color data
        C = [
            [1.0, 1.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ]

        colorData = [
            C[0], C[1], C[3],
            C[0], C[3], C[2]
        ]

        # Set texture coordinates
        T = [
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0]
        ]

        uvData = [
            T[0], T[1], T[3],
            T[0], T[3], T[2]
        ]

        # Add attributes
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)
        self.countVertices()