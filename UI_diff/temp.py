from diff.image import *
from PIL import Image

img0 = cv2.imread("res/Image/0.png")
img1 = cv2.imread("res/Image/1.png")
gray_image0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
gray_image1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
print(gray_image0.shape)
print(gray_image1.shape)
img2 = cv2.resize(gray_image0, gray_image1.shape)
# gray_img为二维矩阵表示,要实现array到image的转换
img2 = Image.fromarray(img2)
img2.save("res/Image/3.png")
