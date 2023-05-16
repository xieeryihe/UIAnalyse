import time

from appium import webdriver
import threading


# 设备一
def run_01():
    desired = {
        "platformName": "Android",
        "platformVersion": "9",
        "deviceName": "emulator-5554",
        "appPackage": "com.example.android.navigation",
        "appActivity": ".MainActivity",
        "unicodeKeyboard": True,
        "resetKeyboard": True,
        "noReset": True,
        "newCommandTimeout": 6000,
        "automationName": "UiAutomator2"
    }
    driver_01 = webdriver.Remote(command_executor="http://127.0.0.1:4723/wd/hub", desired_capabilities=desired)
    # driver(driver_01)


# 设备二
def run_02():
    desired = {
        "platformName": "Android",
        "platformVersion": "9",
        "deviceName": "emulator-5556",
        "appPackage": "com.example.android.navigation",
        "appActivity": ".MainActivity",
        "unicodeKeyboard": True,
        "resetKeyboard": True,
        "noReset": True,
        "newCommandTimeout": 6000,
        "automationName": "UiAutomator2"
    }
    driver_02 = webdriver.Remote(command_executor="http://127.0.0.1:4725/wd/hub", desired_capabilities=desired)


def driver(drivers):  # 元素操作方法
    time.sleep(5)
    drivers.quit()


if __name__ == '__main__':
    threading.Thread(target=run_01).start()
    threading.Thread(target=run_02).start()
