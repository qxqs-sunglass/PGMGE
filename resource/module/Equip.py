from . import sprite


class Equip(sprite.Sprite):
    def __init__(self, name, image, pos=(0, 0), size=(1, 1)):
        """装备类"""
        super().__init__(name, image, pos, size)
        self.type = 'equip'
