import pygame


class Actor:
    def __init__(self, image, pos=None, size=None,
                 image_type='img'):
        """标准的sprite类，游戏实例素体的基类。
        :param image: 素材图片
        :param pos: 素材位置
        :param size: 素材大小
        :param image_type: 素材类型，默认为'img'('str'为字符串路径)"""
        self.image = image  # 素材图片
        self.rect = pygame.Rect(pos, size) if pos and size else image.get_rect()  # 素材位置和大小
        self.image_type = image_type  # 素材类型，默认为'img'('str'为字符串路径)
        self.dirty = 2  # 0: 不需要更新，1：需要更新，2：需要重绘

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, *args):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.image!r}, {self.rect!r})>"

