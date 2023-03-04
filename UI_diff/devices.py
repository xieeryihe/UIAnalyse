import os
from selenium.webdriver.common.by import By
from appium import webdriver
from config import trivia_info
from server import *


def get_caps(platformVersion, deviceName, app_info):
    caps = {
        "platformName": "Android",
        "platformVersion": platformVersion,  # 安卓版本
        "deviceName": deviceName,  # 设备名（主要针对IOS），安卓手机可以随意填写
        "appPackage": app_info["packageName"],  # APP Package名称
        "appActivity": app_info["activityName"],  # 启动Activity名称
        "unicodeKeyboard": True,  # 使用自带输入法，True时可以输入unicode字符
        "resetKeyboard": True,  # 执行完程序恢复原来输入法
        "noReset": True,  # 不要重置App（否则每次打开程序都像刚安装一样）
        "newCommandTimeout": 6000,  # 自动化操作的超时时间
        "automationName": "UiAutomator2"
    }
    return caps


def DFS(element):
    print("in: " + element.get_attribute("class"))
    if element.text != "":
        print(element.text)
    elements = element.find_elements(By.XPATH, "child::*/*")
    for e in elements:
        DFS(e)


class Device:
    """
    设备类
    """
    platformVersion = ""
    deviceName = ""
    driver = None

    def __init__(self, platformVersion="", deviceName="", driver=None):
        self.platformVersion = platformVersion
        self.deviceName = deviceName
        self.driver = driver


class Devices:
    """
    用于UI_diff的类，可以封装多种函数
    目前只是先考虑对比一个APP
    """
    device_num = 0
    devices_dict = []  # device的字典列表
    devices = []  # Device类实例的列表

    # apps = []  # 待检测app的列表，好像不需要app列表，因为要检测的内容由device中的driver决定

    def __init__(self):
        self.devices_dict = self.get_devices()
        self.device_num = len(self.devices_dict)
        print(self.device_num)
        print(self.devices_dict)
        pass

    @staticmethod
    def get_devices():
        """
        获取devices字典列表，
        dict{
            "deviceName":"xxx",
            "platformVersion":""
        }
        一个可能的格式如下：
        C:\\Users\\xieeryihe>adb devices
        * daemon not running; starting now at tcp:5037
        * daemon started successfully
        List of devices attached
        emulator-5554   device
        emulator-5556   device

        :return: devices的list[dict...]
        """

        device_list = []
        text = os.popen("adb devices").read()
        lines = text.split('\n')
        # 获取的文本至少有三行，第一行是"List of devices attached"，然后是设备列表，最后两行是空白行
        if len(lines) < 3:
            print("error")
        # print(lines)
        line_offset = 1
        for line in lines:
            # print(line)
            if line and line[0] == "*":  # 在避免空串的情况下跳过开头带 * 的行
                line_offset += 1

        device_lines = lines[line_offset:len(lines) - 2]
        for device_line in device_lines:
            # print(device_line)
            temp_info = device_line.split()
            if temp_info[1] == "device":  # 设备可用时状态为 "device"，还有 offline 状态
                temp_device_name = temp_info[0]
                temp_command = "adb -s {} shell getprop ro.build.version.release".format(temp_device_name)
                temp_version = os.popen(temp_command).read().strip()  # 删除空白内容
                temp_dict = {
                    "deviceName": temp_device_name,
                    "platformVersion": temp_version
                }
                device_list.append(temp_dict)

        # print(device_list)
        return device_list

    def start(self, app_info):
        appium_server = AppiumServer()
        servers = appium_server.start_servers(server_num=self.device_num)
        for (device_info, server_info) in zip(self.devices_dict, servers):
            platform_version = device_info["platformVersion"]
            device_name = device_info["deviceName"]
            host = server_info["host"]
            port = server_info["port"]
            caps = get_caps(platform_version, device_name, app_info)

            driver = webdriver.Remote("http://{}:{}/wd/hub".format(host, port), caps)  # here

            driver.implicitly_wait(5)
            device = Device(platform_version, device_name, driver)
            self.devices.append(device)
        # root = driver.find_element(By.XPATH, "/hierarchy/*")

    def end(self):
        """
        停用所有driver
        :return:
        """
        for device in self.devices:
            device.driver.quit()

        print("-------------------end-----------------")

    def test(self):
        self.start(trivia_info)
        self.end()
