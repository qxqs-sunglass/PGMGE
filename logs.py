"""用于处理全局日志"""
from config.BaseConfig import __G_GR_ID__
import os


def write_log(log_str, G_ID):
    """写入日志:
    :param log_str: 日志内容
    :param G_ID: 所属系统模块的的日志ID"""
    if not os.path.exists(__G_GR_ID__[G_ID]):
        os.mkdir(__G_GR_ID__[G_ID].rsplit('/', 1)[0])

    with open(__G_GR_ID__[G_ID], 'a', encoding='utf-8') as f:
        f.write(log_str + '\n')   # 写入日志内容
        f.flush()   # 刷新缓冲区



