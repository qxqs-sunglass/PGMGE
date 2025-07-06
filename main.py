"""游戏引擎主程序"""
from G_GRL import GGRLoader
from G_GRA import GGALoader
import sys
import pygame
import json


class Main:
    def __init__(self):
        pygame.init()
        self.G_GRL = GGRLoader()  # 加载游戏资源
        self.G_GRA = GGALoader()  # 合成、分配游戏场景
        self.data = {}
        with open("resource/config.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
            f.close()
        self.screen = None
        self.read_path = {}
        self.init()

    def init(self):
        """初始化游戏"""
        self.screen = pygame.display.set_mode((self.data["width"], self.data["height"]))
        pygame.display.set_caption(self.data["title"])
        self.read_path = self.data["read_path"]
        self.G_GRL.load_file(self.read_path)

    def run(self):
        while True:
            self.draw()
            self.event()
            pygame.display.flip()

    def draw(self):
        while True:
            pass

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == '__main__':
    app = Main()
    app.run()


