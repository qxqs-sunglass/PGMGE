from . import sprite
import pygame


class Actor(sprite.Sprite):
    def __init__(self, name, image, pos=None, size=None,
                 image_type='img'):
        super().__init__(name, image, pos, size, image_type)


