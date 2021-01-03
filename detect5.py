import cv2
import numpy as np
def find_rectangle(contour):
    '''
    寻找矩形轮廓
    return：
        列表，包含四个值，x和y的最值坐标
    '''
    y,x=[],[]
    
    for p in contour:
        y.append(p[0][0])
        x.append(p[0][1])
    
    return [min(y),min(x),max(y),max(x)]

def locate_license(img):
    '''
    定位图中最大的矩形
    return：
        [[矩形坐标]，矩形框面积，长度比，矩，[轮廓面积,索引]]
    '''
    contours,hier = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # 找出最大的区域
    maxarea = 0
    area = []
    block = []
    for index,c in enumerate(contours):
        # 找出轮廓的左上点和右下点，由此计算它的面积和长度比
        area = []
        r = find_rectangle(c)
        s = (r[2]-r[0])*(r[3]-r[1])   # 矩形框的面积
        l = (r[2]-r[0])*(r[3]-r[1])   # 长度比
        p = cv2.arcLength(c,False)  # 轮廓周长
        M = cv2.moments(c)          # 矩
        cs = cv2.contourArea(c)   # 轮廓面积
        if cs > maxarea:
            # 计算最大的轮廓面积
            maxarea = cs
            max_index = index
        area.append(cs)
        area.append(index)
        block.append([r,s,l,M,p,area,c])
    # max_index=block[]
    # 选出指定的参数获得区域
    block = sorted(block,key=lambda b: b[4])[-1:]
    return block


img =cv2.imread("image/NO_2.jpg")
#img =cv2.imread("image/yes_0.jpg")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray_img)
# 高斯图片降噪
gs_img = cv2.GaussianBlur(gray_img, (5,5), 0, 0, cv2.BORDER_DEFAULT)



# 形态学处理
'''kernel = np.ones((3,3)) 
img1=cv2.dilate(gs_img,kernel,iterations=1)
img1 = cv2.erode(img1, kernel, iterations=1)
#img1=cv2.dilate(img1,kernel,iterations=1)
cv2.imshow('oc',img1)'''

# Canny寻找轮廓
ret, thresh = cv2.threshold(gs_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
canny = cv2.Canny(thresh,100,150)
cv2.imshow('canny',canny)



rect=locate_license(canny)

cv2.rectangle(canny,(rect[0][0][0],rect[0][0][1]),(rect[0][0][2],rect[0][0][3]),(0,255,0),2)

x,y,w,h = cv2.boundingRect(rect[0][6])
# 图像切割
# 第一个参数是高度，第二个参数是宽度
newimage = img[y:y+h,x:x+w] 
cv2.imshow('new_img',newimage)
cv2.imwrite('no.jpg',newimage)
cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imshow('rect',img)
#cv2.imwrite('test.jpg',img)


# 图像切割
# 第一个参数是高度，第二个参数是宽度


cv2.waitKey(0)
cv2.destroyAllWindows()