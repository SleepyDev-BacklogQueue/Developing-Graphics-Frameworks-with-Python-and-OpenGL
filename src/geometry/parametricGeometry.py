from geometry.geometry import Geometry
import numpy as np

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

        def calcNormal(P0, P1, P2):
            v1 = np.array(P1) - np.array(P0)
            v2 = np.array(P2) - np.array(P0)
            normal = np.cross(v1, v2)
            normal /= np.linalg.norm(normal)
            return normal

        vertexNormals = []
        for uIndex in range(uResolution+1):
            vArray = []
            for vIndex in range(vResolution+1):
                u = uStart + uIndex * uDelta
                v = vStart + vIndex * vDelta
                h = 0.0001
                P0 = surfaceFunction(u, v)
                P1 = surfaceFunction(u+h, v)
                P2 = surfaceFunction(u, v+h)
                normalVector = calcNormal(P0, P1, P2)
                vArray += [normalVector]
            vertexNormals += [vArray]

        # Group attributes into quads
        positionData = []
        colorData = []
        uvData = []
        vertexNormalData = []
        faceNormalData = []
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

                # Set normals
                nQuad = [
                    vertexNormals[xIndex  ][yIndex  ],
                    vertexNormals[xIndex+1][yIndex  ],
                    vertexNormals[xIndex  ][yIndex+1],
                    vertexNormals[xIndex+1][yIndex+1]
                ]
                vertexNormalData += [
                    nQuad[0],
                    nQuad[1],
                    nQuad[3],
                    nQuad[0],
                    nQuad[3],
                    nQuad[2]
                ]

                fnQuad0 = calcNormal(quadPosition[0], quadPosition[1], quadPosition[3])
                fnQuad1 = calcNormal(quadPosition[0], quadPosition[3], quadPosition[2])

                faceNormalData += [
                    fnQuad0,
                    fnQuad0,
                    fnQuad0,
                    fnQuad1,
                    fnQuad1,
                    fnQuad1
                ]

        # Add attributes
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)
        self.addAttribute("vec3", "vertexNormal", vertexNormalData)
        self.addAttribute("vec3", "faceNormal", faceNormalData)
        self.countVertices()