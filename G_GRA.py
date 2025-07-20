from logs import write_log
from config.BaseConfig import __warning_msg__


class GGRAllocator:
    def __init__(self, master=None):
        """游戏全局资源分配器（Game Global Resource Allocator）
        作用：分配、合成游戏全局资源，如：角色、物品、场景等。"""
        self.master = master  # main.py的实例化对象
        self.ID = "G_GRAllocator"  # 全局资源分配器ID
        self.data_game = {}  # 基础游戏数据素体
        # 独立
        self.data_sprites = {}  # 角色数据
        self.data_images = {}  # 图片数据
        self.data_sounds = {}  # 音效数据
        self.data_music = {}  # 音乐数据
        self.data_scenes = {}  # 场景数据
        self.data_scripts = {}  # 脚本数据
        self.data_map = {
            "images": self.data_images,
            "scenes": self.data_scenes,
            "sounds": self.data_sounds,
            "music": self.data_music,
            "scripts": self.data_scripts,
            "sprites": self.data_sprites,
        }
        self.tag_map = [
            self.init_sprites,
            self.init_scene,
            self.init_script,
        ]

    def init(self):
        """初始化游戏全局资源分配器"""

    def loading(self):
        """加载游戏全局资源"""
        self.data_game = self.master.call_G_GRL('data_game')  # 获取基础游戏数据素体
        for tag in ["images", "sounds", "music", "scripts"]:
            self.data_map[tag].update(self.data_game.get(tag, {}))  # 获取游戏素体数据
        for tag in self.tag_map:
            tag()  # 初始化角色->场景->脚本资源

    def init_sprites(self):
        """初始化角色资源"""
        name = "sprite"
        custom_tags = self.master.custom_data.get(name, [])  # 获取自定义标签
        write_log(f"获取数据<{name}: {custom_tags}>", self.ID)
        data = {}
        data2 = {}  # 自定义标签数据：映射表
        for k, v in custom_tags.items():
            # 注：tag = {"...", class}
            data.update(self.data_game.get(k, {}))  # 合并角色数据
            data2.update({k: v})
        # 角色数据格式：data = {"name": data}
        # print(data)
        if not data:  # 跳过空数据
            write_log("警告：角色数据为空！", self.ID, "warning")
            return
        for k, v in data.items():  # 遍历角色数据
            if k in self.data_sprites:  # 跳过已存在的角色
                write_log(f"角色{k}已存在！", self.ID)
                continue
            if not v:  # 跳过空数据
                write_log(f"警告：角色{k}数据为空！", self.ID, "warning")
                continue
            # ————————————————————————————————————
            try:
                sp_type = v.get("type")  # 获取角色类型
                temp = data2.get(sp_type)(v.get("image"), v.get("pos"), v.get("size"))  # 创建角色对象
                self.data_sprites[name][k] = temp  # 保存角色数据
                write_log(f"角色{k}加载成功！", self.ID)
            except Exception as e:
                write_log(f"角色{k}加载失败！{e}", self.ID, "error")
            # ————END———
            if self.master.first_load:
                self.master.update()

    def init_scene(self):
        """初始化场景资源"""

    def init_script(self):
        """初始化脚本资源"""

    def load_scene(self, name):
        """加载场景"""
        if name in __warning_msg__:
            write_log("弱警告：无效场景！", self.ID, "warning")
            return
        self.master.call_G_GRL("data_game")
        self.master.call_charge_scene(name)

    def get_scene_data(self, name):
        """获取场景数据"""
        return self.data_scenes.get(name)

