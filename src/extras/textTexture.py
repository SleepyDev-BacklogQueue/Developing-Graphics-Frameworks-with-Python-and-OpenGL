from core.texture import Texture
import pygame

class TextTexture(Texture):
    def __init__(self,
        text="Hello, world!",
        systemFontName="Arial",
        fontFileName=None,
        fontSize=24,
        fontColor=[0,0,0],
        backgroundColor=[255,255,255],
        transparent=False,
        imageWidth=None, imageHeight=None,
        alignHorizontal=0.0,
        alignVertical=0.0,
        imageBorderWidth=0,
        imageBorderColor=[0,0,0]):
        super().__init__()

        # Default font
        font = pygame.font.SysFont(systemFontName, fontSize)
        fontSurface = font.render(text, True, fontColor)

        # Texture surface
        (textWidth, textHeight) = font.size(text)
        if imageWidth is None:
            imageWidth = textWidth
        if imageHeight is None:
            imageHeight = textHeight
        self.surface = pygame.Surface((imageWidth, imageHeight), pygame.SRCALPHA)

        if not transparent:
            self.surface.fill(backgroundColor)
        cornerPoint = (alignHorizontal*(imageWidth - textWidth), alignVertical*(imageHeight - textHeight))
        destinationRectangle = fontSurface.get_rect(topleft=cornerPoint)

        # Add border
        if imageBorderWidth > 0:
            pygame.draw.rect(self.surface, imageBorderColor,[0,0,imageWidth,imageHeight], imageBorderWidth)
        
        self.surface.blit(fontSurface, destinationRectangle)

        self.uploadData()