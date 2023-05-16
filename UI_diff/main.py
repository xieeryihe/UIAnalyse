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

    device_list = devices.start_drivers(info, implicitly_time=0.1)
    uidiff.diff_all(device_list)

    devices.stop_drivers()
    uidiff.end()


def start_time_cal():
    time1 = time.time()

    uidiff.init()
    devices = Devices()
    devices.start_drivers(config.trivia_info)

    time2 = time.time()

    devices.stop_drivers()
    uidiff.end()

    time3 = time.time()
    print(time2 - time1)
    print(time3 - time2)


if __name__ == '__main__':
    start_time = time.time()

    app_test(config.soundrecorder_info)
    # start_time_cal()

    end_time = time.time()

    run_time = end_time - start_time
    print("总运行时长: {:.2f} 秒。".format(run_time))
