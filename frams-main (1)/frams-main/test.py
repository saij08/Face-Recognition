import cv2
import os

videoCaptureObject = cv2.VideoCapture(0)
result = True
while(result):
    ret,frame = videoCaptureObject.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) == ord("q"):
        
        result=False
    

videoCaptureObject.release()
cv2.destroyAllWindows()