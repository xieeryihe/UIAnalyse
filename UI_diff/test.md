记录测试的函数

Devices类中测试用的的成员函数

```python
def test_single(self):
    driver = self.devices[0].driver
    root = driver.find_element(By.XPATH, "/hierarchy/*")  # 得到顶层元素
    print(root)


def compare_test(self):
    """
    对比测试
    :return:
    """
    driver1 = self.devices[0].driver
    driver2 = self.devices[1].driver
    img1_node = driver1.find_element(By.ID, "category_image")
    img2_node = driver2.find_element(By.ID, "category_image")
    img1 = img1_node.screenshot_as_png
    img2 = img2_node.screenshot_as_png
    img1_cv = byte2cv(img1)
    img2_cv = byte2cv(img2)
    print(img1_node.get_attribute("bounds"))
    print(img2_node.get_attribute("bounds"))
    # cv2.imshow("Image1", img1_cv)
    # cv2.imshow("Image2", img2_cv)
    # cv2.waitKey(0)
    cv2.imwrite('./img1.jpg', img1_cv)
    cv2.imwrite('./img2.jpg', img2_cv)

```
