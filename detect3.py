import  cv2
import numpy as np

def stretch(img):
    '''
    图像拉伸函数
    '''
    maxi=float(img.max())
    mini=float(img.min())
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i,j]=(255/(maxi-mini)*img[i,j]-(255*mini)/(maxi-mini))
    
    return img

def dobinaryzation(img):
    '''
    二值化处理函数
    '''
    maxi=float(img.max())
    mini=float(img.min())
    
    x=maxi-((maxi-mini)/2)
    #二值化,返回阈值ret  和  二值化操作后的图像thresh
    ret,thresh=cv2.threshold(img,x,255,cv2.THRESH_BINARY)
    #返回二值化后的黑白图像
    return thresh

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

def locate_license(img,afterimg):
    '''
    定位图中最大的矩形
    return：
        列表，轮廓值
    '''
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #找出最大的三个区域
    block=[]
    for c in contours:
        #找出轮廓的左上点和右下点，由此计算它的面积和长度比
        r=find_rectangle(c)
        a=(r[2]-r[0])*(r[3]-r[1])   #面积
        s=(r[2]-r[0])*(r[3]-r[1])   #长度比
        
        block.append([r,a,s])
    #选出面积最大的区域
    block=sorted(block,key=lambda b: b[1])[-3:]
    return block[0][0]

def find_license(img):
    '''
    预处理函数
    return：
        rect 轮廓
        img 压缩后的图像

    '''
    m=400*img.shape[0]/img.shape[1]
    
    #压缩图像
    img=cv2.resize(img,(400,int(m)),interpolation=cv2.INTER_CUBIC)
    
    #BGR转换为灰度图像
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    #灰度拉伸
    stretchedimg=stretch(gray_img)
    
    '''进行开运算，用来去除噪声'''
    r=16
    h=w=r*2+1
    kernel=np.zeros((h,w),np.uint8)
    cv2.circle(kernel,(r,r),r,1,-1)
    #开运算
    openingimg=cv2.morphologyEx(stretchedimg,cv2.MORPH_OPEN,kernel)
    #获取差分图，两幅图像做差  cv2.absdiff('图像1','图像2')
    strtimg=cv2.absdiff(stretchedimg,openingimg)
    
    #图像二值化
    binaryimg=dobinaryzation(strtimg)
    
    #canny边缘检测
    canny=cv2.Canny(binaryimg,binaryimg.shape[0],binaryimg.shape[1])
    
    '''消除小的区域，保留大块的区域，从而定位矩形'''
    #进行闭运算
    kernel=np.ones((5,19),np.uint8)
    closingimg=cv2.morphologyEx(canny,cv2.MORPH_CLOSE,kernel)
    
    #进行开运算
    openingimg=cv2.morphologyEx(closingimg,cv2.MORPH_OPEN,kernel)
    
    #再次进行开运算
    kernel=np.ones((11,5),np.uint8)
    openingimg=cv2.morphologyEx(openingimg,cv2.MORPH_OPEN,kernel)
    
    #消除小区域，定位矩形位置
    rect=locate_license(openingimg,img)
    
    return rect,img


def cut_license(afterimg,rect):
    '''
    图像分割函数
    '''
    #转换为宽度和高度
    rect[2]=rect[2]-rect[0]
    rect[3]=rect[3]-rect[1]
    rect_copy=tuple(rect.copy())
    rect=[0,0,0,0]
    #创建掩膜
    mask=np.zeros(afterimg.shape[:2],np.uint8)
    #创建背景模型  大小只能为13*5，行数只能为1，单通道浮点型
    bgdModel=np.zeros((1,65),np.float64)
    #创建前景模型
    fgdModel=np.zeros((1,65),np.float64)
    #分割图像
    cv2.grabCut(afterimg,mask,rect_copy,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2=np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img_show=afterimg*mask2[:,:,np.newaxis]
    
    return img_show




if __name__=='__main__':
    img=cv2.imread('image/20201228/151815_0.jpg',cv2.IMREAD_COLOR)
    #预处理图像
    rect,afterimg=find_license(img)

    #框出矩形
    cv2.rectangle(afterimg,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),2)
    cv2.imshow('afterimg',afterimg)
    #分割矩形与背景
    cutimg=cut_license(afterimg,rect)
    cv2.imshow('cutimg',cutimg)

    cv2.waitKey(0)
    cv2.destroyAllWindows()