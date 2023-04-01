from diff.devices import *
from conf import config
import os


def init():
    # 删除上一次log的所有图片
    dir_path = "./log/img/"
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            os.remove(file_path)

    # 打开log文件
    config.diff_log = open("./log/diff_log.txt", "w")
    config.diff_log.write("start\n")


def end():
    # 结束操作
    config.diff_log.close()


def app_test(info):
    devices = Devices()
    devices.start_drivers(info)
    # devices.compare_two_page()
    # devices.compare_test()
    devices.test_single()
    devices.stop_drivers()


if __name__ == '__main__':
    init()

    app_test(config.bilibili_info)

    end()
