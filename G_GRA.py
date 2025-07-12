class GGRAllocator:
    def __init__(self, master=None):
        """游戏全局资源分配器（Game Global Resource Allocator）
        作用：分配、合成游戏全局资源，如：角色、物品、场景等。"""
        self.master = master  # main.py的实例化对象
        self.ID = "G_GRAllocator"  # 全局资源分配器ID
        self.game_data = {
            "sprites": {},  # 存放实例数据
            "scenes": {}  # 存放场景数据
        }  # 存放游戏全局资源数据

    def init(self):
        pass
