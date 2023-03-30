import os

from appium import webdriver

from diff.comparison import *
from diff.image import *
from diff.server import *


def get_caps(platformVersion, deviceName, app_info):
    caps = {
        "platformName": "Android",
        "deviceName": deviceName,  # 设备名（用于区分设备）
        "platformVersion": platformVersion,  # 安卓版本
        "appPackage": app_info["packageName"],  # APP Package名称
        "appActivity": app_info["activityName"],  # 启动Activity名称
        "unicodeKeyboard": True,  # 使用自带输入法，True时可以输入unicode字符
        "resetKeyboard": True,  # 执行完程序恢复原来输入法
        "noReset": True,  # 不要重置App（否则每次打开程序都像刚安装一样）
        "newCommandTimeout": 6000,  # 自动化操作的超时时间
        "automationName": "UiAutomator2"
    }
    return caps


class Device:
    """
    设备类
    """
    platformVersion = ""
    deviceName = ""
    SAP = None
    driver = None

    def __init__(self, platformVersion="", deviceName="", SAP=None, driver=None):
        self.platformVersion = platformVersion
        self.deviceName = deviceName
        self.SAP = SAP
        self.driver = driver


class Devices:
    """
    用于UI_diff的类，可以封装多种函数
    目前只是先考虑针对一个APP
    """
    device_num = 0
    devices_dict = []  # device的字典列表
    devices = []  # Device类实例的列表

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

    def start_drivers(self, app_info):
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
        servers = appium_server.start_servers(server_num=self.device_num, devices_dict=self.devices_dict)
        for (device_info, server_info) in zip(self.devices_dict, servers):
            platform_version = device_info["platformVersion"]
            device_name = device_info["deviceName"]
            host = server_info["host"]
            port = server_info["port"]
            caps = get_caps(platform_version, device_name, app_info)
            driver = webdriver.Remote("http://{}:{}/wd/hub".format(host, port), caps)

            driver.implicitly_wait(5)
            device = Device(platform_version, device_name, server_info, driver)
            self.devices.append(device)
        # root = driver.find_element(By.XPATH, "/hierarchy/*")

    def stop_drivers(self):
        """
        停用所有device的driver，目前的缺点是没办法关掉停止driver后的cmd窗口
        """
        for device in self.devices:
            device.driver.quit()
            cmd = "netstat -aon | findstr \"{}:{}\"".format(device.SAP["host"], device.SAP["port"])
            info_list = os.popen(cmd).read().strip().split('\n')
            for info in info_list:
                temp = info.split()
                pid = int(temp[4])
                if pid > 0:
                    temp_cmd = "taskkill /pid {} -f".format(pid)
                    os.popen(temp_cmd)
                    # print("execute " + temp_cmd)
            # print(device.SAP)

        print("-------------------stop_drivers-----------------")

    def test_single(self):
        driver = self.devices[0].driver
        root = driver.find_element(By.XPATH, "/hierarchy/*")  # 得到顶层元素
        print(root)
        img = root.find_element(By.ID, "titleImage").screenshot_as_png

    def compare_test(self):
        """
        对比测试
        :return:
        """
        driver1 = self.devices[0].driver
        driver2 = self.devices[1].driver

        c = Comparison(driver1, driver2)
        node1 = driver1.find_element(By.ID, "titleImage")
        node2 = driver2.find_element(By.ID, "titleImage")
        # ssim_value = c.image_compare(node1, node2)
        # print("ssim_value is :{:.3f}".format(ssim_value))
        c.position_compare(node1, node2)

    def compare_two_page(self):
        driver1 = self.devices[0].driver
        driver2 = self.devices[1].driver
        c = Comparison(driver1, driver2)
        c.dfs()


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
    print("-----------")
    print(driver.caps)
    image_byte = driver.find_element(By.ID, "titleImage").screenshot_as_png
    byte2image(image_byte).save("./res/Image/0.png")  # 二进制图片转png
    src = byte2cv(image_byte)
    # print(src)
