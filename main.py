"""游戏引擎主程序"""
from config.BaseConfig import __custom_tags__, __FPS__, __default_path__
from logs import init_log, write_log
from G_GRA import GGRAllocator
from G_GRR import GGRRender
from G_GRC import GGRControl
from importlib import import_module
import pygame
import json


class Main:
    def __init__(self):
        pygame.init()
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
        self.custom_data = {}
        # 自定义标签字典:{'sprite':{"name": class, "name": class},'scene':{...},'script':{...}}
        self.init()

    def init(self):
        """初始化游戏"""
        init_log()   # 初始化日志模块
        self.init_game()  # 初始化游戏
        self.init_module()  # 初始化游戏模块
        self.search_deal_tag()  # 搜索并处理自定义标签
        if not self.first_load:
            self.call_charge_scene(self.data.get("scene", "00001"))  # 加载场景
        write_log("\n-------------------------\n游戏初始化成功！", self.ID, msg_type="info")

    def init_game(self):
        """初始化游戏"""
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )  # 设置屏幕大小
        pygame.display.set_caption(self.data.get("title", "游戏标题"))  # 设置窗口标题
        self.clock = pygame.time.Clock()  # 时钟
        self.fps = self.data.get("fps", __FPS__)  # 帧率
        self.G_GRA.file_path = self.data.get("file_path", __default_path__)  # 资源文件路径

    def init_module(self):
        """初始化游戏模块"""
        self.G_GRA.init()
        # self.sprites_data
        self.G_GRC.init()
        self.G_GRR.init()

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.G_GRR.update()
            self.G_GRC.update()
            pygame.display.flip()  # 刷新屏幕

    def update(self):
        """更新游戏"""
        self.G_GRR.update()
        self.G_GRC.update()
        pygame.display.flip()  # 刷新屏幕

    def search_deal_tag(self):
        """搜索并处理自定义标签
        注：deal_tag_list中存放自定义标签名称，deal_tag_map中存放对应的处理方法
        通过映射表处理标签数据"""
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
        name = "sprites"
        self.G_GRA.file_type.extend(data)  # 扩展文件类型列表
        self.custom_data[name] = {}  # 保存自定义数据
        for e in data:
            module_path = f"resource.module.{e}"
            data2 = {}
            try:
                temp = import_module(module_path)
                data2[e] = temp.__dict__[e]  # 保存自定义数据
                self.custom_data[name].update(data2)  # 保存自定义数据
                write_log(f"加载成功: <{e}: {data2[e]}>", self.ID)
            except ModuleNotFoundError as err:
                # 明确提示缺失的模块名
                write_log(f"加载失败: {e} (原因: {err})", self.ID, "warning")
            except KeyError as err:
                # 明确提示缺失的类名
                write_log(f"加载失败: {e} (原因: {err})", self.ID, "warning")
        write_log(f"{self.custom_data[name]}", self.ID)

    def deal_tag__custom_scene_type(self, data):
        """自定义场景标签处理"""
        self.G_GRA.file_type.extend(data)  # 扩展文件类型列表
        self.custom_data["scene"] = data  # 保存自定义数据
        write_log(data, self.ID)

    def deal_tag__custom_script_type(self, data):
        """自定义脚本标签处理"""
        self.G_GRA.file_type.extend(data)  # 扩展文件类型列表
        self.custom_data["script"] = data  # 保存自定义数据
        write_log(data, self.ID)

    def deal_tag__first_load(self, data):
        """处理首次启动标签"""
        # print(data["path"])
        # print(data["scene"])
        if "path" in data:
            path = data.get("path", "")
            self.G_GRA.load_file(path, "list")  # 加载资源文件
        self.call_charge_scene(data.get("scene", "00001"))  # 加载场景
        self.first_load = True  # 标记为初始加载

    def call_G_GRA(self, name, G_ID):
        """调用G_GRA模块"""
        write_log(f"【{G_ID}】调用G_GRA模块: 【{name}】", "call_msg")
        return getattr(self.G_GRA, name)  # 调用G_GRA模块

    def call_G_GRR(self, name, G_ID):
        """调用G_GRR模块"""
        write_log(f"【{G_ID}】调用G_GRR模块: 【{name}】", "call_msg")
        return getattr(self.G_GRR, name)  # 调用G_GRR模块

    def call_G_GRC(self, name, G_ID):
        """调用G_GRC模块"""
        write_log(f"【{G_ID}】调用G_GRC模块: 【{name}】", "call_msg")
        return getattr(self.G_GRC, name)  # 调用G_GRC模块

    def call_charge_scene(self, scene_name):
        """调用场景切换"""
        self.scene_name = scene_name  # 保存场景名称
        self.G_GRR.charge_scene(scene_name)  # 切换场景
        self.G_GRC.charge_scene(scene_name)  # 切换场景


if __name__ == '__main__':
    app = Main()
    app.run()


