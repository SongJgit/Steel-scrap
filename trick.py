import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ret,frame = cap.read()
#设置跟踪窗口大小
r,h,c,w = 10,200,10,200
track_window = (c,r,w,h)

roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#inRange函数用来设置下限和上限值
mask = cv2.inRange(hsv_roi,np.array((100.,30.,32.)),np.array((180.,120.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,1)
while True:
    ret,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        ret,track_window = cv2.meanShift(dst,track_window,term_crit)

        x,y,w,h = track_window
        img2 = cv2.rectangle(frame,(x,y),(x+w,y+h),255,2)
        cv2.imshow('img2',img2)

        if cv2.waitKey(100) & 0xff == ord("q"):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()