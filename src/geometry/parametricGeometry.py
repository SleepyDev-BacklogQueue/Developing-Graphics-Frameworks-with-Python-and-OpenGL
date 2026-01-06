from geometry.geometry import Geometry

class ParametricGeometry(Geometry):
    def __init__(self, uStart, uEnd, uResolution, vStart, vEnd, vResolution, surfaceFunction):
        super().__init__()

        # Generate positions from input space
        positions = []
        uvs = []

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

        for uIndex in range(uResolution+1):
            vArray = []
            for vIndex in range(vResolution+1):
                u = uIndex/uResolution
                v = vIndex/vResolution

                vArray += [[u, v]]
            uvs += [vArray]

        # Group attributes into quads
        positionData = []
        colorData = []
        uvData = []
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
                    quadPosition[3].copy(),
                    quadPosition[0].copy(),
                    quadPosition[3].copy(),
                    quadPosition[2].copy()
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

                # Set uvData
                uvQuad = [
                    uvs[xIndex  ][yIndex  ],
                    uvs[xIndex+1][yIndex  ],
                    uvs[xIndex  ][yIndex+1],
                    uvs[xIndex+1][yIndex+1]
                ]
                uvData += [
                    uvQuad[0],
                    uvQuad[1],
                    uvQuad[3],
                    uvQuad[0],
                    uvQuad[3],
                    uvQuad[2]
                ]

        # Add attributes
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)
        self.countVertices()