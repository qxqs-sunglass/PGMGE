"""用于处理全局日志"""
from config.BaseConfig import __G_GR_ID__
import os
import time


def init_log():
    """初始化日志"""
    for G_ID in __G_GR_ID__:
        if not os.path.exists(__G_GR_ID__[G_ID]):
            with open(__G_GR_ID__[G_ID], 'w', encoding='utf-8') as f:
                f.write('日志初始化\n')   # 写入日志初始化信息
                f.flush()   # 刷新缓冲区
        else:   # 日志文件已存在，清空文件内容
            with open(__G_GR_ID__[G_ID], 'r+', encoding='utf-8') as f:
                f.truncate()


def write_log(log_str, G_ID):
    """写入日志:
    :param log_str: 日志内容
    :param G_ID: 所属系统模块的的日志ID"""
    if type(log_str) is not str:
        log_str = str(log_str)

    time_str = time.thread_time()   # 获取当前运行时间
    with open(__G_GR_ID__[G_ID], 'a', encoding='utf-8') as f:
        f.write(log_str + '\t\t\t\t' + str(time_str) + '\n')   # 写入日志内容
        f.flush()   # 刷新缓冲区



