# 对比模块
import os
import re
import threading

from diff.image import *
from skimage.metrics import structural_similarity
from selenium.webdriver.common.by import By
from diff.config import *
from diff import config


def init():
    """
    初始化
    """
    # 判断路径是否存在
    dir_path = "./img/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # 删除上一次log的所有图片
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            os.remove(file_path)

    # 打开log文件
    config.diff_log = open("./log/diff_log.txt", "w")
    config.diff_log.write("start\n")


def end():
    """
    后续操作
    """
    config.diff_log.close()


def get_bounds(node):
    """bounds字符串转换为数字数组"""
    bounds = node.get_attribute("bounds")  # bounds字符串
    pattern = r'\d+'
    str_list = re.findall(pattern, bounds)
    return list(map(int, str_list))


class Diff:
    driver1 = None
    driver2 = None
    root1 = None
    root2 = None
    list1 = None
    list2 = None

    # 软检测白名单
    white_list = {
        "class": [
            "RecyclerView",
            "HorizontalScrollView"
        ],
        "resource-id": [
            "input",
            "search"
        ]
    }

    def __init__(self, driver1, driver2):
        self.driver1 = driver1
        self.driver2 = driver2

    def in_white_list(self, target, check_type):
        for t in self.white_list[check_type]:
            if t in target:
                return True
        return False

    def mismatch(self, node1, node2, rec_color=(0, 0, 255), img_path="./img"):
        """
        失配时，保存图片，颜色为BGR
        """
        # print("---mismatch---")
        # print(node1.get_attribute("resource-id"))
        img1_byte = self.driver1.get_screenshot_as_png()  # driver取出的图片是四通道的
        img2_byte = self.driver2.get_screenshot_as_png()
        img1_cv = byte2cv(img1_byte)
        img2_cv = byte2cv(img2_byte)

        # 如果是四通道的，转为三通道
        if img1_cv.shape[2] == 4:
            img1_cv = cv2.cvtColor(img1_cv, cv2.COLOR_BGRA2BGR)
        if img2_cv.shape[2] == 4:
            img2_cv = cv2.cvtColor(img2_cv, cv2.COLOR_BGRA2BGR)

        bounds1 = get_bounds(node1)
        upper_left1 = (bounds1[0], bounds1[1])
        lower_right1 = (bounds1[2], bounds1[3])

        bounds2 = get_bounds(node2)
        upper_left2 = (bounds2[0], bounds2[1])
        lower_right2 = (bounds2[2], bounds2[3])

        # 圈出不匹配的位置
        cv2.rectangle(img1_cv, upper_left1, lower_right1, rec_color, 3)  # 颜色是BGR
        cv2.rectangle(img2_cv, upper_left2, lower_right2, rec_color, 3)

        # 拼接出错的图像便于对比
        diff_img = hconcat_images(img1_cv, img2_cv)

        # cv2.imshow('Image', diff_img)
        # cv2.waitKey(0)
        # print("save img")

        cv2.imwrite("{}/{}.png".format(img_path, config.mis_no), diff_img)
        config.mis_no += 1

    def position_compare(self, node1, node2):
        """
        位置对比，包括1.元素占整个屏幕长宽的百分比和2.元素中点占屏幕位置的百分比
        bounds属性一般形式为：bounds="[16,373][704,757]"，为字符串类型，分别为左上，右下坐标
        """

        # 提取bounds属性中的数字并转换为整型
        node1_bounds = get_bounds(node1)
        node2_bounds = get_bounds(node2)
        root1_bounds = get_bounds(self.root1)
        root2_bounds = get_bounds(self.root2)

        width1 = root1_bounds[2] - root1_bounds[0]  # 宽度
        width2 = root2_bounds[2] - root2_bounds[0]
        height1 = root1_bounds[3] - root1_bounds[1]  # 高度
        height2 = root2_bounds[3] - root2_bounds[1]

        node1_center_x = int(node1_bounds[0] + width1 / 2)  # 元素中点的横坐标
        node1_center_y = int(node1_bounds[1] + height1 / 2)  # 元素中点的纵坐标
        node1_center_prop_x = node1_center_x / width1  # 元素中点在x方向占屏幕位置比例
        node1_center_prop_y = node1_center_y / height1  # 元素中点在y方向占屏幕位置比例

        node2_center_x = int(node2_bounds[0] + width2 / 2)
        node2_center_y = int(node2_bounds[1] + height2 / 2)
        node2_center_prop_x = node2_center_x / width2
        node2_center_prop_y = node2_center_y / height2

        # 中点差异的比例（比例范围0~1）
        center_diff_x = node2_center_prop_x - node1_center_prop_x
        center_diff_y = node2_center_prop_y - node1_center_prop_y

        node1_width_prop = node1_bounds[2] / width1
        node1_height_prop = node1_bounds[3] / height1
        node2_width_prop = node2_bounds[2] / width2
        node2_height_prop = node2_bounds[3] / height2

        # 长宽差异比例
        width_diff = node2_width_prop - node1_width_prop
        height_diff = node2_height_prop - node1_height_prop

        result = [x < position_threshold for x in
                  [center_diff_x, center_diff_y, width_diff, height_diff]]
        if not all(result):  # 如果但凡有一个超过阈值，就有问题
            print("position mismatch")
            config.diff_log.write("{} : position mismatch.\n".format(config.mis_no))
            self.mismatch(node1, node2)
            return RET_MISMATCH

        return RET_OK

    @staticmethod
    def image_compare(node1, node2):
        """
        图片对比
        """
        image1_byte = node1.screenshot_as_png
        image2_byte = node2.screenshot_as_png
        image1_cv = byte2cv(image1_byte)
        image2_cv = byte2cv(image2_byte)
        gray_image1 = cv2.cvtColor(image1_cv, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(image2_cv, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.resize(gray_image2, (gray_image1.shape[1], gray_image1.shape[0]))
        # structural_similarity 的两个图片必须是相同size
        ssim_value = structural_similarity(gray_image1, gray_image2)
        # 打印SSIM值
        # print("The SSIM value is", ssim_value)
        return ssim_value

    def image_node(self, node1, node2, strict_mode=1):
        """
        图像节点对比
        """
        if strict_mode:
            ssim_value = self.image_compare(node1, node2)
            if ssim_value < SSIM_threshold:
                print("img mismatch" + str(ssim_value))
                config.diff_log.write("{} : image mismatch.\n".format(config.mis_no))
                self.mismatch(node1, node2)
                return RET_MISMATCH
        return self.position_compare(node1, node2)

    def text_node(self, node1, node2, strict_mode=1):
        """
        文本节点对比（TextView）
        """
        if strict_mode:
            text1 = node1.get_attribute("text")
            text2 = node2.get_attribute("text")
            if text1 != text2:
                print("text mismatch: text1 is \"{}\", text2 is \"{}\".".format(text1, text2))
                config.diff_log.write("{} : text mismatch.\n".format(config.mis_no))
                self.mismatch(node1, node2)
                return RET_MISMATCH
        return self.position_compare(node1, node2)

    def compare(self, node1, node2):
        """
        对比两个节点的总函数
        """
        class1 = node1.get_attribute("class")
        class2 = node2.get_attribute("class")
        id1 = node1.get_attribute("resource-id")
        id2 = node2.get_attribute("resource-id")

        strict_mode = 1

        # 跳过白名单
        if self.in_white_list(class1, "class"):
            # print("skip class")
            return RET_SKIP
        if id1 and self.in_white_list(id1, "resource-id"):
            # print("skip id")
            return RET_SKIP

        # 类名检测
        if class1 != class2:
            # 类都不一致，用蓝色圈出来
            print("class1: " + class1 + "  class2: " + class2)
            print("id1: " + id1 + "  id2: " + id2)
            config.diff_log.write("{} : class mismatch.\n".format(config.mis_no))
            self.mismatch(node1, node2, rec_color=(255, 0, 0))  # BGR
            return RET_MISMATCH

        # 图片检测
        if "ImageView" in class1:
            if self.image_node(node1, node2, strict_mode) < 0:
                return RET_MISMATCH

        # 文本检测
        if "TextView" in class1:
            if self.text_node(node1, node2, strict_mode) < 0:
                return RET_MISMATCH
        return RET_OK

    @staticmethod
    def find_all_child(node, node_list):
        elements = node.find_elements(By.XPATH, "child::*/*")
        elements.reverse()
        for e in elements:
            node_list.append(e)

    def diff(self):
        self.root1 = self.driver1.find_element(By.XPATH, "/hierarchy/*")
        self.root2 = self.driver2.find_element(By.XPATH, "/hierarchy/*")
        self.list1 = [self.root1]
        self.list2 = [self.root2]

        # print(type(self.driver1))
        # print(type(self.root1))

        while self.list1 and self.list2:
            node1 = self.list1.pop()
            node2 = self.list2.pop()
            # print(node1.get_attribute("resource-id"))
            # print(node2.get_attribute("resource-id"))
            # compare
            if self.compare(node1, node2) < 0:
                # 如果当前节点有问题，就不用push子节点了，继续就行
                continue
            else:
                # 如果检测没问题（那么都是一样的，取其中一个log即可）
                id1 = node1.get_attribute("resource-id")
                config.diff_log.write(str(id1) + " compare OK...\n")

            # 经过测试，查找子元素耗时较长，下面代码用于多线程获取子元素

            t1 = threading.Thread(target=self.find_all_child, args=(node1, self.list1,))
            t2 = threading.Thread(target=self.find_all_child, args=(node2, self.list2,))

            t1.start()
            t2.start()

            t1.join()
            t2.join()

            # 单线程
            # elements1 = node1.find_elements(By.XPATH, "child::*/*")
            # elements2 = node2.find_elements(By.XPATH, "child::*/*")

            # for e1 in elements1:
            #     self.list1.append(e1)
            # for e2 in elements2:
            #     self.list2.append(e2)
