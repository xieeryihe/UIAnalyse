from appium import webdriver
from selenium.common import NoSuchElementException

import diff.image
from diff.server import *
from diff.uidiff import *


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
    SAP中的元素为字典，一般格式如下：
    {
        "host": self.host,
        "port": temp_port,
    }
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
    设备管理核心类
    """
    device_num = 0
    devices_dict = []  # device的字典列表
    devices = []  # Device类实例的列表
    threads = []  # 多线程启动

    def __init__(self):
        self.devices_dict = self.get_devices()
        self.device_num = len(self.devices_dict)
        # print(self.device_num)
        # print(self.devices_dict)
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
        # 该步骤速度很快，就不用多线程了
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

    @staticmethod
    def preprocessing(driver):
        """
        预处理开屏广告、青少年协议、登录
        """
        # 跳过广告
        try:
            # # 青少年协议
            # action_bar_root = driver.find_element(By.ID, "action_bar_root")
            # if action_bar_root:
            #     driver.press_keycode(4)  # 按一下返回键

            # 广告
            ad = driver.find_element(By.ID, "btn_skip")
            if ad:
                ad.click()

            # 登录
            login = driver.find_element(By.ID, "dialog_container")
            if login:
                close = driver.find_element(By.ID, "close")
                if close:
                    driver.press_keycode(4)  # 按一下返回键

        except NoSuchElementException:
            # print("NoSuchElementException")
            pass

    def start_drivers(self, app_info, device_dict=None, if_background=False):
        """
        初始化设备并连接到服务器，打开对应的应用
        :param if_background: 是否在后台运行，默认不在后台运行
        :param device_dict: 要启动的设备列表，一般形式为：
        dict{
            "deviceName": "emulator-5554",
            "platformVersion": "9"
        }
        :param app_info:待启动的app信息，一般形式为：
        dict{
            "packageName": "xxx",
            "activityName": "xxx"
        }
        :return:Device实例列表
        """
        # 启动server
        appium_server = AppiumServer()
        # 可自定义设备列表检测，也可以用默认的（系统检测到的所有设备）
        if device_dict:
            target_num = len(device_dict)
            target_devices = device_dict
        else:
            target_num = self.device_num
            target_devices = self.devices_dict
        servers = appium_server.start_servers(
            server_num=target_num, devices_dict=target_devices, if_background=if_background)
        # 连接devices
        for (device_info, server_info) in zip(self.devices_dict, servers):
            t = threading.Thread(target=self.start_driver, args=(device_info, server_info, app_info))
            self.threads.append(t)
            t.start()
        for t in self.threads:
            t.join()
        return self.devices

    def start_driver(self, device_info, server_info, app_info):
        platform_version = device_info["platformVersion"]
        device_name = device_info["deviceName"]
        host = server_info["host"]
        port = server_info["port"]
        caps = get_caps(platform_version, device_name, app_info)
        driver = webdriver.Remote("http://{}:{}/wd/hub".format(host, port), caps)
        driver.implicitly_wait(5)
        device = Device(platform_version, device_name, server_info, driver)
        self.devices.append(device)

        # 进行一些预处理
        self.preprocessing(driver)

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

    def temp_test(self):
        driver1 = self.devices[0].driver
        # driver2 = self.devices[1].driver
        # d = Diff(driver1, driver2)
        # d.diff()
        # text_node = driver1.find_element(By.ID, "recording_status_text")
        # text = text_node.get_attribute("text")
        # text_pic = text_node.screenshot_as_png
        # print(text)
        # print(text_pic)
        # pic_cv2 = diff.image.byte2cv(text_pic)
        # # cv2.imshow('1', pic_cv2)
        # cv2.imwrite('image.png', pic_cv2)

        # textColor = text_node.get_attribute("contentSize")
        # print(textColor)
        root = driver1.find_element(By.XPATH, "/hierarchy/*")
        img_png = root.screenshot_as_png
        img_cv2 = byte2cv(img_png)
        cv2.imshow("image", img_cv2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
