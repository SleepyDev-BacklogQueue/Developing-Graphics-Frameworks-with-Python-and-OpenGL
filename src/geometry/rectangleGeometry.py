from geometry.geometry import Geometry

class RectangleGeometry(Geometry):
    def __init__(self, width=1, height=1):
        super().__init__()

        # Set position data
        P = [
            [-width/2, -height/2,  0.0],
            [ width/2, -height/2,  0.0],
            [-width/2,  height/2,  0.0],
            [ width/2,  height/2,  0.0]
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