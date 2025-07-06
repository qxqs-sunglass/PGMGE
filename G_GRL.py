"""读取文件的控制模块"""


class GGRLoader:
    def __init__(self, master=None):
        """游戏全局资源加载器（Game Global Resource Loader）
        作用：读取游戏资源文件，包括图片、场景、脚本等"""
        self.master = master  # main.py的实例化对象
        self.file_type = [
            "images", "scenes", "scripts"
        ]

    def init(self):
        pass

    def load_file(self, file_path):
        """读取文件"""


