import os
from selenium.webdriver.common.by import By


def get_devices():
    """
    获取devices字典列表，
    dict{
        "deviceName":"xxx",
        "platformVersion":""
    }
    :return: devices的list[dict...]
    """
    device_list = []
    text = os.popen("adb devices").read()
    lines = text.split('\n')
    # 获取的文本至少有三行，第一行是"List of devices attached"，然后是设备列表，最后两行是空白行
    if len(lines) < 3:
        print("error")
    device_lines = lines[1:len(lines) - 2]
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


def get_caps(platformVersion, deviceName, packageName, activityName):
    caps = {
        "platformName": "Android",
        "platformVersion": platformVersion,  # 安卓版本
        "deviceName": deviceName,  # 设备名（主要针对IOS），安卓手机可以随意填写
        "appPackage": packageName,  # APP Package名称
        "appActivity": activityName,  # 启动Activity名称
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
