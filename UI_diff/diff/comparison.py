# 对比模块
from diff.image import *
from skimage import measure
from selenium.webdriver.common.by import By


def simple_compare(ele1, ele2):
    if ele1.get_attribute("class") == ele2.get_attribute("class"):
        print(ele1.get_attribute("class") + " | basic class checked OK! ")


def image_compare(img1_byte, img2_byte):
    """
    两个图片对比的函数
    :param img1_byte:图片的二进制形式
    :param img2_byte:图片的二进制形式
    :return:
    """

    img1_cv = byte2cv(img1_byte)
    img2_cv = byte2cv(img2_byte)
    result = cv2.matchTemplate(img1_cv, img2_cv, cv2.TM_SQDIFF_NORMED)
    # min_value, max_value, min_location, max_location = cv2.minMaxLoc(result)
    return cv2.minMaxLoc(result)


def images_compare(image_byte_list):
    """
    图像列表的对比函数
    :param image_byte_list:图像列表
    :return:
    """
    pass


def image_compare_test(image1_byte, image2_byte):
    image1_cv = byte2cv(image1_byte)
    image2_cv = byte2cv(image2_byte)
    gray_image1 = cv2.cvtColor(image1_cv, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2_cv, cv2.COLOR_BGR2GRAY)

    ssim_value = measure.compare_ssim(gray_image1, gray_image2)

    # 打印SSIM值
    print("The SSIM value is", ssim_value)


def dfs_two_pages(root1, root2):
    """
    同时深搜两个页面结构树
    :param root2: <class 'appium.webdriver.webelement.WebElement'>
    :param root1: <class 'appium.webdriver.webelement.WebElement'>
    :return:
    """
    list1 = [root1]
    list2 = [root2]
    while list1 and list2:
        node1 = list1.pop()
        node2 = list2.pop()

        simple_compare(node1, node2)

        elements1 = node1.find_elements(By.XPATH, "child::*/*")
        elements2 = node2.find_elements(By.XPATH, "child::*/*")
        for e1 in elements1:
            list1.append(e1)
        for e2 in elements2:
            list2.append(e2)
