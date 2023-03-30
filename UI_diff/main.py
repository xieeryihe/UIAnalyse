from diff.devices import *
from conf import config
if __name__ == '__main__':
    config.diff_log = open("./log/diff_log.txt", "w")
    config.diff_log.write("start\n")
    devices = Devices()

    # devices.start_drivers(config.trivia_info)
    devices.start_drivers(config.zhihu_info)

    devices.compare_two_page()
    # devices.test_single()
    # devices.compare_two_page()
    devices.stop_drivers()

    config.diff_log.close()

