from geometry.geometry import Geometry

class BoxGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1):
        super().__init__()

        # Set position data
        P = [
            [-width/2, -height/2, -depth/2],
            [ width/2, -height/2, -depth/2],
            [-width/2,  height/2, -depth/2],
            [ width/2,  height/2, -depth/2],
            [-width/2, -height/2,  depth/2],
            [ width/2, -height/2,  depth/2],
            [-width/2,  height/2,  depth/2],
            [ width/2,  height/2,  depth/2]
        ]

        positionData = [
            P[5], P[1], P[3],
            P[5], P[3], P[7],
            P[0], P[4], P[6],
            P[0], P[6], P[2],
            P[6], P[7], P[3],
            P[6], P[3], P[2],
            P[0], P[1], P[5],
            P[0], P[5], P[4],
            P[4], P[5], P[7],
            P[4], P[7], P[6],
            P[1], P[0], P[2],
            P[1], P[2], P[3],
        ]

        # Set color data
        C = [
            [1.0, 0.5, 0.5],
            [0.5, 0.0, 0.0],
            [0.5, 1.0, 0.5],
            [0.0, 0.5, 0.0],
            [0.5, 0.5, 1.0],
            [0.0, 0.0, 0.5]
        ]

        colorData  = 6*[C[0]]
        colorData += 6*[C[1]]
        colorData += 6*[C[2]]
        colorData += 6*[C[3]]
        colorData += 6*[C[4]]
        colorData += 6*[C[5]]

        # Set texture coordinates
        T = [
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0]
        ]

        uvData = 6 * [
            T[0], T[1], T[3],
            T[0], T[3], T[2]
        ]

        # Add attributes
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)
        self.countVertices()