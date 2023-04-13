import time

from selenium.webdriver.common.by import By

from diff.devices import Devices
from diff import config, uidiff

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

    # 测知乎用的
    # for device in device_list:
    #     eles = device.driver.find_elements(By.CLASS_NAME, "android.widget.TextView")
    #     for e in eles:
    #         if e.get_attribute("text") == "未登录":
    #             e.click()
    #             break
    # time.sleep(5)

    uidiff.diff_all(device_list)

    devices.stop_drivers()

    uidiff.end()


def single_test():
    devices = Devices()
    devices.start_drivers(config.soundrecorder_info)
    devices.temp_test()
    devices.stop_drivers()
    uidiff.end()


if __name__ == '__main__':
    start_time = time.time()

    app_test(config.soundrecorder_info)
    # single_test()

    end_time = time.time()

    run_time = end_time - start_time
    print("总运行时长: {:.2f} 秒。".format(run_time))
