import pygame


class GGRControl:
    def __init__(self, master=None):
        """游戏全局控制器(GGRC)"""
        self.master = master  # main.py的实例化对象

    def init(self):
        pass

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 系统默认的退出事件
                self.master.running = False
                break
