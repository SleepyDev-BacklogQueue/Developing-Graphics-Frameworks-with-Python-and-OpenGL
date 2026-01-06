from core.object3D import Object3D
from math import pi

class MovementRig(Object3D):
    def __init__(self, unitsPerSecond=1, degreesPerSecond=60):
        super().__init__()

        self.lookAttachment = Object3D()
        self.lookAttachment.parent = self
        self.children = [self.lookAttachment]

        self.unitsPerSecond = unitsPerSecond
        self.degreesPerSecond = degreesPerSecond

        # Default keymap
        self.KEY_MOVE_FORWARDS  = "w"
        self.KEY_MOVE_BACKWARDS = "s"
        self.KEY_MOVE_LEFT      = "a"
        self.KEY_MOVE_RIGHT     = "d"
        self.KEY_MOVE_UP        = "r"
        self.KEY_MOVE_DOWN      = "f"
        self.KEY_TURN_LEFT      = "q"
        self.KEY_TURN_RIGHT     = "e"
        self.KEY_LOOK_UP        = "t"
        self.KEY_LOOK_DOWN      = "g"

    def add(self, child):
        self.lookAttachment.add(child)
    
    def remove(self, child):
        self.lookAttachment.remove(child)

    def update(self, inputObject, deltaTime):
        moveAmount = self.unitsPerSecond * deltaTime
        rotateAmount = self.degreesPerSecond * pi / 180 * deltaTime

        if inputObject.isKeyPressed(self.KEY_MOVE_FORWARDS):
            self.translate(0, 0, -moveAmount)
        if inputObject.isKeyPressed(self.KEY_MOVE_BACKWARDS):
            self.translate(0, 0, moveAmount)
        if inputObject.isKeyPressed(self.KEY_MOVE_LEFT):
            self.translate(-moveAmount, 0, 0)
        if inputObject.isKeyPressed(self.KEY_MOVE_RIGHT):
            self.translate(moveAmount, 0, 0)
        if inputObject.isKeyPressed(self.KEY_MOVE_UP):
            self.translate(0, moveAmount, 0)
        if inputObject.isKeyPressed(self.KEY_MOVE_DOWN):
            self.translate(0, -moveAmount, 0)

        if inputObject.isKeyPressed(self.KEY_TURN_RIGHT):
            self.rotateY(-moveAmount)
        if inputObject.isKeyPressed(self.KEY_TURN_LEFT):
            self.rotateY(moveAmount)

        if inputObject.isKeyPressed(self.KEY_LOOK_UP):
            self.lookAttachment.rotateX(rotateAmount)
        if inputObject.isKeyPressed(self.KEY_LOOK_DOWN):
            self.lookAttachment.rotateX(-rotateAmount)