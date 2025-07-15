import main


class GGRAllocator:
    def __init__(self, master=None):
        """游戏全局资源分配器（Game Global Resource Allocator）
        作用：分配、合成游戏全局资源，如：角色、物品、场景等。"""
        self.master: main.Main = master  # main.py的实例化对象
        self.ID = "G_GRAllocator"  # 全局资源分配器ID
        self.data_game = {}  # 基础游戏数据素体
        self.data_images = {}  # 图片数据
        self.data_sounds = {}  # 音效数据
        self.data_music = {}  # 音乐数据
        self.data_scenes = {}  # 场景数据
        self.data_scripts = {}  # 脚本数据
        self.data_map = {
            "images": self.data_images,
            "scenes": self.data_scenes,
            "sounds": self.data_sounds,
            "music": self.data_music
        }
        self.tag_map = {
            "sprite": self.init_sprite,
            "scene": self.init_scene,
            "script": self.init_script,
        }

    def init(self):
        """初始化游戏全局资源分配器"""
        self.data_game = self.master.call_G_GRL('data_game')  # 获取基础游戏数据素体
        for key, value in self.data_game.items():
            if key in self.data_map:
                self.data_map[key] = value  # 基础游戏数据素体赋值到对应数据字典
        print(self.data_game)
        for k, v in self.master.custom_data.items():
            self.tag_map[k](v, in_type="list")  # 处理自定义标签

    def init_sprite(self, value, in_type="str"):
        """初始化角色资源"""
        if in_type not in ["str", "list"]:
            in_type = "str"

        if in_type == "str":
            print(value)
        elif in_type == "list":
            for item in value:
                print(item)

    def init_scene(self, name, in_type="str"):
        """初始化场景资源"""
        if in_type not in ["str", "list"]:
            in_type = "str"

        if in_type == "str":
            pass
        elif in_type == "list":
            pass

    def init_script(self, name, in_type="str"):
        """初始化脚本资源"""
        if in_type not in ["str", "list"]:
            in_type = "str"

        if in_type == "str":
            pass
        elif in_type == "list":
            pass

    def get_scene_data(self, name):
        """获取场景数据"""
        return self.data_scenes.get(name)


