import cv2
from cv2 import threshold 
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 4608)
cap.set(4, 3456)

def nothing(evt):
    pass

set_window = 'Setting'
cv2.namedWindow(set_window)
cv2.createTrackbar('max', set_window, 255, 255, nothing)
cv2.createTrackbar('min', set_window, 0, 255, nothing)

while 1:
    key = cv2.waitKey(1)&0xff

    MIN = cv2.getTrackbarPos('min', set_window)
    MAX = cv2.getTrackbarPos('max', set_window)

    ret, frame = cap.read()
    frame = cv2.resize(frame, (800, 800))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,th = cv2.threshold(gray,MIN,MAX,cv2.THRESH_BINARY)
    th1 = cv2.adaptiveThreshold(gray,MAX, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
          cv2.THRESH_BINARY,11,2)
    cv2.imshow(set_window, th)
    cv2.imshow('adaptive gausian', th1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()