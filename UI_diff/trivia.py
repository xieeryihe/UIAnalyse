from appium import webdriver
from devices import *
from config import *
from server import AppiumServer


def test():
    devices = Devices.get_devices()
    device_num = len(devices)
    appium_server = AppiumServer()
    appium_server.start_servers(server_num=device_num)

    print(len(devices))
    print(devices)
    device = devices[0]
    caps = get_caps(device["platformVersion"], device["deviceName"], trivia_info)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    driver.implicitly_wait(5)

    # for device in devices:
    #     caps = get_caps(device["platformVersion"], device["deviceName"],
    #                     trivia_packageName, trivia_activityName)
    #     driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    #     driver.implicitly_wait(5)

    root = driver.find_element(By.XPATH, "/hierarchy/*")

    # DFS(root)

    print("-------------------")

    es1 = root.find_element(By.ID, "titleConstraint")
    print(es1.id)
    print(es1.text)
    es2 = es1.find_elements(By.XPATH, "./child::*/*")
    print(len(es2))
    for ele in es2:
        if ele.text != "":
            print(ele.text)

    driver.quit()


def test1():
    devices = Devices()
    devices.test()


if __name__ == '__main__':
    test1()
