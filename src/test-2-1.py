#!/usr/bin/env python3

from core.base import Base

class Test(Base):
    def initialise(self):
        print("Initialising program...")

    def update(self):
        pass

# Launch application
Test().run()