import pygame


class Sprite:
    def __init__(
            self,
            name: str,
            image: pygame.Surface,
            pos=(0, 0),
            size=(1, 1),
            image_type='img', *args, **kwargs
    ):
        """标准的sprite类，游戏实例素体的基类。
        :param name: str——素材名称
        :param image: pygame.Surface——素材图片
        :param pos: (x, y)——素材位置
        :param size: (w, h)——素材大小:(宽比例, 高比例)
        :param image_type: 素材类型，默认为'img'('str'为字符串路径)"""
        self.name = name  # 素材名称
        self.pos = pos  # 素材位置
        self.size = size  # 素材大小
        self.image = self.smoothscale_image(image, size)  # 素材图片
        self.rect = self.image.get_rect()  # 素材矩形
        self.rect.topleft = pos  # 素材矩形位置
        self.image_type = image_type  # 素材类型，默认为'img'('str'为字符串路径)
        self.dirty = 2  # 0: 不需要更新，1：需要更新，2：需要重绘

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, *args):
        pass

    def set_pos(self, pos):
        self.pos = pos
        self.rect.topleft = pos

    def set_size(self, size):
        self.size = size
        self.image = self.smoothscale_image(self.image, size)
        self.rect = self.image.get_rect()

    def set_image(self, image):
        self.image = self.smoothscale_image(image, self.size)
        self.rect = self.image.get_rect()

    def __repr__(self):
        """返回Sprite对象的字符串表示形式。"""
        return f"<{self.__class__.__name__}({self.image!r}, {self.rect!r})>"

    @staticmethod
    def smoothscale_image(image, size):
        w = image.get_width()
        h = image.get_height()
        w = w*size[0]
        h = h*size[1]
        return pygame.transform.smoothscale(image, (int(w), int(h)))
