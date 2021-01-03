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
        列表，轮廓值
    '''
    contours,hier=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #找出最大的区域
    block=[]
    for c in contours:
        #找出轮廓的左上点和右下点，由此计算它的面积和长度比
        r=find_rectangle(c)
        a=(r[2]-r[0])*(r[3]-r[1])   #面积
        s=(r[2]-r[0])*(r[3]-r[1])   #长度比
        
        block.append([r,a,s])
    #max_index=block[]
    #选出面积最大的区域
    block=sorted(block,key=lambda b: b[1])[-1:]
    return block[0][0]
 
img =cv2.imread("image/NO_2.jpg")
#img =cv2.imread("image/yes_0.jpg")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray_img)
# 高斯图片降噪
gs_img = cv2.GaussianBlur(gray_img, (3,3), 0, 0, cv2.BORDER_DEFAULT)



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

cv2.rectangle(canny,(rect[0],rect[1]),(rect[2],rect[3]),(255,255,250),2)
cv2.imshow('rect',canny)
#cv2.imwrite('test.jpg',img)


cv2.waitKey(0)
cv2.destroyAllWindows()