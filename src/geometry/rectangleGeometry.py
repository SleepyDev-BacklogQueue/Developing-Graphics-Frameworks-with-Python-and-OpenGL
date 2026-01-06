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

        # Add attributes
        self.addAttribute("vertexPosition", "vec3", positionData)
        self.addAttribute("vertexColor", "vec3", colorData)
        self.countVertices()