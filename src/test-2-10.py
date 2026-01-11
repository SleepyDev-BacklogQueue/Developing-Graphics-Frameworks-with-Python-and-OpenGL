#!/usr/bin/env python3

from core.base import Base

class Test(Base):
    def initialise(self):
        print("Initialising program...")
    
    def update(self):
        # Debug printing
        # if len(self.input.keyDown_l) > 0:
        #     print(f"Keys down: {self.input.keyDown_l}")
        # if len(self.input.keyPressed_l) > 0:
        #     print(f"Keys pressed: {self.input.keyPressed_l}")
        # if len(self.input.keyUp_l) > 0:
        #     print(f"Keys down: {self.input.keyUp_l}")

        # Typical usage
        if self.input.isKeyDown("space"):
            print("Space key was pressed down")
        if self.input.isKeyPressed("right"):
            print("Right key is currently pressed")

# Launch application
Test().run()