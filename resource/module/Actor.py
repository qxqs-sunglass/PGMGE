from . import sprite
import pygame


class Actor(sprite.Sprite):
    def __init__(self, image, pos=None, size=None,
                 image_type='img'):
        super().__init__(image, pos, size, image_type)
        self.image_type = image_type
        self.image = image
        self.rect = pygame.Rect(pos, size) if pos and size else image.get_rect()


