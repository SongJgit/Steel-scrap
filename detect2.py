import cv2
import numpy as np

# pyrDown():brief Blurs an image and downsamples it.
# 将图像高斯平滑，然后进行降采样
img = cv2.pyrDown(cv2.imread('image/20201228/151815_0.jpg', cv2.IMREAD_UNCHANGED))
kernel = np.ones((4,4))  


# 依然是二值化操作

ret, thresh = cv2.threshold(cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
# 计算图像的轮廓
contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    # find bounding box coordinates
    # 先计算出一个简单的边界狂，也就是一个矩形
    # 就是将轮廓信息转换为(x,y)坐标，并加上矩形的高度和宽度
    x, y, w, h = cv2.boundingRect(c)
    # 画出该矩形
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    


    

# 绘制轮廓
cv2.drawContours(img, contours, -1, (255, 0, 0), 1)
cv2.imshow("contours", img)

cv2.waitKey()
cv2.destroyAllWindows()