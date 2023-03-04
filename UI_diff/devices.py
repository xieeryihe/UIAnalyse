import os
import re
import cv2
from selenium.webdriver.common.by import By
from appium import webdriver
from config import trivia_info
from server import *
import io
import numpy as np
from PIL import Image


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

        # 设备可用时状态为 "device"，还有 offline 状态
        :return: devices的list[dict...]
        """

        device_list = []
        devices_info = os.popen('adb devices').read()
        devices = re.findall(r'(.*?)\tdevice\b', devices_info)  # 查看所有设备
        for temp_device_name in devices:
            temp_command = "adb -s {} shell getprop ro.build.version.release".format(temp_device_name)
            temp_version = os.popen(temp_command).read().strip()  # 删除空白内容
            temp_dict = {  # 设备名和版本组成字典
                "deviceName": temp_device_name,
                "platformVersion": temp_version
            }
            device_list.append(temp_dict)

        # print(device_list)
        return device_list

    def start(self, app_info):
        """
        相当于初始化设备并连接到服务器，打开对应的应用
        :param app_info:待启动的app信息，一般形式为：
        dict{
            "packageName": "xxx",
            "activityName": "xxx"
        }

        :return:
        """
        appium_server = AppiumServer()
        servers = appium_server.start_servers(server_num=self.device_num)
        for (device_info, server_info) in zip(self.devices_dict, servers):
            platform_version = device_info["platformVersion"]
            device_name = device_info["deviceName"]
            host = server_info["host"]
            port = server_info["port"]
            caps = get_caps(platform_version, device_name, app_info)

            driver = webdriver.Remote("http://{}:{}/wd/hub".format(host, port), caps)

            driver.implicitly_wait(5)
            device = Device(platform_version, device_name, driver)
            self.devices.append(device)
        # root = driver.find_element(By.XPATH, "/hierarchy/*")

    def stop(self):
        """
        停用所有device的driver
        :return:
        """
        for device in self.devices:
            device.driver.quit()

        print("-------------------stop-----------------")

    def test(self):
        self.start(trivia_info)
        self.stop()

    def test_single(self):
        driver = self.devices[0].driver
        root = driver.find_element(By.XPATH, "/hierarchy/*")
        print(root)
        img = root.find_element(By.ID, "titleImage").screenshot_as_png
        print(img)

    def compare_test(self):
        """
        对比测试
        :return:
        """
        driver0 = self.devices[0].driver
        driver1 = self.devices[1].driver
        img0_byte = driver0.find_element(By.ID, "titleImage").screenshot_as_png
        img1_byte = driver1.find_element(By.ID, "titleImage").screenshot_as_png
        img0 = byte2image(img0_byte)
        img1 = byte2image(img1_byte)
        print(img0.size)
        print(img1.size)

        img0_cv = byte2cv(img0_byte)
        img1_cv = byte2cv(img1_byte)
        result = cv2.matchTemplate(img0_cv, img1_cv, cv2.TM_SQDIFF_NORMED)
        min_value, max_value, min_location, max_location = cv2.minMaxLoc(result)
        print(min_value, max_value)

        # TODO:将两个图片resize成一样的大的，然后调用cv库比对。


def temp():
    caps = {
        "platformName": "Android",
        "platformVersion": "9",
        "deviceName": "xxx",
        "appPackage": "com.example.android.navigation",
        "appActivity": ".MainActivity",
        "unicodeKeyboard": True,
        "resetKeyboard": True,
        "noReset": True,
        "newCommandTimeout": 6000,
        "automationName": "UiAutomator2"
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    driver.implicitly_wait(5)
    image_byte = driver.find_element(By.ID, "titleImage").screenshot_as_png
    byte2image(image_byte).save("./Image/a.png")  # 二进制图片转png
    src = byte2cv(image_byte)
    print(src)


def image2byte(image):
    """
    图片转byte
    image: 必须是PIL格式
    image_bytes: 二进制
    """
    # 创建一个字节流管道
    img_bytes = io.BytesIO()
    # 把PNG格式转换成的四通道转成RGB的三通道，然后再保存成jpg格式
    image = image.convert("RGB")
    # 将图片数据存入字节流管道， format可以按照具体文件的格式填写
    image.save(img_bytes, format="JPEG")
    # 从字节流管道中获取二进制
    image_bytes = img_bytes.getvalue()
    return image_bytes


def byte2image(byte_data):
    """
    byte转为图片
    byte_data: 二进制
    """
    image = Image.open(io.BytesIO(byte_data))
    return image


def byte2cv(im):
    """
    二进制图片转cv2
    :param im: 二进制图片数据，bytes
    :return: cv2图像，numpy.ndarray
    """
    return cv2.imdecode(np.array(bytearray(im), dtype='uint8'), cv2.IMREAD_UNCHANGED)  # 从二进制图片数据中读取
