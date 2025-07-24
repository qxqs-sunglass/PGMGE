from logs import write_log
import pygame


class GGRControl:
    def __init__(self, master=None):
        """游戏全局控制器(GGRC)"""
        self.master = master  # main.py的实例化对象
        self.ID = "G_GRControl"  # 全局控制器ID
        self.script_data = {}  # 脚本数据
        self.scene_name = ""  # 当前场景名称

    def init(self):
        """初始化"""
        write_log("初始化G_GRC", self.ID)

    def loading(self, name="None"):
        """游戏载入
        :param name: 场景名称(选填)"""
        if name == "None":
            self.script_data = self.master.call_G_GRA("data_scripts", self.ID).get(self.scene_name, {})
            write_log(f"载入{self.scene_name}场景数据", self.ID)
            return
        self.scene_name = name
        temp = self.master.call_G_GRA("data_scripts", self.ID)
        # print(temp)
        self.script_data = temp.get(self.scene_name, {})

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 系统默认的退出事件
                self.master.running = False
                break

    def charge_scene(self, scene_name):
        """载入场景"""
        self.loading(scene_name)
        write_log(f"载入场景{scene_name}", self.ID)
