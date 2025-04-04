import pygame

class Sprites:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colorkey):
        image = pygame.Surface((width, height)).convert()
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
        image.set_colorkey(colorkey)
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image
