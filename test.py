import cv2
import os
import datetime
import time

class StartCV():
    """
    num_camera:摄像头的数量
    path:图像存储的根目录
    """
    def __init__(self, num_camera=3,path='image'):
        super().__init__()
        self.path = path 
        self.num_camera=num_camera 

        # 创建摄像头实例
        for i in range(self.num_camera):
            setattr(self,'camera_'+str(i),cv2.VideoCapture(i))
            

        #cv_event = threading.Event()

    def save_image(self,img,index):
        """
        存储图像
        """
        # 定义存储的根目录，子目录（年月日）以及图像名称（精确到秒）
        save_path=self.path
        save_dir = datetime.datetime.now().strftime('%Y%m%d')
        save_file_name = datetime.datetime.now().strftime('%H%M%S')+'_'+str(index)+'.jpg'
        
        if not os.path.exists(os.path.join(save_path,save_dir)):
            # 判断文件夹是否存在，如果不存在则创建
            os.mkdir(os.path.join(save_path,save_dir))

        cv2.imwrite(os.path.join(save_path,save_dir,save_file_name),img)
        

    def delete(self):
        """删除未使用的图片"""
        pass


    def readimage(self):
        """获得读取的图片，需要打标签，防误删"""
        pass


    def start(self):
        """开始拍照"""
        self.img_0=cv2.resize(self.img_0,(1920,1080),interpolation=cv2.INTER_NEAREST)
        self.img_1=cv2.resize(self.img_1,(1920,1080),interpolation=cv2.INTER_NEAREST)
        self.save_image(self.img_0,0)
        self.save_image(self.img_1,1)
        #self.save_image(self.img_2)
        pass


    def stop(self):
        """暂停拍照"""
        pass


    def open(self):
        """启动摄像头"""
        shortcut = False
        while 1:

            if self.num_camera == 1:
                ret_0,self.img_0=self.camera_0.read()
                cv2.imshow('camera_0',self.img_0)
            elif self.num_camera == 2:
                ret_0,self.img_0=self.camera_0.read()
                ret_1,self.img_1=self.camera_1.read()
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


            key = cv2.waitKey(1) & 0xFF
            if key == ord('c') or shortcut:
                while True:
                    time.sleep(2)
                    self.start()
            
            elif key == ord('q'):
                
                break
            """elif cv2.getWindowProperty(['camera_0','camera_1'], cv2.WND_PROP_AUTOSIZE) < 1:
                break"""
            shortcut = False
        cv2.destroyAllWindows()

            
        self.camera_1.release()
        self.camera_0.release()
        self.camera_2.release()
        pass