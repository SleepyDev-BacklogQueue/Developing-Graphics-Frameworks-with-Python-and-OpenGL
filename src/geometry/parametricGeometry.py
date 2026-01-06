from geometry.geometry import Geometry

class PolygonGeometry(Geometry):
    def __init__(self, uStart, uEnd, uResolution, vStart, vEnd, vResolution, surfaceFunction):
        super().__init__()

        # Generate positions from input space
        positions = []

        uDelta = (uEnd - uStart) / uResolution
        vDelta = (vEnd - vStart) / vResolution
        for uIndex in range(uResolution+1):
            vArray = []
            for vIndex in range(vResolution+1):
                u = uStart + uIndex * uDelta
                v = vStart + vIndex * vDelta

                vArray += [surfaceFunction(u, v)]
            positions += [vArray]

        C = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]

        # Group attributes into quads
        positionData = []
        colorData = []
        for xIndex in range(uResolution):
            for yIndex in range(vResolution):
                # Set positionData
                quadPosition = [
                    positions[xIndex  ][yIndex  ],
                    positions[xIndex+1][yIndex  ],
                    positions[xIndex  ][yIndex+1],
                    positions[xIndex+1][yIndex+1]
                ]

                positionData += [
                    quadPosition[0].copy(),
                    quadPosition[1].copy(),
                    quadPosition[2].copy(),
                    quadPosition[0].copy(),
                    quadPosition[2].copy(),
                    quadPosition[3].copy(),
                ]

                # Set colorData
                colorData += [
                    C[0],
                    C[1],
                    C[2],
                    C[3],
                    C[4],
                    C[5]
                ]

        # Add attributes
        self.addAttribute("vertexPosition", "vec3", positionData)
        self.addAttribute("vertexColor", "vec3", colorData)
        self.countVertices()