import pygame


class Sprite:
    def __init__(
            self,
            name: str = "None",
            image=None,
            pos=None,
            size=None,
            image_type='img', *args, **kwargs
    ):
        """标准的sprite类，游戏实例素体的基类。
        :param image: 素材图片
        :param pos: 素材位置
        :param size: 素材大小:(宽比例, 高比例)
        :param image_type: 素材类型，默认为'img'('str'为字符串路径)"""
        self.name = name  # 素材名称
        self.image = image  # 素材图片
        self.pos = pos  # 素材位置
        self.size = size  # 素材大小
        self.rect = self.image.get_rect()  # 素材矩形
        self.image_type = image_type  # 素材类型，默认为'img'('str'为字符串路径)
        self.dirty = 2  # 0: 不需要更新，1：需要更新，2：需要重绘

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, *args):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.image!r}, {self.rect!r})>"
