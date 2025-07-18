"""游戏引擎主程序"""
from config.BaseConfig import __custom_tags__, __FPS__, __default_path__
from logs import init_log, write_log
from G_GRL import GGRLoader
from G_GRA import GGRAllocator
from G_GRR import GGRRender
from G_GRC import GGRControl
import pygame
import json


class Main:
    def __init__(self):
        pygame.init()
        self.G_GRL = GGRLoader(self)  # 加载游戏资源
        self.G_GRA = GGRAllocator(self)  # 合成、分配游戏场景
        self.G_GRR = GGRRender(self)  # 渲染游戏图像
        self.G_GRC = GGRControl(self)  # 处理游戏事件
        self.data = {}
        with open("resource/config.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
            f.close()
        # 系统数据
        self.screen = None
        self.clock = None  # 时钟
        self.fps = __FPS__  # 帧率
        self.running = True  # 游戏运行状态
        self.WIDTH = self.data.get("width", 800)  # 屏幕宽度
        self.HEIGHT = self.data.get("height", 600)  # 屏幕高度
        self.deal_tag_map = {
            "custom_sprite_type": self.deal_tag__custom_sprite_type,
            "custom_scene_type": self.deal_tag__custom_scene_type,
            "custom_script_type": self.deal_tag__custom_script_type,
            "first_load": self.deal_tag__first_load
        }  # 自定义标签处理映射
        self.deal_tag_list = []  # 处理标签列表
        self.read_path = {}
        # 变量数据
        self.ID = "Main"  # 主程序ID
        self.first_load = False  # 是否初始加载
        self.scene_name = ""  # 当前场景名称
        self.custom_data = {}  # 自定义标签字典:{'sprite':[],'scene':[],'script':[]}
        self.init()

    def init(self):
        """初始化游戏"""
        init_log()   # 初始化日志模块
        self.init_game()  # 初始化游戏
        self.init_module()  # 初始化游戏模块
        write_log("\n-------------------------\n游戏初始化成功！", self.ID, msg_type="info")

    def init_game(self):
        """初始化游戏"""
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )  # 设置屏幕大小
        pygame.display.set_caption(self.data.get("title", "游戏标题"))  # 设置窗口标题
        self.clock = pygame.time.Clock()  # 时钟
        self.fps = self.data.get("fps", __FPS__)  # 帧率
        self.G_GRL.file_path = self.data.get("file_path", __default_path__)  # 资源文件路径
        self.search_deal_tag()  # 搜索并处理自定义标签

    def init_module(self):
        """初始化游戏模块"""
        self.G_GRL.init()
        self.G_GRA.init()
        # self.sprites_data
        self.G_GRC.init()
        self.G_GRR.init()

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.G_GRR.update()
            self.G_GRC.update()
            pygame.display.flip()

    def search_deal_tag(self):
        """搜索并处理自定义标签"""
        # 搜索自定义标签
        # print(self.data)
        for tag in __custom_tags__:
            if tag in self.data:
                write_log("发现自定义标签："+tag, self.ID)
                self.deal_tag_list.append(tag)  # 添加对应的处理方法
        # 处理自定义标签
        if len(self.deal_tag_list) > 0:
            for e in self.deal_tag_list:
                self.deal_tag_map[e](self.data[e])  # 处理自定义标签

    def deal_tag__custom_sprite_type(self, data):
        """自定义精灵标签处理:
        此处为G_GRL添加自定义后，其会自行对目标数据进行处理"""
        self.G_GRL.file_type.extend(data)  # 扩展文件类型列表
        self.custom_data["sprite"] = data  # 保存自定义数据
        write_log(self.G_GRL.file_type, self.ID)

    def deal_tag__custom_scene_type(self, data):
        """自定义场景标签处理"""
        self.G_GRL.file_type.extend(data)  # 扩展文件类型列表
        self.custom_data["scene"] = data  # 保存自定义数据
        write_log(data, self.ID)

    def deal_tag__custom_script_type(self, data):
        """自定义脚本标签处理"""
        self.G_GRL.file_type.extend(data)  # 扩展文件类型列表
        self.custom_data["script"] = data  # 保存自定义数据
        write_log(data, self.ID)

    def deal_tag__first_load(self, data):
        """处理首次启动标签"""
        print(data["path"])
        print(data["scene"])
        self.first_load = True  # 标记为初始加载
        for path in data.get("path", ["00001"]):
            if path == "00001":
                write_log("弱警告：无路径", self.ID, msg_type="warning")
                break
            self.G_GRL.load_file(path)  # 加载资源文件
        for scene in data.get("scene", ["00001"]):
            if scene == "00001":
                write_log("弱警告：无场景", self.ID, msg_type="warning")
                break
            self.G_GRA.load_scene(data.get("name", "00001"))  # 加载场景
        self.call_charge_scene(data.get("name", "title"))  # 切换场景

    def call_G_GRL(self, name):
        """调用G_GRL模块"""
        return getattr(self.G_GRL, name)  # 调用G_GRL模块

    def call_G_GRA(self, name):
        """调用G_GRA模块"""
        return getattr(self.G_GRA, name)  # 调用G_GRA模块

    def call_G_GRR(self, name):
        """调用G_GRR模块"""
        return getattr(self.G_GRR, name)  # 调用G_GRR模块

    def call_G_GRC(self, name):
        """调用G_GRC模块"""
        return getattr(self.G_GRC, name)  # 调用G_GRC模块

    def call_charge_scene(self, scene_name):
        """调用场景切换"""
        self.scene_name = scene_name  # 保存场景名称
        self.G_GRR.charge_scene(scene_name)  # 切换场景
        self.G_GRC.charge_scene(scene_name)  # 切换场景


if __name__ == '__main__':
    app = Main()
    app.run()


