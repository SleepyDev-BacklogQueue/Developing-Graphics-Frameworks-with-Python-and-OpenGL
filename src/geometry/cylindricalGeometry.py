from core.matrix import Matrix
from geometry.parametricGeometry import PolygonGeometry
from geometry.parametricGeometry import ParametricGeometry
from math import sin, cos, pi

class CylindricalGeometry(ParametricGeometry):
    def __init__(self, radiusTop=1, radiusBottom=1, height=1, radiusSegments=32, heightSegments=4, closedTop=True, closedBottom=True):
        def S(u, v):
            return [
                (v*radiusTop + (1-v)*radiusBottom) * sin(u),
                (v - 0.5) * height
                (v*radiusTop + (1-v)*radiusBottom) * cos(u),
            ]
        
        super().__init__(
            0, 2*pi, radiusSegments,
            0, 1, heightSegments,
            S
        )

        if closedTop:
            topGeometry = PolygonGeometry(radiusSegments, radiusTop)
            transform = Matrix.makeRotationX(-pi/2)
            transform = Matrix.makeRotationY(-pi/2) @ transform
            transform = Matrix.makeTranslation(0, height/2) @ transform
            topGeometry.applyMatrix(transform)
            self.merge(topGeometry)

        if closedBottom:
            bottomGeometry = PolygonGeometry(radiusSegments, radiusBottom)
            transform = Matrix.makeRotationX(pi/2)
            transform = Matrix.makeRotationY(-pi/2) @ transform
            transform = Matrix.makeTranslation(0, -height/2) @ transform
            bottomGeometry.applyMatrix(transform)
            self.merge(bottomGeometry)