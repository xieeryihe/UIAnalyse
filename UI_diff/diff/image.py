# 图像处理与对比

import io
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity


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


def image_compare_test(image1_byte, image2_byte):
    image1_cv = byte2cv(image1_byte)
    image2_cv = byte2cv(image2_byte)
    gray_image1 = cv2.cvtColor(image1_cv, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2_cv, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.resize(gray_image2, (gray_image1.shape[1], gray_image1.shape[0]))
    # structural_similarity 的两个图片必须是相同size
    ssim_value = structural_similarity(gray_image1, gray_image2)
    # 打印SSIM值
    print("The SSIM value is", ssim_value)
    return ssim_value
