__author__ = '@bilibili__秋天会有下雪天'  # 作者
__version__ = '0.1.1'  # 版本号
__date__ = '2025-07-5'  # 创建日期
__default_path__ = 'resource\\'  # 默认资源路径
__default_scene__ = 'title'   # 默认场景名称
__default_script__ = 'title'  # 默认脚本名称
__FPS__ = 60  # 帧率
__G_GR_ID__ = {
    "Main": "LogsTemp/Main.log",
    "G_GRControl": "LogsTemp/G_GRControl.log",
    "G_GRRender": "LogsTemp/G_GRRender.log",
    "G_GRAllocator": "LogsTemp/G_GRAllocator.log",
    "call_msg": "LogsTemp/call_msg.log",
}  # 全局资源ID
__msg_types__ = [
    "info",  # 信息
    "Info",
    "warning",  # 警告
    "Warning",
    "error",  # 错误
    "Error",
    "debug",  # 调试
    "Debug",
    "none",  # 无
    "None"
]
__custom_tags__ = [
    "custom_sprite_type",  # 自定义精灵类型标签，注：需要在resource/module中创建相应的模块
    "custom_scene_type",  # 自定义场景类型标签
    "custom_script_type",  # 自定义脚本类型标签，注：需要在resource/module中创建相应的脚本模块
    "first_load"  # 初始导入标签:一般用于打开加载界面
]  # 系统规范的自定义标签
__warning_msg__ = [
    "00001"  # 警告信息
]
collider_types = [
    "check_mouse",  # 鼠标碰撞器
    "check_keyboard",  # 键盘碰撞器
]




