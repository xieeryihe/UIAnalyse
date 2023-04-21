import time

from diff import config, uidiff
from diff.devices import Devices

test_device_list = [
    {
        "deviceName": "emulator-5554",
        "platformVersion": "9"
    },
    {
        "deviceName": "emulator-5556",
        "platformVersion": "9"
    },
]


def app_test(info):
    uidiff.init()

    devices = Devices()

    device_list = devices.start_drivers(info)

    uidiff.diff_all(device_list)

    devices.stop_drivers()

    uidiff.end()


def single_test():
    devices = Devices()
    devices.start_drivers(config.soundrecorder_info)
    # devices.temp_test()
    devices.stop_drivers()
    uidiff.end()


if __name__ == '__main__':
    start_time = time.time()

    app_test(config.todolist_info)

    end_time = time.time()

    run_time = end_time - start_time
    print("总运行时长: {:.2f} 秒。".format(run_time))
