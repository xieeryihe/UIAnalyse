# 对比模块
from diff.image import *
from skimage.measure import compare_ssim


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

    ssim_value = compare_ssim(gray_image1, gray_image2)

    # 打印SSIM值
    print("The SSIM value is", ssim_value)
