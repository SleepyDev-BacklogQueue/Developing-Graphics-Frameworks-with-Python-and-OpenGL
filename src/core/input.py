import pygame

class Input(object):
    def __init__(self):
        # Application quit
        self.quit = False

        # Track keypress
        self.keyDown_l    = []
        self.keyUp_l      = []
        self.keyPressed_l = []

    def update(self):
        # Reset discrete keypress events
        self.keyDown_l = []
        self.keyUp_l   = []

        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                self.quit = True
            
            # Keyboard event
            if event.type == pygame.KEYDOWN:
                keyName = pygame.key.name(event.key)
                self.keyDown_l += [keyName]
                self.keyPressed_l += [keyName]
            if event.type == pygame.KEYUP:
                keyName = pygame.key.name(event.key)
                self.keyUp_l += [keyName]
                self.keyPressed_l.remove(keyName)
    
    # Check key states
    def isKeyDown(self, keyCode):
        return keyCode in self.keyDown_l
    def isKeyUp(self, keyCode):
        return keyCode in self.keyUp_l
    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressed_l