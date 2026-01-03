#!/usr/bin/env python3

from core.base import Base

class Test(Base):
    def initialise(self):
        print("Initialising program...")
    
    def update(self):
        # Typical usage
        if self.input.isKeyDown("space"):
            print("Space key was pressed down")
        if self.input.isKeyPressed("right"):
            print("Right key is currently pressed")


# Launch application
Test().run()