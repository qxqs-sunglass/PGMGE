"""读取文件的控制模块"""
from config.BaseConfig import __default_path__
from logs import write_log
import os
import json
import pygame


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
        # 以下为私有变量
        self.save_path_dict = {
            "image": self.save_path_image,
            "json": self.save_path_json,
        }  # 映射字典
        self.file_content_paths = []    # 目录下所有文件路径
        self.data_game = {
            "images": {},
            "scenes": {},
            "scripts": {},
            "unknown": {}
        }  # 游戏数据

    def init(self):
        """初始化"""
        self.dfs_path(self.file_path)
        write_log("\n-------------------------\n初始化成功！", self.ID, msg_type="info")
        write_log("文件数量："+str(len(self.file_content_paths)), self.ID)
        write_log("文件类型："+str(len(self.file_type)), self.ID)
        for key, value in self.data_game.items():
            write_log(key+": "+str(len(value)), self.ID)
            write_log(str(value), self.ID)

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

    def dfs_path(self, path):
        """深度优先遍历目录"""
        for file in os.listdir(path):  # 遍历目录
            file_path = os.path.join(path, file)  # 文件路径
            if os.path.basename(file_path) == "__pycache__" or os.path.basename(file_path) == "config.json":  # 排除缓存文件
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

    def judge_file_type(self, file_path):
        """判断文件类型"""
        suffix = os.path.splitext(file_path)[1]  # 文件后缀
        if suffix in self.Suffix_images:
            return "image"
        elif suffix == ".json":
            return "json"

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
            if gtype not in self.data_game.keys():
                self.data_game[gtype] = {name: data}
            else:
                self.data_game[gtype][name] = data
        else:
            self.data_game["unknown"][name] = data
        # print("加载.json文件：", os.path.basename(path))
        write_log("加载.json文件："+os.path.basename(path), self.ID)


if __name__ == '__main__':
    loader = GGRLoader()
    loader.init()


