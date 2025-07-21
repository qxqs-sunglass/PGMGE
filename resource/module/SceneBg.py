from . import sprite
import pygame


class SceneBg(sprite.Sprite):
    def __init__(self, image, pos=None, size=None):
        super().__init__(image, pos, size)
        # self.image = pygame.transform.scale(self.image, size)
        # self.rect = self.image.get_rect(center=pos)
