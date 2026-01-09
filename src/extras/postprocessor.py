from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.renderTarget import RenderTarget
from geometry.geometry import Geometry

class Postprocessor(object):
    def __init__(self, renderer, scene, camera, finalRenderTarget=None):
        self.renderer = renderer
        self.sceneList = [scene]
        self.cameraList = [camera]
        self.renderTargetList = [finalRenderTarget]
        self.finalRenderTarget = finalRenderTarget
        self.orthoCamera = Camera()
        self.orthoCamera.setOrthographic()

        self.rectangleGeo = Geometry()
        P = [
            [-1,-1],
            [ 1,-1],
            [-1, 1],
            [ 1, 1]
        ]
        T = [
            [0,0],
            [1,0],
            [0,1],
            [1,1]
        ]
        positionData = [
            P[0], P[1], P[3],
            P[0], P[3], P[2],
        ]
        uvData = [
            T[0], T[1], T[3],
            T[0], T[3], T[2],
        ]
        self.rectangleGeo.addAttribute("vec2", "vertexPosition", positionData)
        self.rectangleGeo.addAttribute("vec2", "vertexUV", uvData)
        self.rectangleGeo.countVertices()

    def addEffect(self, effect):
        postScene = Scene()
        resolution = self.renderer.windowSize
        target = RenderTarget(resolution)
        self.renderTargetList[-1] = target
        
        effect.uniforms["texture"].data[0] = target.texture.textureRef

        mesh = Mesh(self.rectangleGeo, effect)
        postScene.add(mesh)
        self.sceneList += [postScene]
        self.cameraList += [self.orthoCamera]
        self.renderTargetList+= [self.finalRenderTarget]

    def render(self):
        passes = len(self.sceneList)
        for n in range(passes):
            scene = self.sceneList[n]
            camera = self.cameraList[n]
            target = self.renderTargetList[n]
            self.renderer.render(scene, camera, renderTarget=target)