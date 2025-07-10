"""游戏引擎主程序"""
from config.BaseConfig import __custom_tags__, __FPS__
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
        self.G_GRL = GGRLoader()  # 加载游戏资源
        self.G_GRA = GGRAllocator()  # 合成、分配游戏场景
        self.G_GRR = GGRRender()  # 渲染游戏图像
        self.G_GRC = GGRControl()  # 处理游戏事件
        self.data = {}
        with open("resource/config.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
            f.close()
        self.screen = None
        self.clock = None  # 时钟
        self.fps = __FPS__  # 帧率
        self.custom_map = {
            "custom_sprite_type": self.custom_sprite_type
        }  # 自定义标签映射
        self.custom_tags = []  # 自定义标签列表
        self.read_path = {}
        # 变量数据
        self.ID = "Main"
        # 资源数据
        self.data_images = {}
        self.data_scenes = {}
        self.data_scripts = {}
        self.data_unknown = {}
        # 精灵数据
        self.data_sprites = {}
        self.init()

    def init(self):
        """初始化游戏"""
        init_log()   # 初始化日志模块
        self.screen = pygame.display.set_mode(
            (self.data.get("width", 800), self.data.get("height", 600))
        )  # 设置屏幕大小
        pygame.display.set_caption(self.data.get("title", "游戏标题"))  # 设置窗口标题
        self.clock = pygame.time.Clock()  # 时钟
        self.fps = self.data.get("fps", __FPS__)  # 帧率
        self.read_path = self.data["read_path"]  # 读取路径
        self.search_tag()
        if len(self.custom_tags) > 0:
            for tag in self.custom_tags:
                # print("处理自定义标签：", tag)
                write_log("处理自定义标签："+tag, self.ID)
                self.custom_map[tag](self.data[tag])  # 处理自定义标签
        self.G_GRL.init()
        self.G_GRA.init()
        # self.sprites_data
        self.G_GRC.init()
        self.G_GRR.init()

    def run(self):
        while True:
            self.clock.tick(self.fps)
            self.G_GRR.update()
            self.G_GRC.update()
            pygame.display.flip()

    def search_tag(self):
        """搜索自定义标签"""
        for tag in __custom_tags__:
            if tag in self.data:
                write_log("发现自定义标签："+tag, self.ID)
                # print(tag, self.data[tag])
                self.custom_tags.append(tag)

    def custom_sprite_type(self, tag_data):
        """自定义精灵标签处理:
        此处为G_GRL添加自定义后，其会自行对目标数据进行处理"""
        self.G_GRL.file_type.extend(tag_data)   # 扩展文件类型列表
        write_log(self.G_GRL.file_type, self.ID)
        # print(self.G_GRL.file_type)


if __name__ == '__main__':
    app = Main()
    # app.run()


