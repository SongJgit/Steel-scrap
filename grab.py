import cv2



cameraCapture0 = cv2.VideoCapture(0)

success0 = cameraCapture0.grab()
frame0= cameraCapture0.retrieve()
while 1:
    cv2.imshow('came',frame0)
    frame0= cameraCapture0.retrieve()
        
