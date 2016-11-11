import cv2
import numpy as np
from numpy import *
import sys
import os
from subprocess import call
pathToVideo = sys.argv[1]
cap = cv2.VideoCapture(pathToVideo)

os.mkdir('./temp')
ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
iter=0;
while True:
    iter=iter+1
    ret, frame2 = cap.read()
    if(not ret):
        break 
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prvs,next, 0.5, 3, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    cv2.imwrite('./temp/res%d.jpg' % (iter), bgr)
    
    prvs = next

cap.release()
cv2.destroyAllWindows()
os.system('ffmpeg -framerate 10 -i ./temp/res%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p ~/Videos/cvflow.mp4')

os.system("rm -r ./temp")
