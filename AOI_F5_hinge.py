
import FINS_TCP
import cv2
import numpy as np

ip = '192.168.250.1'
soc = FINS_TCP.TCPconnect(host=ip, port = 9600)
soc.connectt()
cap = cv2.VideoCapture(0)
cap.set(3, 4608)
cap.set(4, 3456)

def readDM(area):
    content = soc.ReadMemory(FINS_TCP.FinsCommandCode().MEMORY_AREA_READ,
                            FINS_TCP.FinsPLCMemoryAreas().DATA_MEMORY_WORD, area)
    return content

def writeDM(area, mess):
    soc.WriteMemory(FINS_TCP.FinsCommandCode().MEMORY_AREA_WRITE,
                    FINS_TCP.FinsPLCMemoryAreas().DATA_MEMORY_WORD, area, mess)

def nothing(evt):
    pass

roi_corners = np.array([[(410, 250),(550, 150),(790,450),(700, 550)]], dtype=np.int32)
ignore_mask_color = (255,255,255)
font = cv2.FONT_HERSHEY_COMPLEX
set_winname = 'setting'
cv2.namedWindow(set_winname)
cv2.createTrackbar('maxH', set_winname, 255, 255, nothing)
cv2.createTrackbar('maxS', set_winname, 255, 255, nothing)
cv2.createTrackbar('maxV', set_winname, 169, 255, nothing)
cv2.createTrackbar('minH', set_winname, 1, 255, nothing)
cv2.createTrackbar('minS', set_winname, 0, 255, nothing)
cv2.createTrackbar('minV', set_winname, 0, 255, nothing)
while 1:
    key = cv2.waitKey(1)&0xff
    ret, frame = cap.read()

    maxH = cv2.getTrackbarPos('maxH', set_winname)
    maxS = cv2.getTrackbarPos('maxS', set_winname)
    maxV = cv2.getTrackbarPos('maxV', set_winname)

    minH = cv2.getTrackbarPos('minH', set_winname)
    minS = cv2.getTrackbarPos('minS', set_winname)
    minV = cv2.getTrackbarPos('minV', set_winname)

    MAX = np.array([maxH, maxS, maxV])
    MIN = np.array([minH, minS, minV])

    frame = cv2.resize(frame, (800, 800))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_zero = np.zeros(hsv.shape, dtype=np.uint8)
    cv2.fillPoly(mask_zero, roi_corners, ignore_mask_color)
    roi_img = cv2.bitwise_and(hsv, mask_zero)

    mask = cv2.inRange(roi_img, MIN, MAX)
    kernel = cv2.ones(7,7)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,(7,7))

    contours, hierachi = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    D300 = readDM(300)[-1]

    if len(contours)!=0:
        max_c = max(contours, key = cv2.contourArea)
        area = cv2.contourArea(max_c)
        bounding_rect_contour = cv2.minAreaRect(max_c)
        bounding_contour_box = np.int0(cv2.boxPoints(bounding_rect_contour))
        print(area) 
        if area>55000:
            cv2.drawContours(frame, [bounding_contour_box], 0, (0, 255, 0), 2)
            cv2.putText(frame, "OK", (300, 300), font, 2, (0,255,0), 3)
        if area<55000:
            cv2.drawContours(frame, [bounding_contour_box], 0, (0, 0, 255), 2)
            cv2.putText(frame, "NG", (300, 300), font, 2, (0,0,255), 3)
    cv2.imshow('frame', frame)
    if D300 == 1:
        writeDM(300, 10)
        cv2.imshow('AOI_F5', frame)
    
    if key == ord(' '):
        writeDM(300, 1)

    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
