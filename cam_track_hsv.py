import cv2
import numpy as np

def nothing(evt):
    pass

def cvt_kel(kel):
    if kel%2==0:
        kel+=1
    return kel

cap = cv2.VideoCapture(0)
cap.set(3, 4608)
cap.set(4, 3456)

set_window = "Setting"
cv2.namedWindow(set_window)
cv2.createTrackbar('highH', set_window, 255, 255, nothing)
cv2.createTrackbar('highS', set_window, 255, 255, nothing)
cv2.createTrackbar('highV', set_window, 255, 255, nothing)

cv2.createTrackbar('lowH', set_window, 0, 255, nothing)
cv2.createTrackbar('lowS', set_window, 0, 255, nothing)
cv2.createTrackbar('lowV', set_window, 0, 255, nothing)

cv2.createTrackbar('kel', set_window, 0, 255, nothing)

while 1:
    key = cv2.waitKey(1)&0xff
    highH = cv2.getTrackbarPos('highH', set_window)
    highS = cv2.getTrackbarPos('highS', set_window)
    highV = cv2.getTrackbarPos('highV', set_window)

    lowH = cv2.getTrackbarPos('lowH', set_window)
    lowS = cv2.getTrackbarPos('lowS', set_window)
    lowV = cv2.getTrackbarPos('lowV', set_window)

    
    MIN = np.array([lowH, lowS, lowV], dtype=np.uint8)
    MAX = np.array([highH, highS, highV], dtype=np.uint8)  
    ret, frame = cap.read()
    frame = cv2.resize(frame, 800, 800)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, MIN, MAX)

    ker = cv2.getTrackbarPos('kel', set_window)
    ker = cvt_kel(ker)
    kernel = cv2.ones(ker,ker)

    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,(7,7))

    cv2.imshow(set_window, mask)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()