# 对比模块
import re

from conf import config
from diff.image import *
from skimage.metrics import structural_similarity
from selenium.webdriver.common.by import By


def get_bounds(node):
    """bounds字符串转换为数字数组"""
    bounds = node.get_attribute("bounds")  # bounds字符串
    pattern = r'\d+'
    str_list = re.findall(pattern, bounds)
    return list(map(int, str_list))


class Comparison:
    driver1 = None
    driver2 = None
    root1 = None
    root2 = None
    # 软检测白名单
    white_list = {
        "class": ["RecyclerView"]
    }

    def __init__(self, driver1, driver2):
        self.driver1 = driver1
        self.driver2 = driver2
        self.root1 = driver1.find_element(By.XPATH, "/hierarchy/*")  # 得到顶层元素
        self.root2 = driver2.find_element(By.XPATH, "/hierarchy/*")

    def mismatch(self, node1, node2, rec_color=(0, 0, 255)):
        # UI不匹配，将两张图片出错区域圈出来，并合并，保存
        img1_byte = self.root1.screenshot_as_png
        img2_byte = self.root2.screenshot_as_png
        img1_cv = byte2cv(img1_byte)
        img2_cv = byte2cv(img2_byte)

        bounds1 = get_bounds(node1)
        upper_left1 = (bounds1[0], bounds1[1])
        lower_right1 = (bounds1[0] + bounds1[2], bounds1[1] + bounds1[3])

        bounds2 = get_bounds(node2)
        upper_left2 = (bounds2[0], bounds2[1])
        lower_right2 = (bounds2[0] + bounds2[2], bounds2[1] + bounds2[3])

        # 圈出不匹配的位置
        cv2.rectangle(img1_cv, upper_left1, lower_right1, rec_color, 3)  # 颜色是BGR
        cv2.rectangle(img2_cv, upper_left2, lower_right2, rec_color, 3)

        # 拼接出错的图像便于对比
        diff_img = hconcat_images(img1_cv, img2_cv)

        cv2.imwrite("../log/img/{}.png".format(config.mismatch_no), diff_img)
        config.mismatch_no += 1

    def position_compare(self, node1, node2):
        """
        位置对比，包括1.元素占整个屏幕长宽的百分比和2.元素中点占屏幕位置的百分比
        bounds属性一般形式为：bounds="[16,373][704,757]"，为字符串类型
        :param node1:
        :param node2:
        :return:
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

        node1_center_x = int(node1_bounds[0] + node1_bounds[2] / 2)  # 元素中点的横坐标
        node1_center_y = int(node1_bounds[1] + node1_bounds[3] / 2)  # 元素中点的纵坐标
        node1_center_prop_x = node1_center_x / width1  # 元素中点在x方向占屏幕位置比例
        node1_center_prop_y = node1_center_y / height1  # 元素中点在y方向占屏幕位置比例

        node2_center_x = int(node2_bounds[0] + node2_bounds[2] / 2)
        node2_center_y = int(node2_bounds[1] + node2_bounds[3] / 2)
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

        result = [x < config.position_threshold for x in
                  [center_diff_x, center_diff_y, width_diff, height_diff]]
        if not all(result):  # 如果但凡有一个超过阈值，就有问题
            config.diff_log.write("---------------mismatch-------------------\n")
            self.mismatch(node1, node2)
            return -1

        return 1

    @staticmethod
    def image_compare(node1, node2):
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
        # 对图像节点的处理
        if strict_mode:
            ssim_value = self.image_compare(node1, node2)
            if ssim_value < config.SSIM_threshold:
                self.mismatch(node1, node2)
                return -1
        return self.position_compare(node1, node2)

    def text_node(self, node1, node2, strict_mode=1):
        if strict_mode:
            text1 = node1.get_attribute("text")
            text2 = node2.get_attribute("text")
            if text1 != text2:
                self.mismatch(node1, node2)
                return -1
        return self.position_compare(node1, node2)

    def compare(self, node1, node2):
        class1 = node1.get_attribute("class")
        class2 = node2.get_attribute("class")
        strict_mode = 1
        if class1 in self.white_list["class"]:
            strict_mode = 0
        # 类名检测
        if class1 != class2:
            # 类都不一致，用黑色圈出来
            self.mismatch(node1, node2, rec_color=(255, 0, 0))  # BGR
            return -1

        # 图片检测
        if "ImageView" in class1:
            if self.image_node(node1, node2, strict_mode) < 0:
                return -1

        # 文本检测
        if "TextView" in class1:
            if self.text_node(node1, node2, strict_mode) < 0:
                return -1
        return 1

    def dfs(self):
        # 两个driver对比的函数
        # 严格模式，宽松模式单独列个函数。
        list1 = [self.root1]
        list2 = [self.root2]
        while list1 and list2:
            node1 = list1.pop()
            node2 = list2.pop()

            # compare
            if self.compare(node1, node2) < 0:
                # 如果当前节点有问题，就不用push子节点了，继续就行
                continue
            else:
                class1 = node1.get_attribute("class")
                config.diff_log.write(class1 + " compare OK...\n")

            elements1 = node1.find_elements(By.XPATH, "child::*/*")
            elements2 = node2.find_elements(By.XPATH, "child::*/*")
            for e1 in elements1:
                list1.append(e1)
            for e2 in elements2:
                list2.append(e2)
