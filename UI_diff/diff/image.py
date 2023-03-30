# 图像处理

import io
import cv2
import numpy as np
from PIL import Image


def image2byte(image):
    # 图片转byte, image: 必须是PIL格式
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
    # byte转为图片
    image = Image.open(io.BytesIO(byte_data))
    return image


def byte2cv(im):
    # 二进制图片转cv2
    return cv2.imdecode(np.array(bytearray(im), dtype='uint8'), cv2.IMREAD_UNCHANGED)  # 从二进制图片数据中读取


def img_padding(img_cv2, dst_width, dst_height, x_offset=0, y_offset=0, channel=3):
    src_height, src_width, _ = img_cv2.shape
    new_img = np.zeros((dst_height, dst_width, channel), dtype=np.uint8)
    new_img[y_offset: y_offset + src_height, x_offset: x_offset + src_width] = img_cv2
    return new_img


def hconcat_images(img1_cv2, img2_cv2, divider_flag=True, width=3, color=(0, 0, 255)):
    # 颜色是BGR顺序
    height1, width1, _ = img1_cv2.shape
    height2, width2, _ = img2_cv2.shape
    dst_height = height2  # 目标高度是选高的
    if height1 > height2:
        dst_height = height1
        img2_cv2 = img_padding(img2_cv2, width2, height1)
    else:
        img1_cv2 = img_padding(img1_cv2, width1, height2)

    if divider_flag:
        line_divider = np.zeros((dst_height, width, 3), np.uint8)
        line_divider[:, :] = color
        dst = cv2.hconcat([img1_cv2, line_divider, img2_cv2])
    else:
        dst = cv2.hconcat([img1_cv2, img2_cv2])

    return dst


def test_concat():
    # 加载图片
    img1_cv2 = cv2.imread('./1.png')
    img2_cv2 = cv2.imread('./2.png')

    # 获取图片大小

    dst = hconcat_images(img1_cv2, img2_cv2)
    # 保存结果
    cv2.imshow("image", dst)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
