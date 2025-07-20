import pygame


class GGRRender:
    def __init__(self, master=None):
        """游戏渲染器"""
        self.master = master  # main.py的实例化对象
        self.ID = "G_GRRender"  # 渲染器ID
        self.sprites_data = None  # 存放当前场景所有精灵的数据
        self.scene = None  # 当前场景

    def init(self):
        pass

    def loading(self):
        """游戏加载"""
        pass

    def init_scene(self):
        """初始化游戏场景"""
        pass

    def update(self):
        """更新游戏渲染器"""
        pass
        """for sprite in self.sprites_data:
            sprite.draw()"""

    def charge_scene(self, scene_name):
        """更换游戏场景"""
        self.sprites_data = self.master.call_G_GRA("data_scenes").get(scene_name, None)
        self.scene = scene_name
