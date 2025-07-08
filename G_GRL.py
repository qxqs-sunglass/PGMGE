"""读取文件的控制模块"""
from config.BaseConfig import __default_path__
import os
import json
import pygame
import logs


class GGRLoader:
    def __init__(self, master=None):
        """游戏全局资源加载器（Game Global Resource Loader）
        作用：读取游戏资源文件，包括图片、场景、脚本等"""
        self.master = master  # main.py的实例化对象
        self.ID = "G_GRLoader"  # 全局游戏资源加载器标识符
        self.file_path = __default_path__  # 默认资源路径
        self.file_type = [
            "image", "scene", "script"
        ]
        # 文件类型列表
        # 图片：images
        self.Suffix_images = [
            ".png", ".jpg", ".jpeg", ".gif", ".bmp"
        ]
        # 场景&脚本：scenes&scripts
        self.Suffix_scenes_scripts = [
            ".json"
        ]
        # 以下为私有变量
        self.save_path_dict = {
            "image": self.save_path_image,
            "scene_script": self.save_path_scene_script,
            "unknown": self.save_path_scene_script
        }  # 映射字典
        self.file_content_paths = []    # 目录下所有文件路径
        self.data_images = {}   # 图片资源
        self.data_scenes = {}   # 场景资源
        self.data_scripts = {}  # 脚本资源
        self.data_unknown = {}  # 未知资源

    def init(self):
        """初始化"""
        self.dfs_path(self.file_path)
        print("文件数量：", len(self.file_content_paths))
        print(self.data_images)
        print(self.data_scenes)
        print(self.data_scripts)
        print(self.data_unknown)

    def load_file(self, file_path):
        """读取文件，用于动态加载资源"""

    def dfs_path(self, path):
        """深度优先遍历目录"""
        for file in os.listdir(path):  # 遍历目录
            file_path = os.path.join(path, file)  # 文件路径
            if os.path.isdir(file_path):  # 目录
                self.dfs_path(file_path)
                continue
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
        elif suffix in self.Suffix_scenes_scripts:
            return "scene_script"
        else:
            return "unknown"

    def save_path_image(self, path):
        """保存图片路径"""
        data = pygame.image.load(path)
        self.data_images[os.path.basename(path)] = data
        print("加载图片：", os.path.basename(path))

    def save_path_scene_script(self, path):
        """保存场景或脚本路径"""
        if os.path.splitext(path)[1] != ".json":
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()
        if data.get("type") == "scene":
            self.data_scenes[os.path.basename(path)] = data
        elif data.get("type") == "script":
            self.data_scripts[os.path.basename(path)] = data
        else:
            self.data_unknown[os.path.basename(path)] = data
        print("加载场景或脚本：", os.path.basename(path))


if __name__ == '__main__':
    loader = GGRLoader()
    loader.init()
    print(loader.file_content_paths)


