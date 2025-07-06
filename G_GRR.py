import pygame


class GGRRender:
    def __init__(self, master=None):
        """游戏渲染器"""
        self.master = master  # main.py的实例化对象
        self.sprites_data = None  # 存放所有精灵的数据

    def init(self):
        self.sprites_data = self.master.sprites_data  # 精灵数据

    def update(self):
        for sprite in self.sprites_data:
            sprite.draw()
