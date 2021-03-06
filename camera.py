import cv2
import os
import datetime
import time
from threading import Thread,Event
from multiprocessing import Process

class StartCV():
    """
    num_camera:摄像头的数量 default:1,上限6
    path:图像存储的根目录 default:image
    """
    def __init__(self, num_camera=1,img_path='image',video_path= 'video',height=1080,width=1920):
        super().__init__()
        self.img_path = img_path
        self.video_path = video_path
        self.num_camera=num_camera 
        self.img_cut_thr_sig = True # 控制cut线程生成的信号
        self.stop_img_thr_sig = False # 控制线程，false结束，true保持
        self.vid_cut_thr_sig = True
        self.stop_vid_thr_sig = False
        self.img_cut_evt = Event()
        self.vid_cut_evt = Event()
        self.height = height
        self.width = width

        # 创建摄像头实例
        for i in range(self.num_camera):
            setattr(self,'camera_'+str(i),cv2.VideoCapture(i))


    def save_image(self,img,index):
        """
        存储图像
        img:cv.read的返回值
        index:摄像头索引

        """
        # 定义存储的根目录，子目录（年月日）以及图像名称（精确到秒）
        save_path=self.img_path
        save_dir = datetime.datetime.now().strftime('%Y%m%d')
        save_file_name = datetime.datetime.now().strftime('%H%M%S')+'_'+str(index)+'.jpg'
        
        if not os.path.exists(os.path.join(save_path,save_dir)):
            # 判断文件夹是否存在，如果不存在则创建
            os.makedirs(os.path.join(save_path,save_dir))

        cv2.imwrite(os.path.join(save_path,save_dir,save_file_name),img)


    
    def save_video(self,index):
        '''存储视频'''
        # 定义存储的根目录，子目录（年月日）以及视频名称
        save_path = self.video_path
        save_dir = datetime.datetime.now().strftime('%Y%m%d')
        save_file_name = datetime.datetime.now().strftime('%H%M%S')+'_'+str(index)+'.mp4'
        if not os.path.exists(os.path.join(save_path,save_dir)):
            # 判断文件夹是否存在，如果不存在则创建
            os.makedirs(os.path.join(save_path,save_dir))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(os.path.join(save_path,save_dir,save_file_name),fourcc, 240.0, (640,480))
        return out
        #while self.stop_vid_thr_sig:
        #    out.write(self.img_0)

    def delete(self):
        """删除未使用的图片"""
        pass


    def readimage(self):
        """获得读取的图片，需要打标签，防误删"""
        pass


    def img_cut(self,):
        """开始拍照"""
        # 设置保存的尺寸
        try:
            self.img_0=cv2.resize(self.img_0,(self.width,self.height),interpolation=cv2.INTER_NEAREST)
            self.img_1=cv2.resize(self.img_1,(self.width,self.height),interpolation=cv2.INTER_NEAREST)
            self.img_2=cv2.resize(self.img_2,(self.width,self.height),interpolation=cv2.INTER_NEAREST)
            self.img_3=cv2.resize(self.img_3,(self.width,self.height),interpolation=cv2.INTER_NEAREST)
            self.img_4=cv2.resize(self.img_4,(self.width,self.height),interpolation=cv2.INTER_NEAREST)
            self.img_5=cv2.resize(self.img_5,(self.width,self.height),interpolation=cv2.INTER_NEAREST)
        except AttributeError:
            pass

        self.img_cut_evt.wait()
        while self.stop_img_thr_sig:
            time.sleep(2)
            try:
                self.save_image(self.img_0,0)
                self.save_image(self.img_1,1)
                self.save_image(self.img_2,2)
                self.save_image(self.img_3,3)
                self.save_image(self.img_4,4)
                self.save_image(self.img_5,5)
            except AttributeError:
                pass
        pass


    def video_cut(self):
        '''开始录制的接口
        '''
        self.vid_cut_evt.wait()
        out=self.save_video(index=0)

        while self.stop_vid_thr_sig:
            out.write(self.img_0)
        pass


    def start_img_cut(self,):
        '''开始拍照的接口
            发送Event的set信号
        '''
        self.stop_img_thr_sig = True 
        self.img_cut_evt.set() # 发送启动线程的信号


    def stop_img_cut(self):
        """停止拍照的接口，同时也是停止录制的接口
            同时发送信号结束线程
        """
        self.img_cut_evt.clear()
        self.stop_img_thr_sig = False #
        self.img_cut_thr_sig = True # 重新启动一个新的线程

        self.vid_cut_evt.clear()
        self.stop_vid_thr_sig = False
        self.vid_cut_thr_sig = True
        pass


    def start_vid_cut(self):
        '''开始视频录制的接口'''
        self.stop_vid_thr_sig = True
        self.vid_cut_evt.set()
        pass

    def stop_vid_cut(self):
        '''停止视频录制的接口'''
        pass
    def find_rectangle(self,contour):
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

    def locate_license(self,img):
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
            r = self.find_rectangle(c)
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

    def detect(self,img):
        '''检测当前帧的矩形轮廓
        return：
        经过检测的帧
        '''
        # 预处理，灰度+高斯模糊
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gs_img = cv2.GaussianBlur(gray_img, (3,3), 0, 0, cv2.BORDER_DEFAULT)

        # Canny寻找轮廓
        ret, thresh = cv2.threshold(gs_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        canny = cv2.Canny(thresh,100,150)
        
        # 对轮廓的矩形进行判定，然后绘制
        rect=self.locate_license(canny)
        cv2.rectangle(img,(rect[0][0][0],rect[0][0][1]),(rect[0][0][2],rect[0][0][3]),(0,255,0),2)
    
    def data_path(self):
        '''
        Return:当天的image存储路径,视频存储路径
        '''
        path_date = datetime.datetime.now().strftime('%Y%m%d')
        img_data_path = os.path.join('image',path_date)
        video_data_path = os.path.join('video',path_date)
        return img_data_path, video_data_path

    def control(self):
        """启动摄像头
            包括按键接收等等
        """
        while True:
            if self.num_camera == 1:
                ret_0,self.img_0=self.camera_0.read()
                self.detect(self.img_0)
                
                cv2.imshow('camera_0',self.img_0)
            elif self.num_camera == 2:
                ret_0,self.img_0=self.camera_0.read()
                ret_1,self.img_1=self.camera_1.read()
                self.detect(self.img_0)
                self.detect(self.img_1)
                cv2.imshow('camera_0',self.img_0)
                cv2.imshow('camera_1',self.img_1)
            elif self.num_camera == 3:
                ret_0,self.img_0=self.camera_0.read()
                ret_1,self.img_1=self.camera_1.read()
                ret_2,self.img_2=self.camera_2.read()
                cv2.imshow('camera_0',self.img_0)
                cv2.imshow('camera_1',self.img_1)
                cv2.imshow('camera_2',self.img_2)
            elif self.num_camera == 4:
                ret_0,self.img_0=self.camera_0.read()
                ret_1,self.img_1=self.camera_1.read()
                ret_2,self.img_2=self.camera_2.read()
                ret_3,self.img_3=self.camera_3.read()
                cv2.imshow('camera_0',self.img_0)
                cv2.imshow('camera_1',self.img_1)
                cv2.imshow('camera_2',self.img_2)
                cv2.imshow('camera_3',self.img_3)
            elif self.num_camera == 5:
                ret_0,self.img_0=self.camera_0.read()
                ret_1,self.img_1=self.camera_1.read()
                ret_2,self.img_2=self.camera_2.read()
                ret_3,self.img_3=self.camera_3.read()
                ret_4,self.img_4=self.camera_4.read()
                cv2.imshow('camera_0',self.img_0)
                cv2.imshow('camera_1',self.img_1)
                cv2.imshow('camera_2',self.img_2)
                cv2.imshow('camera_3',self.img_3)
                cv2.imshow('camera_4',self.img_4)
            elif self.num_camera == 6:
                ret_0,self.img_0=self.camera_0.read()
                ret_1,self.img_1=self.camera_1.read()
                ret_2,self.img_2=self.camera_2.read()
                ret_3,self.img_3=self.camera_3.read()
                ret_4,self.img_4=self.camera_4.read()
                ret_5,self.img_5=self.camera_5.read()
                cv2.imshow('camera_0',self.img_0)
                cv2.imshow('camera_1',self.img_1)
                cv2.imshow('camera_2',self.img_2)
                cv2.imshow('camera_3',self.img_3)
                cv2.imshow('camera_4',self.img_4)
                cv2.imshow('camera_5',self.img_5)


            if self.img_cut_thr_sig:
                # 设置线程，但是该线程受到cut_event的阻塞，需要等待self.start()给信号
                self.img_cut_thr_sig = False
                start_img_thread = Thread(target=self.img_cut,daemon=True) # 设置后台线程
                start_img_thread.setName('img_thread')
                start_img_thread.start()
            
            if self.vid_cut_thr_sig:
                self.vid_cut_thr_sig = False
                start_vid_thread = Thread(target=self.video_cut,daemon=True)
                start_vid_thread.setName('video_thread')
                start_vid_thread.start()

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                self.start_img_cut()
            if key == ord('s'):
                self.stop_img_cut()
            elif key == ord('v'):
                self.start_vid_cut()
            elif cv2.getWindowProperty('camera_0', cv2.WND_PROP_AUTOSIZE) < 1:
                break

        cv2.destroyAllWindows()
        for i in range(self.num_camera):
            exec('self.camera_{}.release()'.format(i))
        pass

