from config.BaseConfig import __default_path__
from logs import write_log
import os
import json
import pygame


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
        }  # 映射表
        self.file_path = __default_path__  # 默认资源路径
        self.file_type = [
            "image", "scene", "script"
        ]
        # 文件类型列表
        # 图片：images
        self.Suffix_images = [
            ".png", ".jpg", ".jpeg", ".gif", ".bmp"
        ]
        # 以下为私有变量
        self.save_path_dict = {
            "image": self.save_path_image,
            "json": self.save_path_json,
        }  # 映射字典
        self.file_content_paths = []  # 目录下所有文件路径
        self.data_game = {
            "images": {},
            "scenes": {},
            "scripts": {},
            "unknown": {}
        }  # 游戏数据

    def init(self):
        """初始化游戏全局资源分配器"""
        write_log("初始化游戏全局资源分配器", self.ID, msg_type="info")

    def load_file(self, file_path, import_way="str"):
        """读取文件，用于动态加载资源，注：此处使用绝对路径
        :param file_path: 文件路径
        :param import_way: 导入方式，str或list，默认为str"""
        if import_way == "str":
            self.load(file_path)
        elif import_way == "list":
            for file in file_path:
                self.load(file)
        else:
            write_log("导入方式错误！", self.ID, msg_type="error")
        print(self.file_content_paths)

    def load(self, file_path):
        if not os.path.exists(file_path):  # 文件不存在
            write_log("文件不存在："+file_path, self.ID, msg_type="error")
            return
        self.file_content_paths.append(file_path)  # 添加文件路径到列表
        # 保存路径到字典
        file_type = self.judge_file_type(file_path)  # 判断文件类型
        if file_type in self.save_path_dict.keys():  # 类型存在于字典中
            self.save_path_dict[file_type](file_path)  # 保存路径到字典

    def judge_file_type(self, file_path):
        """判断文件类型"""
        suffix = os.path.splitext(file_path)[1]  # 文件后缀
        if suffix in self.Suffix_images:
            return "image"
        elif suffix == ".json":
            return "json"

    def dfs_path(self, path):
        """深度优先遍历目录"""
        for file in os.listdir(path):  # 遍历目录
            file_path = os.path.join(path, file)  # 文件路径
            if os.path.basename(file_path) in ["__pycache__", "config.json"]:  # 排除缓存文件
                continue
            if os.path.isdir(file_path):  # 目录
                self.dfs_path(file_path)
                continue
            if file_path in self.file_content_paths:  # 已存在
                continue
            self.file_content_paths.append(file_path)  # 添加文件路径到列表
            # 保存路径到字典
            print(file_path)
            file_type = self.judge_file_type(file_path)  # 判断文件类型
            if file_type in self.save_path_dict.keys():  # 类型存在于字典中
                self.save_path_dict[file_type](file_path)  # 保存路径到字典
            # ————————————————————
            if self.master.first_load:
                self.master.update()  # 更新主窗口

    def loading(self):
        """加载游戏全局资源"""
        # 加载游戏素体数据
        self.dfs_path(self.file_path)
        write_log("\n-------------------------\n初始化成功！", self.ID, msg_type="info")
        write_log("文件数量："+str(len(self.file_content_paths)), self.ID)
        write_log("文件类型："+str(len(self.file_type)), self.ID)
        for key, value in self.data_game.items():
            write_log(key+": "+str(len(value)), self.ID)
            write_log(str(value), self.ID)
        # ——————————————————————————————————————————————————————————
        for tag in ["images", "sounds", "music", "scripts"]:
            self.data_map[tag].update(self.data_game.get(tag, {}))  # 获取游戏素体数据
        self.loading_sprites()  # 加载角色

    def loading_sprites(self):
        """构建角色"""
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
                self.master.update()  # 更新主窗口

    def get_scene_data(self, name):
        """获取场景数据"""
        return self.data_scenes.get(name)

    def save_path_image(self, path):
        """保存图片路径"""
        data = pygame.image.load(path)
        self.data_game["images"][os.path.basename(path)] = data
        # print("加载图片：", os.path.basename(path))
        write_log("加载图片："+os.path.basename(path), self.ID)

    def save_path_json(self, path):
        """保存场景或脚本路径"""
        if os.path.splitext(path)[1] != ".json":
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()
        gtype = data.get("type")  # 获取类型
        name = os.path.basename(path)  # 获取文件名
        if gtype == "scene":  # 场景
            self.data_game["scenes"][name] = data
        elif gtype == "script":  # 脚本
            self.data_game["scripts"][name] = data
        elif gtype in self.file_type:  # 未知类型
            if gtype not in self.data_game.keys():  # 类型不存在
                self.data_game[gtype] = {name: data}
            else:
                self.data_game[gtype][name] = data
        else:  # 未知类型
            self.data_game["unknown"][name] = data
        # print("加载.json文件：", os.path.basename(path))
        write_log("加载.json文件："+os.path.basename(path), self.ID)

