from core.input import Input

import pygame
import sys

class Base(object):
    def __init__(self, screenSize=[512, 512]):
        # Initialise pygame
        pygame.init()

        # Specify OpenGL context
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

        # Create window
        displayFlags = pygame.DOUBLEBUF | pygame.OPENGL
        self.screen = pygame.display.set_mode(screenSize, displayFlags)
        pygame.display.set_caption("Graphics Window")

        # Application attributes
        self.running = True
        self.clock = pygame.time.Clock()
        self.time = 0
        self.input = Input()

    def initialise(self):
        pass

    def update(self):
        pass

    def run(self):
        # Startup
        self.initialise()

        # Mainloop
        while self.running:
            # Process input
            self.input.update()
            if self.input.quit:
                self.running = False

            # Update
            self.deltaTime = self.clock.get_time() / 1000
            self.time += self.deltaTime
            self.update()

            # Render
            pygame.display.flip()

            # Pause for fixed FPS
            self.clock.tick(60)

        ## Shutdown ##
        pygame.quit()
        sys.exit()