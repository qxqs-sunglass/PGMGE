from . import sprite


class But(sprite.Sprite):
    def __init__(self, name, image, pos, size):
        super().__init__(name, image, pos, size)
        self.type = 'but'
