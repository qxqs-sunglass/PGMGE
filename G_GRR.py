import pygame


class GGRRender:
    def __init__(self, master=None):
        """游戏渲染器"""
        self.master = master  # main.py的实例化对象
        self.ID = "G_GRRender"  # 渲染器ID
        self.sprites_data = None  # 存放所有精灵的数据

    def init(self):
        pass

    def update(self):
        """更新游戏渲染器"""
        pass
        """for sprite in self.sprites_data:
            sprite.draw()"""
