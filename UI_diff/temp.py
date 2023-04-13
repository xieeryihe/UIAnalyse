import cv2
import pytesseract

# 读取图片并将其转换为灰度图像
img = cv2.imread('image.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 对灰度图像进行二值化处理
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# 使用Tesseract OCR识别文本
text = pytesseract.image_to_string(thresh)

# 获取每个识别出来的文本的边界框并计算大小和颜色
boxes = pytesseract.image_to_boxes(thresh)
for b in boxes.splitlines():
    b = b.split(' ')
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    text_size = (w, h)
    text_region = img[y:y+h, x:x+w]
    text_color = cv2.mean(text_region)

    # 输出结果
    print(f'Text: {b[0]}, Size: {text_size}, Color: {text_color}')

# 显示结果
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
