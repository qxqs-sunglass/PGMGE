from logs import write_log
import pygame


class GGRRender:
    def __init__(self, master=None):
        """游戏渲染器"""
        self.master = master  # main.py的实例化对象
        self.ID = "G_GRRender"  # 渲染器ID
        self.sprites_data = []  # 存放当前场景所有精灵的数据
        self.scene_name = "默认"  # 当前场景
        self.scene_data = {}

    def init(self):
        """游戏渲染器初始化"""
        write_log("G_GRRender初始化", self.ID)

    def loading(self, name="None"):
        """游戏加载"""
        if name == "None":
            self.scene_data = self.master.call_G_GRA("data_scenes", self.ID).get(self.scene_name, {})
            write_log("加载场景{}数据".format(self.scene_name), self.ID)
        else:
            self.scene_name = name
            self.scene_data = self.master.call_G_GRA("data_scenes", self.ID).get(name, {})
            write_log("加载场景{}数据".format(name), self.ID)
        # ————————————————————————————————————————————————
        sprites_data = self.master.call_G_GRA("data_sprites", self.ID)
        print(self.scene_data)
        print(sprites_data)
        if "sprites" in self.scene_data.keys():
            for n in self.scene_data["sprites"]:  # 遍历场景中所有精灵
                if n not in sprites_data.keys():  # 若精灵数据不存在，则跳过
                    continue
                self.sprites_data.append(sprites_data.get(n, None))
        print(self.sprites_data)

    def update(self):
        """更新游戏渲染器"""
        for sprite in self.sprites_data:
            sprite.draw(self.master.screen)

    def charge_scene(self, scene_name):
        """更换游戏场景"""
        self.loading(scene_name)
        write_log("更换场景为{}".format(scene_name), self.ID)
