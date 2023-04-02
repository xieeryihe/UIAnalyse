import time

from selenium.webdriver.common.by import By

from diff.devices import Devices
from diff import config, uidiff


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

    # 两两对比
    for i in range(len(device_list) - 1):
        uidiff.Diff(device_list[i].driver, device_list[i + 1].driver).diff()

    devices.stop_drivers()

    uidiff.end()


if __name__ == '__main__':
    start_time = time.time()

    app_test(config.soundrecorder_info)

    end_time = time.time()

    run_time = end_time - start_time
    print("运行时长: {:.2f} 秒。".format(run_time))
