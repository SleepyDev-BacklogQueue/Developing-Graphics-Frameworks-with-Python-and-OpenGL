import pygame

class Input(object):
    def __init__(self):
        # Application quit
        self.quit = False

    def update(self):
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                self.quit = True