from appium import webdriver
from selenium.webdriver.common.by import By

from config import *
from basic import *


def test():
    device_list = get_devices()
    temp_device = device_list[1]
    caps = get_caps(temp_device["platformVersion"], temp_device["deviceName"], trivia_packageName, trivia_activityName)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
    driver.implicitly_wait(5)
    root = driver.find_element(By.XPATH, "/hierarchy/*")
    DFS(root)
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


if __name__ == '__main__':
    test()
